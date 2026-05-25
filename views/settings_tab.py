import webbrowser

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QCheckBox, QLabel, QPushButton
)

from core.app_info import APP_NAME, format_version_display, GITHUB_REPO
from core.check_update import check_for_updates, CheckResult
from core.updater import UpdateDialog
from core.config import config, save_config
from utils.nana_tools import ask_yes_no, show_info, show_error, run_in_background



class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self) # 主布局（垂直）
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        group_update = QGroupBox("软件更新")
        update_layout = QVBoxLayout() # 启动行为布局（垂直）
        group_update.setLayout(update_layout)

        # 按钮布局（水平）：将"检查更新"按钮靠左放置
        chk_btn_layout = QHBoxLayout()
        self.check_update_btn = QPushButton("检查更新")
        self.check_update_btn.clicked.connect(self._on_check_update)  # type: ignore[attr-defined]

        chk_btn_layout.addWidget(self.check_update_btn)
        chk_btn_layout.addStretch()
        update_layout.addLayout(chk_btn_layout)

        self.check_update_cb = QCheckBox("启动时检查更新")
        # 从配置中读取初始值
        self.check_update_cb.setChecked(config.get("settings.check_update", True))
        update_layout.addWidget(self.check_update_cb)

        main_layout.addWidget(group_update)

        # ----- 体验计划分组 -----
        group_insider = QGroupBox("体验计划")
        insider_layout = QVBoxLayout()
        group_insider.setLayout(insider_layout)

        self.insider_cb = QCheckBox("加入 Insider Preview 计划")
        # 从配置中读取初始值
        self.insider_cb.setChecked(config.get("settings.insider_preview", False))
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
        self.save_btn.clicked.connect(self._on_save_settings)  # type: ignore[attr-defined]
        btn_row.addWidget(self.save_btn)
        # 这里不再需要右弹簧，因为左弹簧已经占满左边

        main_layout.addLayout(btn_row)

    def _on_save_settings(self):
        """点击"保存设置"按钮时调用"""
        # 保存复选框的状态到配置
        config.set("settings.check_update", self.check_update_cb.isChecked())
        config.set("settings.insider_preview", self.insider_cb.isChecked())

        # 保存到文件
        if save_config():
            original_text = self.save_btn.text()
            self.save_btn.setText("保存成功")
            self.save_btn.setEnabled(False)
            # 1秒后恢复按钮状态和文本
            QTimer.singleShot(1000, lambda: self._restore_save_button(original_text))
        else:
            show_error("保存失败", "无法保存设置，请重试")

    def _restore_save_button(self, original_text):
        """恢复保存按钮的状态"""
        self.save_btn.setText(original_text)
        self.save_btn.setEnabled(True)

    def _on_check_update(self):
        """点击"检查更新"按钮时调用"""
        # 如果已有检查在运行，直接忽略
        if hasattr(self, 'worker') and self.worker.isRunning():
            return

        # 禁用"检查更新"按钮，防止用户重复点击
        self.check_update_btn.setEnabled(False)
        original_text = self.check_update_btn.text()
        self.check_update_btn.setText("正在检查")

        # 根据配置决定是否检查预览版
        insider_preview = config.get("settings.insider_preview", False)

        # 使用 ZJCore 的 run_in_background 简化多线程代码
        def task():
            return check_for_updates(insider_preview=insider_preview)

        def on_finished(result):
            self._on_update_finished(result, original_text)

        self.worker = run_in_background(task, on_finished=on_finished)
        self.worker.start()

    def _on_update_finished(self, result: CheckResult, original_text):
        """更新检查完成后的回调（在主线程中执行）"""
        self.check_update_btn.setText(original_text)
        self.check_update_btn.setEnabled(True)

        if result.error:
            show_error("检查更新失败", f"检查更新时遇到错误：{result.error}")
            if result.format_mismatch or result.error_404:
                webbrowser.open(f"{GITHUB_REPO}/releases")
            return

        if result.has_update and result.latest_version and result.download_url:
            version_type = "稳定版" if result.is_stable else "预览版"
            formatted = format_version_display(result.latest_version)
            question = ask_yes_no("发现新版本", f"当前所获取到的最新版本为 {formatted}（{version_type}）\n是否更新？")
            if question:
                UpdateDialog(formatted, result.download_url, self).exec()
        else:
            show_info("无可用更新", f"您的 {APP_NAME} 已是最新版本。")
