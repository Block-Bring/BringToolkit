"""
关于页面
"""

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from core.app_info import APP_NAME, APP_VERSION_DISPLAY, GITHUB_REPO
from utils.style import GITHUB_BUTTON
from views.base_tab import BaseTab


class AboutTab(BaseTab):
    def __init__(self):
        super().__init__()
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        logo_label = QLabel("🛠️")
        logo_label.setStyleSheet("font-size: 48px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(logo_label)

        name_label = QLabel(APP_NAME)
        name_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(name_label)

        version_label = QLabel(f"版本 {APP_VERSION_DISPLAY}")
        version_label.setStyleSheet("font-size: 14px; color: gray;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(version_label)

        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setStyleSheet("color: #e0e0e0;")
        self.main_layout.addWidget(separator1)

        dev_title = QLabel("开发团队")
        dev_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        dev_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(dev_title)

        dev_label = QLabel("QuickYeah Studio")
        dev_label.setStyleSheet("font-size: 14px; color: #3498db;")
        dev_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(dev_label)

        license_title = QLabel("开源许可证")
        license_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        license_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(license_title)

        license_label = QLabel("MIT License")
        license_label.setStyleSheet("font-size: 14px; color: #27ae60;")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(license_label)

        license_desc = QLabel("本软件基于 MIT 许可证开源，你可以自由使用、修改和分发。")
        license_desc.setStyleSheet("font-size: 12px; color: gray;")
        license_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        license_desc.setWordWrap(True)
        self.main_layout.addWidget(license_desc)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("color: #e0e0e0;")
        self.main_layout.addWidget(separator2)

        github_label = QLabel("访问我们的 GitHub 仓库")
        github_label.setStyleSheet("font-size: 14px; color: gray; margin-top: 10px;")
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(github_label)

        github_btn = QPushButton("📦 查看源代码")
        github_btn.setStyleSheet(GITHUB_BUTTON)
        github_btn.setMinimumHeight(40)
        github_btn.clicked.connect(self._open_github)  # type: ignore[attr-defined]

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(github_btn)
        btn_layout.addStretch()
        self.main_layout.addLayout(btn_layout)

        self.main_layout.addStretch()

        copyright_label = QLabel("© 2026 QuickYeah Studio. All rights reserved.")
        copyright_label.setStyleSheet("font-size: 11px; color: lightgray;")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(copyright_label)

    def _open_github(self):
        QDesktopServices.openUrl(QUrl(GITHUB_REPO))
