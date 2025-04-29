"""
MCP 服务器主入口
"""
import asyncio
import logging
import traceback
import uvicorn
from config import settings
from core.server import MCPServer

# 配置日志
logging.basicConfig(**settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

async def main():
    """主函数"""
    mcp_server = None
    try:
        logger.info("===== 开始启动 MCP 服务器 =====")
        logger.info("正在创建 MCPServer 实例...")
        mcp_server = MCPServer()
        logger.info("MCPServer 实例创建完成，准备初始化...")
        
        try:
            # 初始化服务器
            logger.info("正在调用 MCPServer.initialize() 方法...")
            await mcp_server.initialize()
            logger.info("MCPServer.initialize() 方法调用完成")
        except Exception as init_error:
            logger.error(f"MCPServer 初始化失败: {str(init_error)}")
            logger.error(f"初始化错误详细堆栈: {traceback.format_exc()}")
            raise
        
        # 打印服务器信息
        logger.info("正在打印服务器信息...")
        mcp_server.print_server_info()
        
        # 创建并启动服务器
        logger.info("正在创建应用...")
        app = mcp_server.create_app()
        
        logger.info("配置 uvicorn 服务器...")
        config = uvicorn.Config(
            app=app,
            host=settings.SERVER_CONFIG['host'],
            port=settings.SERVER_CONFIG['port'],
            log_level="debug",
            loop="auto",
            workers=1,
            timeout_keep_alive=5,
            timeout_graceful_shutdown=10
        )
        
        logger.info("创建 uvicorn 服务器实例...")
        uvicorn_server = uvicorn.Server(config)
        
        logger.info("启动 uvicorn 服务器...")
        await uvicorn_server.serve()
        logger.info("服务器已关闭")
        
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}", exc_info=True)
        logger.error(f"详细错误堆栈: {traceback.format_exc()}")
        raise
    finally:
        logger.info("正在进行清理工作...")
        if mcp_server:
            try:
                await mcp_server.cleanup()
                logger.info("服务器资源已清理")
            except Exception as cleanup_error:
                logger.error(f"清理资源时出错: {str(cleanup_error)}", exc_info=True)
        logger.info("===== MCP 服务器结束 =====")

if __name__ == "__main__":
    logger.info("===== MCP 服务器程序开始 =====")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"程序异常终止: {str(e)}")
        logger.error(f"详细错误堆栈: {traceback.format_exc()}")
    logger.info("===== MCP 服务器程序结束 =====") 