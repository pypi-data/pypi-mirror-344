"""
MCP 服务器 stdio 模式入口点
"""
import asyncio
import sys
import logging
from typing import Any, Dict
from mcp.server.stdio import stdio_server
from mcp.server.fastmcp import FastMCP

from config import settings
from core.utils import load_tool

# 配置日志
logging.basicConfig(**settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

async def main_stdio():
    """stdio 模式主函数"""
    try:
        # 创建 FastMCP 实例
        mcp = FastMCP("Personal MCP Service")
        
        # 加载工具
        tools: Dict[str, Any] = {}
        for tool_name, tool_config in settings.TOOLS_CONFIG.items():
            if tool_config.get("enabled", False):
                try:
                    tool = load_tool(tool_config)
                    if tool:
                        await tool.initialize()
                        tools[tool_name] = tool
                        
                        # 注册工具方法
                        for method_name, method_info in tool.get_tool_info()['methods'].items():
                            method = getattr(tool, method_name)
                            method_description = ""
                            if 'description' in method_info and method_info['description']:
                                method_description += method_info['description']
                            elif method.__doc__:
                                method_description += method.__doc__
                                
                            mcp.add_tool(
                                fn=method,
                                name=method_name,
                                description=method_description
                            )
                except Exception as e:
                    logger.error(f"加载工具失败: {tool_name}, 错误: {str(e)}", exc_info=True)
                    continue
        
        # 使用 stdio 传输
        async with stdio_server() as (read_stream, write_stream):
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                mcp._mcp_server.create_initialization_options()
            )
        
    except Exception as e:
        logger.error(f"stdio 模式运行失败: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        # 清理资源
        for tool in tools.values():
            try:
                await tool.cleanup()
            except Exception as e:
                logger.error(f"工具清理失败: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main_stdio()) 