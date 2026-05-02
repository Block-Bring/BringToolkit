"""
检查更新模块
从 GitHub 上的 latest/app_latest.json 获取最新版本信息，
与本地 APP_VERSION 比较，判断是否需要更新。
"""
import requests
import webbrowser
from ZJCore import show_error, ask_yes_no
from core.app_info import APP_VERSION

# 线上存放最新版本信息的 JSON 文件地址（你的 GitHub 仓库的 raw 地址）
UPDATE_URL = (
    "https://raw.githubusercontent.com/Block-Bring/BringToolkit/"
    "refs/heads/master/latest/app_latest.json"
)


def check_for_updates():
    """
    联网检查是否有新版本。

    返回值：
        True  - 有新版本可用
        False - 当前已是最新版本
        None  - 检查失败（例如无网络连接、服务器不可达等）
    """
    print(f"正在检查更新... 当前版本：{APP_VERSION}")

    try:
        # 1. 发送 GET 请求，获取线上 JSON
        response = requests.get(UPDATE_URL, timeout=10)

        # 2. 如果 HTTP 状态码不是 200，说明请求失败
        if response.status_code != 200:
            print(f"检查更新失败：HTTP {response.status_code}")
            return None

        # 3. 将返回内容解析为 Python 字典
        data = response.json()
        online_version = data.get("version")
        url = data.get("url")

        # 4. 如果 JSON 里没有 version 字段，说明数据格式有误
        if not online_version:
            print("检查更新失败：线上数据中没有找到 version 字段")
            show_error("检查更新失败", "线上数据中没有找到 version 字段")
            return None

        print(f"线上版本：{online_version}")

        # 5. 比较版本号（简单比较：不一样就算有新版本）
        if online_version != APP_VERSION:
            print("发现新版本！")
            question = ask_yes_no("发现新版本", f"当前所获取到的最新版本为 {online_version}\n是否更新？")
            if question:
                webbrowser.open(url)
            return True
        else:
            print("已是最新版本。")
            return False

    except requests.exceptions.RequestException as e:
        # 网络问题、超时等都会走到这里
        print(f"检查更新失败：网络错误 - {e}")
        return None