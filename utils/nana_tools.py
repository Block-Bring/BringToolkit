"""
NanaTools - 纳西妲的贴心工具箱 🌿
提供常用的 UI 对话框和后台任务执行工具。
"""
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal


def run_in_background(task_func, on_finished=None, on_error=None):
    """
    在后台线程执行耗时任务，避免阻塞 UI。

    参数:
        task_func: 要在后台执行的函数
        on_finished: 任务完成后的回调，接收返回值
        on_error: 任务出错后的回调，接收异常信息

    返回:
        QThread 对象，调用 .start() 启动
    """
    class BackgroundWorker(QThread):
        finished_signal = pyqtSignal(object)
        error_signal = pyqtSignal(object)

        def run(self):
            try:
                self.finished_signal.emit(task_func())  # type: ignore[attr-defined]
            except Exception as e:
                self.error_signal.emit(e)  # type: ignore[attr-defined]

    worker = BackgroundWorker()

    if on_finished:
        worker.finished_signal.connect(on_finished)  # type: ignore[attr-defined]

    if on_error:
        worker.error_signal.connect(on_error)  # type: ignore[attr-defined]

    return worker


def ask_yes_no(title: str, message: str, default: bool = False) -> bool:
    """弹出一个带有"是/否"按钮的询问框。"""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Question)

    yes_btn = box.addButton("是", QMessageBox.ButtonRole.YesRole)
    no_btn = box.addButton("否", QMessageBox.ButtonRole.NoRole)
    box.setDefaultButton(yes_btn if default else no_btn)

    box.exec()
    return box.clickedButton() == yes_btn


def show_info(title: str, message: str):
    """弹出信息提示框。"""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Information)
    box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
    box.exec()


def show_error(title: str, message: str):
    """弹出错误提示框。"""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Critical)
    box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
    box.exec()


def show_warning(title: str, message: str):
    """弹出警告提示框。"""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Warning)
    box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
    box.exec()