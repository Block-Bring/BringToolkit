"""标签页基类 - 统一页面布局"""

from PyQt6.QtWidgets import QVBoxLayout, QWidget


class BaseTab(QWidget):
    """所有标签页的基类，提供统一的页面布局"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
