"""
自动更新模块 - 处理程序下载和替换
"""

import os
import sys
import tempfile

import requests
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout

from utils.logger import logger


class DownloadWorker(QThread):
    """后台下载线程"""

    progress_signal = pyqtSignal(int, int, int)  # 已下载, 总大小, 百分比
    finished_signal = pyqtSignal(str)  # 临时文件路径
    error_signal = pyqtSignal(str)  # 错误信息

    def __init__(self, url, temp_file):
        super().__init__()
        self.url = url
        self.temp_file = temp_file

    def run(self):
        try:
            logger.info(f"开始下载更新: {self.url}")
            response = requests.get(self.url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(self.temp_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percentage = int((downloaded / total_size) * 100) if total_size > 0 else 0
                        self.progress_signal.emit(downloaded, total_size, percentage)

            logger.info("下载完成")
            self.finished_signal.emit(self.temp_file)

        except Exception as e:
            logger.error(f"下载失败: {e}")
            self.error_signal.emit(f"下载失败: {e}")


class UpdateDialog(QDialog):
    """更新对话框"""

    def __init__(self, version, url, parent=None):
        super().__init__(parent)
        self.version = version
        self.url = url
        self.temp_file = os.path.join(tempfile.gettempdir(), "bring_toolkit_update.exe")
        self.downloaded_file = None

        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("软件更新")
        self.setFixedSize(450, 200)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题
        title_label = QLabel(f"📦 发现新版本 {self.version}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 状态文字
        self.status_label = QLabel("准备下载...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # 进度详情
        self.progress_detail = QLabel("")
        self.progress_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_detail.setStyleSheet("font-size: 11px; color: gray;")
        layout.addWidget(self.progress_detail)

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)  # type: ignore
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setMinimumWidth(80)
        btn_layout.addWidget(self.cancel_btn)

        self.start_btn = QPushButton("开始更新")
        self.start_btn.clicked.connect(self.start_download)  # type: ignore
        self.start_btn.setMinimumWidth(80)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        btn_layout.addWidget(self.start_btn)

        layout.addLayout(btn_layout)

    def start_download(self):
        """开始下载"""
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText("正在下载更新包...")

        # 启动下载线程
        self.worker = DownloadWorker(self.url, self.temp_file)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.download_finished)
        self.worker.error_signal.connect(self.download_error)
        self.worker.start()

    def update_progress(self, downloaded, total, percentage):
        """更新进度"""
        self.progress_bar.setValue(percentage)

        if total >= 1024 * 1024 * 1024:
            unit, divisor = "GB", 1024**3
        elif total >= 1024 * 1024:
            unit, divisor = "MB", 1024**2
        else:
            unit, divisor = "B", 1

        self.progress_detail.setText(
            f"{downloaded / divisor:.2f} {unit} / {total / divisor:.2f} {unit} ({percentage}%)"
        )

    def download_finished(self, file_path):
        """下载完成"""
        self.downloaded_file = file_path
        self.status_label.setText("✅ 下载完成！")
        self.progress_bar.setValue(100)
        self.progress_detail.setText('点击"开始更新"按钮安装更新')

        self.start_btn.setText("安装更新")
        self.start_btn.setEnabled(True)
        self._set_start_action(self.install_update)
        self.cancel_btn.setText("关闭")

    def download_error(self, error_msg):
        """下载出错"""
        self.status_label.setText("❌ 下载失败")
        self.status_label.setStyleSheet("color: red;")
        self.progress_detail.setText(error_msg)
        self.start_btn.setEnabled(True)
        self.start_btn.setText("重试")
        self._set_start_action(self.start_download)
        self.cancel_btn.setText("关闭")

    def install_update(self):
        """安装更新（替换程序）"""
        if not self.downloaded_file or not os.path.exists(self.downloaded_file):
            return

        try:
            logger.info("开始安装更新...")
            self.status_label.setText("正在安装更新...")
            self.start_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)

            current_exe = sys.executable if getattr(sys, "frozen", False) else sys.argv[0]
            batch_script = os.path.join(tempfile.gettempdir(), "bring_toolkit_update.bat")

            with open(batch_script, "w", encoding="gbk") as f:
                f.write("@echo off\n")
                f.write("echo ====================================\n")
                f.write("echo    Bring Toolkit 自动更新程序\n")
                f.write("echo ====================================\n")
                f.write("echo.\n")
                f.write("echo [1/3] 关闭当前程序...\n")
                # 获取当前进程ID
                current_pid = os.getpid()
                f.write(f"taskkill /F /PID {current_pid} >nul 2>&1\n")
                f.write("timeout /t 1 /nobreak >nul\n")
                f.write("echo.\n")
                f.write("echo [2/3] 正在替换文件...\n")
                f.write("set retry_count=0\n")
                f.write(":retry_copy\n")
                f.write(f'copy /y "{self.downloaded_file}" "{current_exe}" >nul 2>&1\n')
                f.write("if errorlevel 1 (\n")
                f.write("    set /a retry_count+=1\n")
                f.write("    if !retry_count! lss 5 (\n")
                f.write("        timeout /t 1 /nobreak >nul\n")
                f.write("        goto retry_copy\n")
                f.write("    ) else (\n")
                f.write("        echo 错误：无法替换文件\n")
                f.write("        pause\n")
                f.write("        exit /b 1\n")
                f.write("    )\n")
                f.write(")\n")
                f.write("echo.\n")
                f.write("echo [3/3] 清理临时文件...\n")
                f.write(f'del "{self.downloaded_file}"\n')
                f.write("echo.\n")
                f.write("echo 更新完成！\n")
                f.write("echo.\n")
                f.write("echo 请手动重新启动程序。\n")
                f.write("timeout /t 5 /nobreak >nul\n")
                f.write('del "%~f0"\n')

            logger.info("更新脚本已创建，请手动重启程序")
            self.status_label.setText("✅ 更新下载完成！")
            self.progress_detail.setText("请关闭此窗口并手动重新启动程序")

            import subprocess

            subprocess.Popen(batch_script, creationflags=subprocess.CREATE_NEW_CONSOLE)

            self.start_btn.setEnabled(False)
            self.start_btn.setText("请手动重启")
            self.cancel_btn.setText("关闭")

        except Exception as e:
            error_msg = f"安装失败: {e}"
            logger.error(error_msg)
            self.status_label.setText("❌ 安装失败")
            self.status_label.setStyleSheet("color: red;")
            self.progress_detail.setText(error_msg)
            self.start_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)

    def _set_start_action(self, action):
        """安全切换按钮行为，避免重复 disconnect 报错"""
        try:
            self.start_btn.clicked.disconnect()
        except TypeError:
            pass
        self.start_btn.clicked.connect(action)

    def reject(self):
        """取消/关闭对话框"""
        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.terminate()

        if self.downloaded_file and os.path.exists(self.downloaded_file):
            try:
                os.remove(self.downloaded_file)
            except OSError:
                pass

        super().reject()
