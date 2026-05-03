"""
Bring Toolkit - 主窗口
"""
import os
import sys

# --- MacType 兼容性设置 ---
# 尝试强制 Qt 使用 GDI/FreeType 渲染，以便 MacType 能够挂钩美化字体
os.environ["QT_QPA_PLATFORM"] = "windows:fontengine=freetype"

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QScrollArea
from PyQt6.QtGui import QFont
from core.app_info import APP_NAME
from main_window.home_tab import HomeTab
from main_window.func_tab import FuncTab
from main_window.settings_tab import SettingsTab
from main_window.about_tab import AboutTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(800, 500)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(HomeTab(), "首页")
        self.tabs.addTab(FuncTab(), "功能")

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
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 9))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())