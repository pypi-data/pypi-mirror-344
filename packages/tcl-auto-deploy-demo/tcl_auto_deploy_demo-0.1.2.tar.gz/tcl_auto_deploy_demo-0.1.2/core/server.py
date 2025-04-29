"""
MCP 服务器核心
"""
import logging
from typing import Dict, Any, List
import signal
import sys
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
import uvicorn
from datetime import datetime
import inspect
import functools
import json

from config import settings
from core.utils import load_tool

logger = logging.getLogger(__name__)

class MCPServer:
    """MCP 服务器核心类"""
    
    def __init__(self):
        """初始化 MCP 服务器"""
        self.config = settings.SERVER_CONFIG
        self.tools: Dict[str, Any] = {}
        self.mcp = FastMCP(self.config['name'])
        self.mcp_server = self.mcp._mcp_server  # noqa: WPS437
        # 添加SSE传输实例字典
        self.sse_transports: Dict[str, SseServerTransport] = {}
        
    async def initialize(self) -> None:
        """初始化服务器"""
        logger.info("正在初始化服务器...")
        
        # 加载工具
        await self._load_tools()
        
        # 注册信号处理器
        self._register_signal_handlers()
        
        logger.info("服务器初始化完成")
        
    async def _load_tools(self) -> None:
        """加载所有工具"""
        logger.info("正在加载工具...")
        
        for tool_name, tool_config in settings.TOOLS_CONFIG.items():
            try:
                logger.info(f"开始加载工具: {tool_name}, 配置: {tool_config}")
                tool = load_tool(tool_config)
                if tool:
                    logger.info(f"工具 {tool_name} 创建成功，准备初始化")
                    await tool.initialize()
                    self.tools[tool_name] = tool
                    logger.info(f"工具 {tool_name} 初始化成功，准备注册方法")
                    self._register_tool_methods(tool)
                    logger.info(f"工具加载成功: {tool_name}")
                else:
                    logger.warning(f"工具 {tool_name} 加载返回 None")
            except Exception as e:
                logger.error(f"工具加载失败: {tool_name}, 错误: {str(e)}", exc_info=True)
                
        logger.info(f"工具加载完成，共加载 {len(self.tools)} 个工具")
        
    def _register_tool_methods(self, tool: Any) -> None:
        """注册工具方法到 MCP 服务器
        
        Args:
            tool: 工具实例
        """
        for method_name, method_info in tool.get_tool_info()['methods'].items():
            method = getattr(tool, method_name)
            
            # 构建完整的方法描述
            method_description = ""
            
            # 添加方法文档
            if 'description' in method_info and method_info['description']:
                method_description += method_info['description']
            elif method.__doc__:
                method_description += method.__doc__
                
            # 直接使用 add_tool 方法注册工具，更加简洁
            self.mcp.add_tool(
                fn=method,
                name=method_name,
                description=method_description
            )
            
            logger.debug(f"注册工具方法: {method_name}, 描述: {method_description}")
            
    def _register_signal_handlers(self) -> None:
        """注册信号处理器"""
        def signal_handler(sig, frame):
            logger.info("收到退出信号，正在关闭服务器...")
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
    def create_app(self) -> Starlette:
        """创建 Starlette 应用
        
        Returns:
            Starlette 应用实例
        """
        # 创建主SSE传输实例
        main_sse = SseServerTransport("/messages/")
        logger.info("创建主 SSE 传输实例")
        
        # 创建路由列表
        routes = []
        
        # 创建主MCP服务器（包含所有工具）
        main_mcp = self.mcp
        main_mcp_server = self.mcp_server
        
        # 添加主SSE路由处理函数
        async def handle_main_sse(request: Request) -> None:
            client_host = request.client.host if request.client else "unknown"
            logger.info(f"收到新的主SSE连接请求 - 客户端: {client_host}")
            
            try:
                async with main_sse.connect_sse(
                    request.scope,
                    request.receive,
                    request._send,  # noqa: SLF001
                ) as (read_stream, write_stream):
                    logger.debug("主SSE连接建立成功，准备初始化服务器")
                    await main_mcp_server.run(
                        read_stream,
                        write_stream,
                        main_mcp_server.create_initialization_options(),
                    )
            except Exception as e:
                logger.error(f"主SSE连接处理失败 - 客户端: {client_host}, 错误: {str(e)}", exc_info=True)
                raise
        
        # 添加主SSE路由
        routes.append(Route("/sse", endpoint=handle_main_sse))
        routes.append(Mount("/messages/", app=main_sse.handle_post_message))
        
        # 为每个工具创建SSE路由
        for tool_name, tool in self.tools.items():
            # 创建工具专用的MCP服务器实例
            tool_mcp = FastMCP(f"{self.config['name']} - {tool_name}")
            tool_mcp_server = tool_mcp._mcp_server  # noqa: WPS437
            
            # 只注册当前工具的方法
            for method_name, method_info in tool.get_tool_info()['methods'].items():
                method = getattr(tool, method_name)
                
                # 构建完整的方法描述
                method_description = ""
                
                # 添加方法文档
                if 'description' in method_info and method_info['description']:
                    method_description += method_info['description']
                elif method.__doc__:
                    method_description += method.__doc__
                    
                # 注册工具方法到工具专用的MCP服务器
                tool_mcp.add_tool(
                    fn=method,
                    name=method_name,
                    description=method_description
                )
                
                logger.debug(f"注册工具方法到 {tool_name} 专用服务器: {method_name}")
            
            # 创建工具专用的SSE传输实例
            tool_messages_path = f"/{tool_name}/messages/"
            tool_sse = SseServerTransport(tool_messages_path)
            self.sse_transports[tool_name] = tool_sse
            logger.info(f"创建 {tool_name} 工具的 SSE 传输实例")
            
            # 创建工具专用的SSE路由处理函数
            def create_tool_sse_handler(t_name, t_sse, t_mcp_server):
                async def handle_tool_sse(request: Request) -> None:
                    client_host = request.client.host if request.client else "unknown"
                    logger.info(f"收到新的 {t_name} 工具SSE连接请求 - 客户端: {client_host}")
                    
                    try:
                        async with t_sse.connect_sse(
                            request.scope,
                            request.receive,
                            request._send,  # noqa: SLF001
                        ) as (read_stream, write_stream):
                            logger.debug(f"{t_name} 工具SSE连接建立成功，准备初始化服务器")
                            await t_mcp_server.run(
                                read_stream,
                                write_stream,
                                t_mcp_server.create_initialization_options(),
                            )
                    except Exception as e:
                        logger.error(f"{t_name} 工具SSE连接处理失败 - 客户端: {client_host}, 错误: {str(e)}", exc_info=True)
                        raise
                return handle_tool_sse
            
            # 添加工具专用的SSE路由
            tool_sse_handler = create_tool_sse_handler(tool_name, tool_sse, tool_mcp_server)
            routes.append(Route(f"/{tool_name}/sse", endpoint=tool_sse_handler))
            routes.append(Mount(tool_messages_path, app=tool_sse.handle_post_message))
            logger.info(f"添加 {tool_name} 工具的SSE路由: /{tool_name}/sse 【仅包含{tool_name}工具的方法】")

        # 创建Starlette应用
        app = Starlette(
            debug=self.config['debug'],
            routes=routes,
        )
        logger.info("Starlette 应用创建完成")
        return app
        
    def print_server_info(self) -> None:
        """打印服务器信息"""
        logger.info("="*50)
        logger.info(f"{self.config['name']}启动中...")
        logger.info("="*50)
        
        logger.info("服务配置信息:")
        logger.info("-"*30)
        logger.info(f"- 服务名称: {self.config['name']}")
        logger.info(f"- 启动时间: {datetime.now().isoformat()}")
        logger.info(f"- 监听地址: {self.config['host']}")
        logger.info(f"- 监听端口: {self.config['port']}")
        logger.info(f"- 服务地址: http://{self.config['host'] if self.config['host'] != '0.0.0.0' else '127.0.0.1'}:{self.config['port']}")
        
        if self.tools:
            logger.info("- 已加载工具:")
            for tool_name, tool in self.tools.items():
                tool_info = tool.get_tool_info()
                logger.info(f"  * {tool_name}:")
                for method_name in tool_info['methods'].keys():
                    logger.info(f"    - {method_name}")
                    
        logger.info("- 端点信息:")
        logger.info("  * 主SSE端点: /sse (包含所有工具)")
        logger.info("  * 主消息端点: /messages/")
        
        # 添加每个工具的SSE端点信息
        for tool_name in self.tools.keys():
            logger.info(f"  * {tool_name} 工具SSE端点: /{tool_name}/sse (仅包含{tool_name}工具)")
            logger.info(f"  * {tool_name} 工具消息端点: /{tool_name}/messages/")
            
        logger.info("-"*30)
        
        # 创建并打印主服务器配置
        main_server_config = {
            "mcpServers": {
                # 主服务器配置
                "personal-mcp-server": {
                    "url": f"http://{'127.0.0.1' if self.config['host'] == '0.0.0.0' else self.config['host']}:{self.config['port']}/sse"
                }
            }
        }
        
        # 打印主服务器配置
        logger.info("主服务器配置:")
        logger.info("-"*30)
        logger.info(json.dumps(main_server_config, indent=2, ensure_ascii=False))
        logger.info("-"*30)
        
        # 创建并打印工具服务器配置
        if self.tools:
            tools_config = {
                "mcpServers": {}
            }
            
            # 为每个工具添加单独的配置
            for tool_name in self.tools.keys():
                tools_config["mcpServers"][f"personal-mcp-server-{tool_name}"] = {
                    "url": f"http://{'127.0.0.1' if self.config['host'] == '0.0.0.0' else self.config['host']}:{self.config['port']}/{tool_name}/sse"
                }
            
            # 打印工具服务器配置
            logger.info("工具服务器配置（包含全部工具）:")
            logger.info("-"*30)
            logger.info(json.dumps(tools_config, indent=2, ensure_ascii=False))
            logger.info("-"*30)
        
        logger.info("提示: 可以复制以上 JSON 配置到 Cursor 的 MCP 配置文件中")
        logger.info("      - 默认配置路径: ~/.cursor/mcp.json")
        
    async def cleanup(self) -> None:
        """清理服务器资源"""
        logger.info("正在清理服务器资源...")
        
        for tool_name, tool in self.tools.items():
            try:
                await tool.cleanup()
                logger.info(f"工具资源清理完成: {tool_name}")
            except Exception as e:
                logger.error(f"工具资源清理失败: {tool_name}, 错误: {str(e)}", exc_info=True)
                
        logger.info("服务器资源清理完成") 