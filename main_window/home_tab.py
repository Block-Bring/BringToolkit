from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt
from core.app_info import APP_NAME, APP_VERSION


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)  # 创建垂直布局

        # 标题部分
        title = QLabel(f"🛠️ {APP_NAME}")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 副标题部分
        subtitle = QLabel("Minecraft 实用工具箱")
        subtitle.setStyleSheet("font-size: 14px; color: gray; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # 版本号
        version = QLabel(f"版本 {APP_VERSION}")
        version.setStyleSheet("font-size: 12px; margin-bottom: 15px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        # 说明文字
        note = QLabel("欢迎使用，请从上方选项卡选择需要的功能。")
        note.setStyleSheet("font-size: 12px; color: gray;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True)
        layout.addWidget(note)

        # 弹簧，把上面所有内容推到顶部
        layout.addStretch()

        # 底部水平布局，放一个按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.start_button = QPushButton("开始使用")
        button_layout.addWidget(self.start_button)
        layout.addLayout(button_layout)