import webbrowser

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.app_info import APP_NAME, GITHUB_REPO, format_version_display
from core.check_update import CheckResult, check_for_updates
from core.config import config, save_config
from core.updater import UpdateDialog
from utils.nana_tools import ask_yes_no, run_in_background, show_error, show_info


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        group_update = QGroupBox("软件更新")
        update_layout = QVBoxLayout()
        group_update.setLayout(update_layout)

        chk_btn_layout = QHBoxLayout()
        self.check_update_btn = QPushButton("检查更新")
        self.check_update_btn.clicked.connect(self._on_check_update)  # type: ignore[attr-defined]

        chk_btn_layout.addWidget(self.check_update_btn)
        chk_btn_layout.addStretch()
        update_layout.addLayout(chk_btn_layout)

        self.check_update_cb = QCheckBox("启动时检查更新")
        self.check_update_cb.setChecked(config.get("settings.check_update", True))
        update_layout.addWidget(self.check_update_cb)

        main_layout.addWidget(group_update)

        group_insider = QGroupBox("体验计划")
        insider_layout = QVBoxLayout()
        group_insider.setLayout(insider_layout)

        self.insider_cb = QCheckBox("加入 Insider Preview 计划")
        self.insider_cb.setChecked(config.get("settings.insider_preview", False))
        insider_layout.addWidget(self.insider_cb)

        insider_note = QLabel("提前体验新功能，可能会遇到不稳定情况。")
        insider_note.setStyleSheet("color: gray;")
        insider_note.setWordWrap(True)
        insider_layout.addWidget(insider_note)

        main_layout.addWidget(group_insider)

        main_layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.save_btn = QPushButton("保存设置")
        self.save_btn.clicked.connect(self._on_save_settings)  # type: ignore[attr-defined]
        btn_row.addWidget(self.save_btn)

        main_layout.addLayout(btn_row)

    def _on_save_settings(self):
        config.set("settings.check_update", self.check_update_cb.isChecked())
        config.set("settings.insider_preview", self.insider_cb.isChecked())

        if save_config():
            original_text = self.save_btn.text()
            self.save_btn.setText("保存成功")
            self.save_btn.setEnabled(False)
            QTimer.singleShot(1000, lambda: self._restore_save_button(original_text))
        else:
            show_error("保存失败", "无法保存设置，请重试")

    def _restore_save_button(self, original_text):
        self.save_btn.setText(original_text)
        self.save_btn.setEnabled(True)

    def _on_check_update(self):
        if hasattr(self, "worker") and self.worker.isRunning():
            return

        self.check_update_btn.setEnabled(False)
        original_text = self.check_update_btn.text()
        self.check_update_btn.setText("正在检查")

        insider_preview = config.get("settings.insider_preview", False)

        def task():
            return check_for_updates(insider_preview=insider_preview)

        def on_finished(result):
            self._on_update_finished(result, original_text)

        self.worker = run_in_background(task, on_finished=on_finished)
        self.worker.start()

    def _on_update_finished(self, result: CheckResult, original_text):
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
            question = ask_yes_no(
                "发现新版本", f"当前所获取到的最新版本为 {formatted}（{version_type}）\n是否更新？"
            )
            if question:
                UpdateDialog(formatted, result.download_url, self).exec()
        else:
            show_info("无可用更新", f"您的 {APP_NAME} 已是最新版本。")
