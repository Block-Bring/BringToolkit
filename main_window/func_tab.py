from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from core.logger import logger


class FuncTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # ===== 标题 =====
        title_label = QLabel("🔧 功能列表")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # ===== 分隔线 =====
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: lightgray;")
        main_layout.addWidget(separator)
        
        # ===== 功能卡片列表 =====
        self.functions_layout = QVBoxLayout()
        self.functions_layout.setSpacing(10)
        
        # 添加功能卡片
        self._add_function_cards()
        
        main_layout.addLayout(self.functions_layout)
        main_layout.addStretch()  # 弹簧，把内容推到顶部
    
    def _add_function_cards(self):
        """添加功能卡片"""
        
        # 功能 1: Bring Craft 个性化数据迁移
        card1 = self._create_function_card(
            icon="📦",
            title="Bring Craft 个性化数据迁移",
            description="将旧版本整合包的个性化配置、存档等数据迁移到新版本",
            button_text="开始迁移",
            on_click=self._on_bring_craft_migrate
        )
        self.functions_layout.addWidget(card1)
    
    def _create_function_card(self, icon, title, description, button_text, on_click):
        """
        创建一个功能卡片
        
        参数:
            icon: 图标 emoji
            title: 功能标题
            description: 功能描述
            button_text: 按钮文字
            on_click: 点击按钮的回调函数
        """
        # 创建卡片容器
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
            QFrame:hover {
                border: 1px solid #4CAF50;
                background-color: rgba(76, 175, 80, 0.1);
            }
        """)
        
        # 创建卡片布局
        card_layout = QHBoxLayout(card)
        card_layout.setSpacing(15)
        
        # 图标
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedWidth(100)
        card_layout.addWidget(icon_label)
        
        # 文字区域
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        text_layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 12px;")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)
        
        card_layout.addLayout(text_layout)
        
        # 弹簧
        card_layout.addStretch()
        
        # 按钮
        action_button = QPushButton(button_text)
        action_button.setMinimumWidth(100)
        action_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        action_button.clicked.connect(on_click)
        card_layout.addWidget(action_button)
        
        return card
    
    def _on_bring_craft_migrate(self):
        """Bring Craft 数据迁移按钮点击事件"""
        # TODO: 实现迁移功能
        logger.info("开始 Bring Craft 个性化数据迁移...")