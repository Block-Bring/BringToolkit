from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class FeaturesTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("🔧 功能列表")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("QFrame { max-height: 1px; }")
        main_layout.addWidget(separator)

        self.functions_layout = QVBoxLayout()
        self.functions_layout.setSpacing(12)
        self._add_function_cards()

        main_layout.addLayout(self.functions_layout)
        main_layout.addStretch()

    def _add_function_cards(self):
        card = self._create_function_card(
            icon="📦",
            title="Bring Craft 个性化数据迁移",
            description="将旧版本整合包的个性化配置、存档等数据迁移到新版本",
            button_text="开始迁移",
            on_click=self._on_bring_craft_migrate,
        )
        self.functions_layout.addWidget(card)

    def _create_function_card(self, icon, title, description, button_text, on_click):
        card = QFrame()
        card.setObjectName("func_card")
        card.setStyleSheet("""
            QFrame#func_card {
                border: 1px solid palette(midlight);
                border-radius: 10px;
            }
            QFrame#func_card:hover {
                border: 1px solid #4CAF50;
            }
        """)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(16)

        # 图标
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px; border: none;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedWidth(56)
        card_layout.addWidget(icon_label)

        # 文字区域
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 15px; font-weight: bold; border: none;")
        text_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 12px; border: none;")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)

        card_layout.addLayout(text_layout, 1)

        # 按钮
        action_button = QPushButton(button_text)
        action_button.setCursor(Qt.CursorShape.PointingHandCursor)
        action_button.setFixedHeight(36)
        action_button.setMinimumWidth(100)
        action_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        action_button.clicked.connect(on_click)
        card_layout.addWidget(action_button)

        return card

    def _on_bring_craft_migrate(self):
        from features.migrator.window import MigratorWindow

        dialog = MigratorWindow(self)
        dialog.exec()
