"""
日志模块 - 同时写入文件和控制台
"""
from datetime import datetime
from core.app_info import LATEST_LOG_PATH


class Logger:
    """简单的日志记录器"""

    _COLORS = {
        'INFO': '\033[92m',      # 绿色
        'WARNING': '\033[93m',   # 金黄色
        'ERROR': '\033[91m',     # 红色
        'DEBUG': '\033[96m',     # 青色
    }

    def __init__(self, log_file=None):
        self.log_file = log_file or LATEST_LOG_PATH

    def _write(self, level, message, color, to_console):
        """统一写入文件（可选打印到控制台加颜色）"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
        except Exception as e:
            print(f"写入日志文件失败: {e}")

        if to_console:
            print(f"[{timestamp}] {color}[{level}]\033[0m {message}")

    def info(self, message, to_console=True):
        self._write('INFO', message, self._COLORS['INFO'], to_console)

    def warning(self, message, to_console=True):
        self._write('WARNING', message, self._COLORS['WARNING'], to_console)

    def error(self, message, to_console=True):
        self._write('ERROR', message, self._COLORS['ERROR'], to_console)

    def debug(self, message, to_console=False):
        self._write('DEBUG', message, self._COLORS['DEBUG'], to_console)


logger = Logger()
