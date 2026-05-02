"""
Bring Toolkit - 主窗口
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QScrollArea
from PyQt6.QtGui import QFont
from core.app_info import APP_NAME
from main_window.home_tab import HomeTab
from main_window.func_tab import FuncTab
from main_window.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(600, 300)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(HomeTab(), "首页")
        self.tabs.addTab(FuncTab(), "功能")

        settings_tab = SettingsTab() # 设置分组
        scroll_settings = QScrollArea() # 滚动条
        scroll_settings.setWidgetResizable(True) # 允许滚动
        scroll_settings.setWidget(settings_tab) # 设置滚动条
        self.tabs.addTab(scroll_settings, "设置") # 添加设置分组


if __name__ == "__main__":
    # 【萌新必看】下面这行代码是在创建整个软件的“大管家”（应用程序对象）
    # sys.argv 是启动软件时携带的参数列表，虽然这里可能用不到，但必须传给它才能正常启动
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 9))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())