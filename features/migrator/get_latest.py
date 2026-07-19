import os

from core.app_info import FEATURES_DATA_DIR, GITHUB_RAW_BASE
from utils.downloader import fetch_json
from utils.nana_tools import show_error

MIGRATE_LATEST_URL = f"{GITHUB_RAW_BASE}/latest/func/migrate_latest.json"
data_directory = os.path.join(FEATURES_DATA_DIR, "migrator")


def requests_latest_migrate_file():
    """请求最新的迁移配置文件"""
    data, error = fetch_json(MIGRATE_LATEST_URL)
    if error:
        show_error("错误", "无法获取最新版本信息")
        return None
    return data


def create_data_directory():
    """创建功能目录"""
    try:
        os.makedirs(data_directory, exist_ok=True)
    except Exception:
        show_error("严重错误", "无法创建功能目录")
