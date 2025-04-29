"""
时间查询工具
@author: guohao.cheng
"""
from datetime import datetime
from typing import Dict, Any, Annotated
from tools.base import BaseTool, tool_method
from pydantic import Field
import logging

logger = logging.getLogger(__name__)



class TimeQueryTool(BaseTool):
    """时间查询工具"""
    
    async def initialize(self) -> None:
        """初始化工具"""
        logger.info("初始化时间查询工具")


    async def cleanup(self) -> None:
        """清理资源"""
        logger.info("清理时间查询工具资源")
        
    @tool_method(description="查询当前时间")
    async def query_current_time(self) -> Dict[str, Any]:
        """查询当前时间
        
        Returns:
            Dict[str, Any]: 包含当前时间信息的字典，包括：
                - timestamp: 时间戳
                - formatted: 格式化的时间字符串 (格式：YYYY-MM-DD HH:mm:ss)
        """
        now = datetime.now()
        
        return {
            "timestamp": now.timestamp(),
            "formatted": now.strftime("%Y-%m-%d %H:%M:%S")
        } 