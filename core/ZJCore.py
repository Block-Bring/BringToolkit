"""
ZJCore - 简化语法工具箱
用来简化过于复杂的实现代码。
"""
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal


def run_in_background(task_func, on_finished=None, on_error=None):
    """
    在后台线程执行耗时任务，避免阻塞 UI。
    
    参数:
        task_func: 要在后台执行的函数
        on_finished: 任务完成后的回调函数（在主线程中执行），接收任务的返回值
        on_error: 任务出错后的回调函数（在主线程中执行），接收异常信息
    
    返回:
        QThread 对象，可以调用 .start() 启动
    
    示例:
        def long_task():
            import time
            time.sleep(2)
            return "任务完成"
        
        def on_result(result):
            print(result)
        
        worker = run_in_background(long_task, on_finished=on_result)
        worker.start()
    """
    class BackgroundWorker(QThread):
        finished_signal = pyqtSignal(object)
        error_signal = pyqtSignal(object)
        
        def run(self):
            try:
                result = task_func()
                self.finished_signal.emit(result)  # type: ignore[attr-defined]
            except Exception as e:
                self.error_signal.emit(e)  # type: ignore[attr-defined]
    
    worker = BackgroundWorker()
    
    if on_finished:
        worker.finished_signal.connect(on_finished)  # type: ignore[attr-defined]
    
    if on_error:
        worker.error_signal.connect(on_error)  # type: ignore[attr-defined]
    
    return worker


def ask_yes_no(title: str, message: str) -> bool:
    """
    弹出一个带有“是/否”按钮的询问框。
    返回 True 表示用户点击了“是”，False 表示点击“否”。
    """
    # 1. 创建一个消息框对象
    box = QMessageBox()

    # 2. 设置标题和内容
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Question)  # 问号图标

    # 3. 添加中文按钮
    yes_btn = box.addButton("是", QMessageBox.ButtonRole.YesRole)
    no_btn = box.addButton("否", QMessageBox.ButtonRole.NoRole)

    # 4. 默认选中“是”（按回车直接触发）
    box.setDefaultButton(yes_btn)

    # 5. 显示对话框并等待用户点击
    box.exec()

    # 6. 判断用户点的是哪个按钮
    return True if box.clickedButton() == yes_btn else False


def show_info(title: str, message: str):
    """弹出一个“确定”的信息框"""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Information)
    box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
    box.exec()

def show_error(title: str, message: str):
    """弹出一个错误提示框"""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Critical)
    box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
    box.exec()