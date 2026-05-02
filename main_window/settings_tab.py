from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QCheckBox, QComboBox, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

from ZJCore import *
from core.app_info import APP_NAME
from core.update import check_for_updates


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self) # 主布局（垂直）
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        group_update = QGroupBox("软件更新")
        update_layout = QVBoxLayout() # 启动行为布局（垂直）
        group_update.setLayout(update_layout)

        # 按钮布局（水平）：将“检查更新”按钮靠左放置
        chk_btn_layout = QHBoxLayout()
        self.check_update_btn = QPushButton("检查更新")
        self.check_update_btn.clicked.connect(self._on_check_update)  # type: ignore[attr-defined]

        chk_btn_layout.addWidget(self.check_update_btn)
        chk_btn_layout.addStretch()
        update_layout.addLayout(chk_btn_layout)

        self.check_update_cb = QCheckBox("启动时检查更新")
        self.check_update_cb.setChecked(True)
        update_layout.addWidget(self.check_update_cb)

        main_layout.addWidget(group_update)

        # ----- 体验计划分组 -----
        group_insider = QGroupBox("体验计划")
        insider_layout = QVBoxLayout()
        group_insider.setLayout(insider_layout)

        self.insider_cb = QCheckBox("加入 Insider Preview 计划")
        self.insider_cb.setChecked(False)
        insider_layout.addWidget(self.insider_cb)

        # 说明文字（灰色小字）
        insider_note = QLabel("提前体验新功能，可能会遇到不稳定情况。")
        insider_note.setStyleSheet("color: gray;")
        insider_note.setWordWrap(True)
        insider_layout.addWidget(insider_note)

        main_layout.addWidget(group_insider)

        # ----- 底部按钮 -----
        # 先加一个弹簧，把按钮推到底部（如果页面高度大，按钮不会飘在中间）
        main_layout.addStretch()

        # 横盒子装按钮
        btn_row = QHBoxLayout()
        btn_row.addStretch()   # 左弹簧，把按钮推到右边
        self.save_btn = QPushButton("保存设置")
        btn_row.addWidget(self.save_btn)
        # 这里不再需要右弹簧，因为左弹簧已经占满左边

        main_layout.addLayout(btn_row)

    def _on_check_update(self):
        """点击“检查更新”按钮时调用"""
        has_new = check_for_updates()

        if has_new:
            show_info("无可用更新", f"您的 {APP_NAME} 已是最新版本。")
        else:
            QMessageBox.information(self, "检查更新", "您已是最新版本！")