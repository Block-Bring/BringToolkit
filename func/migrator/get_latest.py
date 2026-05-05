import os
import requests
from core.app_info import FUNC_DATA_DIR
from tools.ZJTools import show_error

data_directory = os.path.join(FUNC_DATA_DIR, "migrator")

def requests_latest_migrate_file():
    """
    请求最新的迁移文件
    """
    try:
        response = requests.get("https://ghfast.top/github.com/Block-Bring/BringToolkit/raw/refs/heads/master/latest/migrate_latest.json")
        if response.status_code == 200:
            return response.json()
        else:
            show_error("错误", "无法获取最新版本信息")
    except:
        show_error("错误", "无法连接服务器")

def create_data_directory():
    """
    创建功能目录
    """
    try:
        os.makedirs(data_directory, exist_ok=True)
    except:
        show_error("严重错误", "无法创建功能目录")
    return
