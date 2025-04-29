"""
通用工具类
"""
import time
import logging
from typing import Any, Optional, Dict
import importlib

logger = logging.getLogger(__name__)

class RequestTimer:
    """请求计时器，用于记录请求处理时间"""
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"开始处理请求: {self.name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        if exc_type:
            logger.error(f"请求处理失败: {self.name}, 耗时: {duration:.3f}秒, 错误: {exc_val}")
        else:
            logger.info(f"请求处理完成: {self.name}, 耗时: {duration:.3f}秒")
            
    @property
    def elapsed_ms(self) -> float:
        """获取请求耗时（毫秒）"""
        if self.start_time is None:
            return 0
        return (time.time() - self.start_time) * 1000

def load_class(module_path: str, class_name: str) -> Any:
    """动态加载类
    
    Args:
        module_path: 模块路径
        class_name: 类名
        
    Returns:
        加载的类
    """
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except Exception as e:
        logger.error(f"加载类失败 - 模块: {module_path}, 类: {class_name}, 错误: {str(e)}", exc_info=True)
        raise

def load_tool(tool_config: Dict[str, Any]) -> Optional[Any]:
    """加载工具
    
    Args:
        tool_config: 工具配置
        
    Returns:
        工具实例
    """
    try:
        if not tool_config.get('enabled', True):
            return None
            
        tool_class = load_class(tool_config['module'], tool_config['class'])
        return tool_class(tool_config)
    except Exception as e:
        logger.error(f"加载工具失败 - 配置: {tool_config}, 错误: {str(e)}", exc_info=True)
        return None 