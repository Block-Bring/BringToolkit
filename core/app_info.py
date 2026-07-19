"""
应用信息模块
"""

import os
import re
import sys

APP_NAME = "Bring Toolkit"
APP_VERSION = "1.0.0a5"
GITHUB_REPO = "https://github.com/Block-Bring/BringToolkit"
GITHUB_RAW_BASE = "https://ghfast.top/https://raw.githubusercontent.com/Block-Bring/BringToolkit/refs/heads/master"


def format_version_display(version: str) -> str:
    """1.0.0a1 → 1.0.0 Alpha 1"""
    pattern = r"^(\d+\.\d+\.\d+)(a|alpha|b|beta|rc|preview)(\d+)$"
    match = re.match(pattern, version, re.IGNORECASE)

    if match:
        type_map = {
            "a": "Alpha",
            "alpha": "Alpha",
            "b": "Beta",
            "beta": "Beta",
            "rc": "RC",
            "preview": "Preview",
        }
        friendly = type_map.get(match.group(2).lower(), match.group(2))
        return f"{match.group(1)} {friendly} {match.group(3)}"
    return version


APP_VERSION_DISPLAY = format_version_display(APP_VERSION)


# 路径配置
if getattr(sys, "frozen", False):
    APP_DATA_DIR = os.path.join(os.path.dirname(sys.executable), "BringToolkit")
else:
    APP_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

try:
    os.makedirs(APP_DATA_DIR, exist_ok=True)
except Exception as e:
    print(f"[严重错误] 无法创建程序工作目录：{e}", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = os.path.join(APP_DATA_DIR, "config.json")
LATEST_LOG_PATH = os.path.join(APP_DATA_DIR, "latest.log")
RESOURCES_DIR = "resources"

FEATURES_DATA_DIR = os.path.join(APP_DATA_DIR, "features_data")
os.makedirs(FEATURES_DATA_DIR, exist_ok=True)


def get_resource_path(relative_path: str) -> str:
    """获取资源文件绝对路径（兼容 PyInstaller）"""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        resources_path = os.path.join(base_path, RESOURCES_DIR, os.path.basename(relative_path))
        if os.path.exists(resources_path):
            return resources_path
    return full_path
