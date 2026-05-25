from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt
from core.app_info import APP_NAME, APP_VERSION_DISPLAY


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建主布局（垂直方向）
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # 设置边距：上下左右各20像素
        layout.setSpacing(15)  # 设置控件之间的间距为15像素
        
        # ===== 标题部分 =====
        title = QLabel(f"🛠️ {APP_NAME}")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")  # 字体大小24px，粗体
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 文字居中显示
        layout.addWidget(title)
        
        # ===== 副标题部分 =====
        subtitle = QLabel("Minecraft 实用工具箱")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")  # 灰色小字
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # ===== 版本号 =====
        version = QLabel(f"版本 {APP_VERSION_DISPLAY}")
        version.setStyleSheet("font-size: 12px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        # ===== 分隔线（使用 QLabel 模拟）=====
        separator = QLabel("─" * 50)  # 用横线字符做分隔线
        separator.setStyleSheet("color: lightgray; font-size: 12px;")
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(separator)
        
        # ===== 功能说明区域 =====
        # 创建一个垂直布局来放功能列表
        features_layout = QVBoxLayout()
        features_layout.setSpacing(8)  # 每个功能项之间的间距
        
        # 功能列表（使用简单的 QLabel）
        features = [
            "⚙️  一键配置 Minecraft 相关选项",
            "🔧  提供多种实用的辅助功能"
        ]
        
        # 遍历功能列表，创建每个功能项
        for feature in features:
            label = QLabel(feature)
            label.setStyleSheet("font-size: 13px; padding: 5px;")  # 设置字体和内边距
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
            features_layout.addWidget(label)
        
        # 将功能列表添加到主布局
        layout.addLayout(features_layout)
        
        # ===== 弹簧，把下面内容推到底部 =====
        layout.addStretch()
        
        # ===== 底部提示文字 =====
        note = QLabel("💡 从上方选项卡选择你需要的功能开始使用")
        note.setStyleSheet("font-size: 12px; color: gray;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True)  # 允许文字自动换行
        layout.addWidget(note)
        
        # ===== 底部按钮区域 =====
        # 创建水平布局来放置按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # 按钮之间的间距
        
        # 添加弹簧，让按钮居中
        button_layout.addStretch()
        
        # 主要按钮：开始使用
        self.start_button = QPushButton("开始使用")
        self.start_button.setMinimumWidth(100)  # 设置最小宽度
        button_layout.addWidget(self.start_button)
        
        # 次要按钮：查看帮助
        self.help_button = QPushButton("查看帮助")
        self.help_button.setMinimumWidth(100)
        button_layout.addWidget(self.help_button)
        
        # 再添加弹簧，让按钮居中
        button_layout.addStretch()
        
        # 将按钮布局添加到主布局
        layout.addLayout(button_layout)