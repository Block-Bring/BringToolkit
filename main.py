"""
Bring Toolkit - 主窗口
"""

import os
import sys

# MacType 兼容：强制 Qt 使用 FreeType 字体渲染引擎
os.environ["QT_QPA_PLATFORM"] = "windows:fontengine=freetype"

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea, QTabWidget

from core.app_info import APP_NAME, get_resource_path
from views.about_tab import AboutTab
from views.features_tab import FeaturesTab
from views.home_tab import HomeTab
from views.settings_tab import SettingsTab


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
        scroll_features = QScrollArea()
        scroll_features.setWidgetResizable(True)
        scroll_features.setWidget(features_tab)
        self.tabs.addTab(scroll_features, "功能")

        settings_tab = SettingsTab()
        scroll_settings = QScrollArea()
        scroll_settings.setWidgetResizable(True)
        scroll_settings.setWidget(settings_tab)
        self.tabs.addTab(scroll_settings, "设置")

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

    # 设置窗口图标（兼容 PyInstaller 打包路径）
    icon_path = get_resource_path("resources/icon.ico")
    window.setWindowIcon(QIcon(icon_path))

    window.show()

    sys.exit(app.exec())
