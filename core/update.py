"""
检查更新模块
从 GitHub 上的 latest/app_latest.json 获取最新版本信息，
与本地 APP_VERSION 比较，判断是否需要更新。
"""
import requests
import webbrowser
from core.app_info import APP_VERSION, APP_NAME


UPDATE_URL = (
    "https://raw.githubusercontent.com/Block-Bring/BringToolkit/"
    "refs/heads/master/latest/app_latest.json"
)


def check_for_updates():
    """
    联网检查是否有新版本（仅执行检查逻辑，不显示任何 UI）。

    返回值：
        dict - 包含更新信息的字典：
            {
                "has_update": bool,  # 是否有新版本
                "online_version": str or None,  # 线上版本号
                "url": str or None,  # 下载链接
                "error": str or None  # 错误信息
            }
    """
    print(f"正在检查更新... 当前版本：{APP_VERSION}")

    result = {
        "has_update": False,
        "online_version": None,
        "url": None,
        "error": None
    }

    try:
        response = requests.get(UPDATE_URL, timeout=10)

        if response.status_code != 200:
            error_msg = f"HTTP {response.status_code}"
            print(f"检查更新失败：{error_msg}")
            result["error"] = error_msg
            return result

        data = response.json()
        online_version = data.get("version")
        url = data.get("url")

        if not online_version:
            error_msg = "线上数据中没有找到 version 字段"
            print(f"检查更新失败：{error_msg}")
            result["error"] = error_msg
            return result

        print(f"线上版本：{online_version}")
        result["online_version"] = online_version
        result["url"] = url

        if online_version != APP_VERSION:
            print("发现新版本！")
            result["has_update"] = True
        else:
            print("已是最新版本。")

        return result

    except requests.exceptions.RequestException as e:
        error_msg = f"网络错误 - {e}"
        print(f"检查更新失败：{error_msg}")
        result["error"] = error_msg
        return result
