"""
应用信息模块
包含应用基本信息、版本管理、路径配置等
"""
import os
import re
import sys


# ===== 应用基本信息 =====
APP_NAME = "Bring Toolkit"
APP_VERSION = "1.0.0a5"  # 内部版本号，用于比较和存储
GITHUB_REPO = "https://github.com/Block-Bring/BringToolkit"  # GitHub 仓库地址


# ===== 版本号格式化 =====
def format_version_display(version: str) -> str:
    """
    将内部版本号转换为友好地显示格式

    例如:
        1.0.0a1   -> 1.0.0 Alpha 1
        1.0.0b2   -> 1.0.0 Beta 2
        1.0.0rc3  -> 1.0.0 RC 3
        1.0.0     -> 1.0.0

    参数:
        version: 内部版本号字符串

    返回:
        格式化后的版本号字符串
    """
    # 匹配版本号模式：主版本号 + 预发布类型 + 预发布编号
    pattern = r'^(\d+\.\d+\.\d+)(a|alpha|b|beta|rc|preview)(\d+)$'
    match = re.match(pattern, version, re.IGNORECASE)

    if match:
        base_version = match.group(1)  # 主版本号 (如 1.0.0)
        pre_type = match.group(2).lower()  # 预发布类型
        pre_num = match.group(3)  # 预发布编号

        # 转换预发布类型为友好名称
        type_map = {
            'a': 'Alpha',
            'alpha': 'Alpha',
            'b': 'Beta',
            'beta': 'Beta',
            'rc': 'RC',
            'preview': 'Preview'
        }

        friendly_type = type_map.get(pre_type, pre_type)
        return f"{base_version} {friendly_type} {pre_num}"
    else:
        # 如果不是预发布版本，直接返回
        return version


# 初始化显示版本号
APP_VERSION_DISPLAY = format_version_display(APP_VERSION)


# ===== 路径配置 =====
# 程序数据目录（自动创建）
if getattr(sys, 'frozen', False):
    # PyInstaller 打包环境：使用 exe 所在目录下的 BringToolkit 文件夹
    APP_DATA_DIR = os.path.join(os.path.dirname(sys.executable), "BringToolkit")
else:
    # 开发环境：使用项目根目录下的 data 文件夹
    APP_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# 自动创建数据目录（带错误处理）
try:
    os.makedirs(APP_DATA_DIR, exist_ok=True)
except Exception as e:
    from PyQt6.QtWidgets import QMessageBox, QApplication
    from utils.nana_tools import show_error
    app = QApplication.instance() or QApplication(sys.argv)
    show_error("严重错误", f"无法创建程序工作目录：{e}")
    sys.exit(1)

# 配置文件路径
CONFIG_PATH = os.path.join(APP_DATA_DIR, "config.json")
LATEST_LOG_PATH = os.path.join(APP_DATA_DIR, "latest.log")
RESOURCES_DIR = "resources"  # 资源目录名称

# 功能数据目录（自动创建）
FEATURES_DATA_DIR = os.path.join(APP_DATA_DIR, "features_data")
os.makedirs(FEATURES_DATA_DIR, exist_ok=True)


# ===== 资源路径工具 =====
def get_resource_path(relative_path: str) -> str:
    """
    获取资源文件的绝对路径（兼容 PyInstaller 打包）

    开发环境：返回项目根目录下的资源路径
    打包环境：返回 PyInstaller 临时解压目录下的资源路径

    参数:
        relative_path: 相对于项目根目录或 resources 目录的路径

    返回:
        资源文件的绝对路径

    示例:
        # 获取 resources/icon.ico
        icon_path = get_resource_path("resources/icon.ico")

        # 或者如果 RESOURCES_DIR 已设置
        icon_path = get_resource_path("icon.ico")
    """
    # PyInstaller 打包后的临时目录
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # 开发环境：使用项目根目录
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 构建完整路径
    full_path = os.path.join(base_path, relative_path)

    # 如果文件不存在，尝试从 resources 目录查找
    if not os.path.exists(full_path):
        resources_path = os.path.join(base_path, RESOURCES_DIR, os.path.basename(relative_path))
        if os.path.exists(resources_path):
            return resources_path

    return full_path
