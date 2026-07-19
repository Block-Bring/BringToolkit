import os

import requests

from core.app_info import FEATURES_DATA_DIR, GITHUB_RAW_BASE
from utils.nana_tools import show_error

MIGRATE_LATEST_URL = f"{GITHUB_RAW_BASE}/latest/func/migrate_latest.json"
data_directory = os.path.join(FEATURES_DATA_DIR, "migrator")


def requests_latest_migrate_file():
    """请求最新的迁移配置文件"""
    try:
        response = requests.get(MIGRATE_LATEST_URL)
        if response.status_code == 200:
            return response.json()
        else:
            show_error("错误", "无法获取最新版本信息")
    except Exception:
        show_error("错误", "无法连接服务器")


def create_data_directory():
    """创建功能目录"""
    try:
        os.makedirs(data_directory, exist_ok=True)
    except Exception:
        show_error("严重错误", "无法创建功能目录")
