"""
下载和网络请求工具模块
"""

import requests
from PyQt6.QtCore import QThread, pyqtSignal

from utils.logger import logger


class DownloadWorker(QThread):
    """后台文件下载线程，支持进度回调"""

    progress_signal = pyqtSignal(int, int, int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            logger.info(f"开始下载: {self.url}")
            response = requests.get(self.url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(self.save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percentage = int((downloaded / total_size) * 100) if total_size > 0 else 0
                        self.progress_signal.emit(downloaded, total_size, percentage)

            logger.info("下载完成")
            self.finished_signal.emit(self.save_path)

        except Exception as e:
            logger.error(f"下载失败: {e}")
            self.error_signal.emit(f"下载失败: {e}")


def fetch_json(url, timeout=10):
    """
    发起 GET 请求并返回 JSON 数据。

    返回 (data, error) 元组：
    - 成功时 data 为解析后的 JSON，error 为 None
    - 404 时 error 为 ``"not_found"``
    - 其他 HTTP 错误时 error 为 ``"HTTP {status_code}"``
    - 网络异常时 error 为 ``"网络错误 - {详细信息}"``
    - 其他异常时 error 为 ``"未知错误 - {详细信息}"``
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return None, "not_found"
        status = e.response.status_code if e.response is not None else "unknown"
        return None, f"HTTP {status}"
    except requests.exceptions.RequestException as e:
        return None, f"网络错误 - {e}"
    except Exception as e:
        return None, f"未知错误 - {e}"
