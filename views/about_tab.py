"""
关于页面 - 显示软件信息和开发者信息
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from core.app_info import APP_NAME, APP_VERSION_DISPLAY, GITHUB_REPO


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()

        # 创建主布局（垂直方向）
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)  # 设置边距
        layout.setSpacing(15)  # 设置间距

        # ===== Logo/图标区域（用文字代替）=====
        logo_label = QLabel("🛠️")
        logo_label.setStyleSheet("font-size: 48px;")  # 大号表情符号作为图标
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # ===== 软件名称和版本 =====
        name_label = QLabel(APP_NAME)
        name_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)

        version_label = QLabel(f"版本 {APP_VERSION_DISPLAY}")
        version_label.setStyleSheet("font-size: 14px; color: gray;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # ===== 分隔线 =====
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)  # 水平线
        separator1.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(separator1)

        # ===== 开发者信息 =====
        dev_title = QLabel("开发团队")
        dev_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        dev_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(dev_title)

        dev_label = QLabel("QuickYeah Studio")
        dev_label.setStyleSheet("font-size: 14px; color: #3498db;")
        dev_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(dev_label)

        # ===== 许可证信息 =====
        license_title = QLabel("开源许可证")
        license_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        license_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(license_title)

        license_label = QLabel("MIT License")
        license_label.setStyleSheet("font-size: 14px; color: #27ae60;")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(license_label)

        license_desc = QLabel("本软件基于 MIT 许可证开源，你可以自由使用、修改和分发。")
        license_desc.setStyleSheet("font-size: 12px; color: gray;")
        license_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        license_desc.setWordWrap(True)  # 允许换行
        layout.addWidget(license_desc)

        # ===== 分隔线 =====
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(separator2)

        # ===== GitHub 链接 =====
        github_label = QLabel("访问我们的 GitHub 仓库")
        github_label.setStyleSheet("font-size: 14px; color: gray; margin-top: 10px;")
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(github_label)

        # GitHub 按钮
        github_btn = QPushButton("📦 查看源代码")
        github_btn.setStyleSheet("""
            QPushButton {
                background-color: #24292e;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444d56;
            }
            QPushButton:pressed {
                background-color: #1a1e22;
            }
        """)
        github_btn.setMinimumHeight(40)
        github_btn.clicked.connect(self._open_github)  # type: ignore[attr-defined]

        # 将按钮居中
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(github_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # ===== 弹簧，把内容推到顶部 =====
        layout.addStretch()

        # ===== 底部版权信息 =====
        copyright_label = QLabel("© 2026 QuickYeah Studio. All rights reserved.")
        copyright_label.setStyleSheet("font-size: 11px; color: lightgray;")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)

    def _open_github(self):
        """打开 GitHub 仓库页面"""
        url = GITHUB_REPO
        QDesktopServices.openUrl(QUrl(url))
