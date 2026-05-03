from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QCheckBox, QLabel, QPushButton
)

from ZJCore import *
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
        """点击"检查更新"按钮时调用"""
        # 定义一个内部类 UpdateWorker，继承自 QThread，用于在后台线程执行耗时操作，避免界面卡死
        class UpdateWorker(QThread):
            # 定义一个信号，用于将检查结果（字典类型）发送回主线程
            result_signal = pyqtSignal(dict)

            # run 方法是在新线程中自动执行的入口函数
            def run(self):
                # 调用核心模块的检查更新函数，获取更新信息
                result = check_for_updates()
                # 通过信号将结果发射出去，通知主线程处理结果
                self.result_signal.emit(result)

        # 禁用“检查更新”按钮，防止用户重复点击
        self.check_update_btn.setEnabled(False)
        # 保存按钮当前的文本内容，以便检查结束后恢复
        original_text = self.check_update_btn.text()
        # 将按钮文本修改为“正在检查...”，提示用户当前状态
        self.check_update_btn.setText("正在检查...")

        # 创建 UpdateWorker 的实例
        self.worker = UpdateWorker()
        # 连接信号与槽：当后台线程发出结果信号时，调用 _on_update_finished 方法处理结果
        # 使用 lambda 表达式捕获当前的 original_text，确保回调时能恢复正确的按钮文本
        self.worker.result_signal.connect(lambda result: self._on_update_finished(result, original_text))
        # 启动后台线程，开始执行 run 方法中的检查更新逻辑
        self.worker.start()

    def _on_update_finished(self, result, original_text):
        """更新检查完成后的回调（在主线程中执行）"""
        self.check_update_btn.setText(original_text)
        self.check_update_btn.setEnabled(True)

        error = result.get("error")
        if error:
            show_error("检查更新失败", f"检查更新时遇到错误：{error}")
            return

        has_update = result.get("has_update", False)
        online_version = result.get("online_version")
        url = result.get("url")

        if has_update:
            question = ask_yes_no("发现新版本", f"当前所获取到的最新版本为 {online_version}\n是否更新？")
            if question and url:
                import webbrowser
                webbrowser.open(url)
        else:
            from core.app_info import APP_NAME
            show_info("无可用更新", f"您的 {APP_NAME} 已是最新版本。")
