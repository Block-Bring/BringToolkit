"""
日志模块 - 简化版日志记录器
支持同时写入文件和控制台输出
"""
import os
from datetime import datetime
from core.app_info import LATEST_LOG_PATH


class Logger:
    """简单的日志记录器"""
    
    # ANSI 颜色代码
    COLORS = {
        'INFO': '\033[92m',      # 绿色
        'WARNING': '\033[93m',   # 金黄色
        'ERROR': '\033[91m',     # 红色
        'DEBUG': '\033[96m',     # 青色
        'RESET': '\033[0m'       # 重置颜色
    }
    
    def __init__(self, log_file=None):
        """
        初始化日志记录器
        
        参数:
            log_file: 日志文件路径，默认使用 LATEST_LOG_PATH
        """
        if log_file is None:
            log_file = LATEST_LOG_PATH
        self.log_file = log_file
    
    def _format_message(self, level, message, colorize=False):
        """
        格式化日志消息
        
        参数:
            level: 日志级别
            message: 日志内容
            colorize: 是否添加颜色（仅用于控制台输出）
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}"
        
        if colorize and level in self.COLORS:
            color = self.COLORS[level]
            reset = self.COLORS['RESET']
            # 只给级别标签添加颜色
            formatted = f"[{timestamp}] {color}[{level}]{reset} {message}"
        
        return formatted
    
    def _write_to_file(self, formatted_message):
        """写入日志文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_message + '\n')
        except Exception as e:
            print(f"写入日志文件失败: {e}")
    
    def info(self, message, to_console=True):
        """
        记录信息级别日志
        
        参数:
            message: 日志内容
            to_console: 是否打印到控制台（True=是，False=否）
        """
        formatted_file = self._format_message("INFO", message, colorize=False)
        self._write_to_file(formatted_file)
        if to_console:
            formatted_console = self._format_message("INFO", message, colorize=True)
            print(formatted_console)
    
    def warning(self, message, to_console=True):
        """
        记录警告级别日志
        
        参数:
            message: 日志内容
            to_console: 是否打印到控制台
        """
        formatted_file = self._format_message("WARNING", message, colorize=False)
        self._write_to_file(formatted_file)
        if to_console:
            formatted_console = self._format_message("WARNING", message, colorize=True)
            print(formatted_console)
    
    def error(self, message, to_console=True):
        """
        记录错误级别日志
        
        参数:
            message: 日志内容
            to_console: 是否打印到控制台
        """
        formatted_file = self._format_message("ERROR", message, colorize=False)
        self._write_to_file(formatted_file)
        if to_console:
            formatted_console = self._format_message("ERROR", message, colorize=True)
            print(formatted_console)
    
    def debug(self, message, to_console=False):
        """
        记录调试级别日志（默认不打印到控制台）
        
        参数:
            message: 日志内容
            to_console: 是否打印到控制台
        """
        formatted_file = self._format_message("DEBUG", message, colorize=False)
        self._write_to_file(formatted_file)
        if to_console:
            formatted_console = self._format_message("DEBUG", message, colorize=True)
            print(formatted_console)


# 创建全局日志实例
logger = Logger()
