"""
MCP 服务器 stdio 模式入口点
"""
import asyncio
import sys
import logging
from typing import Any, Dict
from mcp.server.stdio import stdio_server
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Prompt
from config import settings
from core.utils import load_tool

# 配置日志
logging.basicConfig(**settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# 创建 FastMCP 实例
mcp = FastMCP("Personal MCP Service")
        
# 加载工具
tools: Dict[str, Any] = {}
async def initialize():
    """stdio 模式主函数"""
    try:
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
                            # 提取 prompt 信息
                            method_prompt = method_info['prompt']
                                
                            mcp.add_tool(
                                fn=method,
                                name=method_name,
                                description=method_description
                            )
                            prompt = Prompt(fn=method,name=method_name,description=method_prompt,arguments=[])
                            mcp.add_prompt(
                                prompt=prompt
                            )
                except Exception as e:
                    logger.error(f"加载工具失败: {tool_name}, 错误: {str(e)}", exc_info=True)
                    continue
           
    except Exception as e:
        logger.error(f"stdio 模式运行失败: {str(e)}", exc_info=True)
        sys.exit(1)
    



def main():
    try:
        asyncio.run(initialize())
        asyncio.run(mcp.run(transport='stdio'))
    except Exception as e:
        logger.error(f"运行失败: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        # 清理资源
        for tool in tools.values():
            try:
                tool.cleanup()
            except Exception as e:
                logger.error(f"工具清理失败: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()