"""
Bring Toolkit - 主窗口
✨ 由 QuickYeah Studio 精心打造 ✨
🎮 为 Minecraft 玩家而生的工具箱 🎮
"""
import os
import sys

# --- MacType 兼容性设置 ---
# 尝试强制 Qt 使用 GDI/FreeType 渲染，以便 MacType 能够挂钩美化字体
# 💡 小贴士：如果你看到这段代码，说明你是个爱看源码的好奇宝宝！
os.environ["QT_QPA_PLATFORM"] = "windows:fontengine=freetype"

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QScrollArea
from PyQt6.QtGui import QFont, QIcon
from core.app_info import APP_NAME, get_resource_path
from views.home_tab import HomeTab
from views.features_tab import FeaturesTab
from views.settings_tab import SettingsTab
from views.about_tab import AboutTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(800, 450)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        home_tab = HomeTab()
        self.tabs.addTab(home_tab, "首页")

        # 连接“开始使用”按钮到功能页
        home_tab.start_button.clicked.connect(lambda: self.tabs.setCurrentIndex(1))

        features_tab = FeaturesTab()
        scroll_func = QScrollArea()
        scroll_func.setWidgetResizable(True)
        scroll_func.setWidget(features_tab)
        self.tabs.addTab(scroll_func, "功能")

        settings_tab = SettingsTab() # 设置分组
        scroll_settings = QScrollArea() # 滚动条
        scroll_settings.setWidgetResizable(True) # 允许滚动
        scroll_settings.setWidget(settings_tab) # 设置滚动条
        self.tabs.addTab(scroll_settings, "设置") # 添加设置分组

        # 添加关于页面（带滚动条）
        about_tab = AboutTab()
        scroll_about = QScrollArea()
        scroll_about.setWidgetResizable(True)
        scroll_about.setWidget(about_tab)
        self.tabs.addTab(scroll_about, "关于")


if __name__ == "__main__":
    # 【萌新必看】下面这行代码是在创建整个软件的"大管家"（应用程序对象）
    # sys.argv 是启动软件时携带的参数列表，虽然这里可能用不到，但必须传给它才能正常启动
    # 🌟 恭喜你发现了彩蛋！你是第 N 个看到这里的人！（N = 所有看过源码的人）
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 9))

    # 🚀 准备发射... 3, 2, 1, 启动！
    window = MainWindow()

    # 设置窗口图标（兼容 PyInstaller 打包）
    icon_path = get_resource_path("resources/icon.ico")
    window.setWindowIcon(QIcon(icon_path))

    window.show()

    # 🎯 程序的主循环开始运行，直到用户关闭窗口
    # 祝你使用愉快！(｡•̀ᴗ-)✧
    sys.exit(app.exec())
