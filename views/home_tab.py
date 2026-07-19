from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from core.app_info import APP_NAME, APP_VERSION_DISPLAY


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel(f"🛠️ {APP_NAME}")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Minecraft 实用工具箱")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        version = QLabel(f"版本 {APP_VERSION_DISPLAY}")
        version.setStyleSheet("font-size: 12px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        separator = QLabel("─" * 50)
        separator.setStyleSheet("color: lightgray; font-size: 12px;")
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(separator)

        features_layout = QVBoxLayout()
        features_layout.setSpacing(8)

        features = ["⚙️  一键配置 Minecraft 相关选项", "🔧  提供多种实用的辅助功能"]

        for feature in features:
            label = QLabel(feature)
            label.setStyleSheet("font-size: 13px; padding: 5px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            features_layout.addWidget(label)

        layout.addLayout(features_layout)

        layout.addStretch()

        note = QLabel("💡 从上方选项卡选择你需要的功能开始使用")
        note.setStyleSheet("font-size: 12px; color: gray;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True)
        layout.addWidget(note)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        button_layout.addStretch()

        self.start_button = QPushButton("开始使用")
        self.start_button.setMinimumWidth(100)
        button_layout.addWidget(self.start_button)

        self.help_button = QPushButton("查看帮助")
        self.help_button.setMinimumWidth(100)
        button_layout.addWidget(self.help_button)

        button_layout.addStretch()

        layout.addLayout(button_layout)
