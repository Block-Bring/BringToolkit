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


def ask_yes_no(title: str, message: str, default: bool = False) -> bool:
    """
    弹出一个带有"是/否"按钮的询问框。
    
    参数:
        title: 标题
        message: 内容
        default: True 默认选"是"，False 默认选"否"
    
    返回:
        True = 用户点击"是"，False = 用户点击"否"
    
    示例:
        # 默认选"否"（更安全）
        if ask_yes_no("确认删除", "确定要删除这个文件吗？", default=False):
            print("用户选择了是")
        
        # 默认选"是"（更方便）
        if ask_yes_no("确认退出", "确定要退出吗？", default=True):
            print("用户选择了是")
    """
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Question)
    
    yes_btn = box.addButton("是", QMessageBox.ButtonRole.YesRole)
    no_btn = box.addButton("否", QMessageBox.ButtonRole.NoRole)
    
    # 设置默认按钮
    if default:
        box.setDefaultButton(yes_btn)
    else:
        box.setDefaultButton(no_btn)
    
    box.exec()
    return box.clickedButton() == yes_btn


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

def show_warning(title: str, message: str):
    """弹出一个警告提示框"""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Icon.Warning)
    box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
    box.exec()