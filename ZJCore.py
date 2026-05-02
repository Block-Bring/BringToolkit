"""
ZJCore - 简易对话框工具箱
用来快速弹出中文按钮的对话框。
"""
from PyQt6.QtWidgets import QMessageBox


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