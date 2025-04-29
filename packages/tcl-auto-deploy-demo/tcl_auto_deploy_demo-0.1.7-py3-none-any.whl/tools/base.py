"""
MCP 工具基类
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import logging
from core.utils import RequestTimer

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """MCP 工具基类"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化工具
        
        Args:
            config: 工具配置
        """
        self.config = config
        self.name = self.__class__.__name__
        logger.info(f"初始化工具: {self.name}")
    
    @abstractmethod
    async def initialize(self) -> None:
        """初始化工具，在服务启动时调用"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """清理工具资源，在服务关闭时调用"""
        pass
    
    def get_tool_info(self) -> Dict[str, Any]:
        """获取工具信息
        
        Returns:
            包含工具信息的字典
        """
        return {
            "name": self.name,
            "description": self.__doc__,
            "methods": self._get_tool_methods()
        }
    #下划线开头的是私有/内部方法
    def _get_tool_methods(self) -> Dict[str, Any]:
        """获取工具的所有可用方法
        
        Returns:
            包含方法信息的字典
        """
        methods = {}
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, '_is_tool_method'):
                methods[attr_name] = {
                    "description": attr.__doc__,
                    "parameters": getattr(attr, '_parameters', {}),
                    "returns": getattr(attr, '_returns', None)
                }
        return methods

def tool_method(description: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None):
    """工具方法装饰器
    
    Args:
        description: 方法描述
        parameters: 参数说明
    """
    def decorator(func):
        func._is_tool_method = True
        func._description = description
        func._parameters = parameters or {}
        return func
    return decorator 