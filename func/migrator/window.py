"""
Minecraft 数据迁移窗口
用于选择源目录和目标实例，执行数据迁移
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QComboBox,
    QGroupBox
)
from PyQt6.QtCore import Qt

from tools.logger import logger
from tools.NanaTools import ask_yes_no, show_info, show_warning


class MigratorWindow(QDialog):
    """数据迁移窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📦 Bring Craft 数据迁移")
        self.resize(600, 400)

        # 初始化 UI
        self._init_ui()

        # 加载可用的 Minecraft 实例
        self._load_instances()

    def _init_ui(self):
        """初始化界面布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ===== 标题 =====
        title_label = QLabel("📦 Bring Craft 个性化数据迁移")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # ===== 源目录选择 =====
        source_group = QGroupBox("📂 源目录（整合包所在）")
        source_layout = QHBoxLayout(source_group)

        source_label = QLabel(".minecraft 目录:")
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("选择 .minecraft 目录...")
        self.source_input.setReadOnly(True)

        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self._browse_source_directory)
        browse_btn.setFixedWidth(80)

        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_input)
        source_layout.addWidget(browse_btn)
        main_layout.addWidget(source_group)

        # ===== 目标实例选择 =====
        target_group = QGroupBox("🎯 迁移实例")
        target_layout = QHBoxLayout(target_group)

        # 源实例选择
        old_instance_label = QLabel("选择旧版实例:")
        self.instance_combo = QComboBox()
        self.instance_combo.setMinimumHeight(30)

        # 目标实例选择
        new_instance_label = QLabel("选择目标实例:")
        self.new_instance_combo = QComboBox()
        self.new_instance_combo.setMinimumHeight(30)

        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新实例列表")
        refresh_btn.clicked.connect(self._load_instances)
        refresh_btn.setFixedWidth(120)
        refresh_btn.setMinimumHeight(50)

        # 组合下拉框和刷新按钮
        combo_layout = QVBoxLayout()

        # 添加到目标布局
        combo_layout.addWidget(old_instance_label)
        combo_layout.addWidget(self.instance_combo)
        combo_layout.addWidget(new_instance_label)
        combo_layout.addWidget(self.new_instance_combo)
        target_layout.addLayout(combo_layout)
        target_layout.addWidget(refresh_btn)
        main_layout.addWidget(target_group)

        # ===== 说明文字 =====
        info_label = QLabel(
            "💡 提示：迁移将复制以下数据：\n"
            "• 存档 (saves)\n"
            "• 资源包 (resourcepacks)\n"
            "• 光影配置 (shaderpacks)\n"
            "• 截图 (screenshots)\n"
            "• 模组配置 (config)"
        )
        info_label.setStyleSheet("""
            background-color: rgba(76, 175, 80, 0.1);
            border: 1px solid #4CAF50;
            border-radius: 4px;
            padding: 10px;
            font-size: 11px;
        """)
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)

        # ===== 按钮区域 =====
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFixedWidth(80)

        migrate_btn = QPushButton("开始迁移")
        migrate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        migrate_btn.setFixedWidth(100)
        migrate_btn.clicked.connect(self._start_migration)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(migrate_btn)
        main_layout.addLayout(button_layout)

    def _browse_source_directory(self):
        """浏览选择源目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择 .minecraft 目录",
            "",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )

        if directory:
            # 检查是否是有效的 .minecraft 目录
            self.source_input.setText(directory)
            logger.info(f"已选择源目录: {directory}")

    def _load_instances(self):
        """加载可用的 Minecraft 实例"""
        self.instance_combo.clear()
        self.new_instance_combo.clear()

        # TODO: 从启动器或配置文件读取实际的实例列表
        # 这里先添加一些示例数据
        instances = [
            "BringCraft-Latest",
            "BringCraft-1.20.1",
            "BringCraft-1.19.2",
            "Default-Minecraft"
        ]

        for instance in instances:
            self.instance_combo.addItem(instance)
            self.new_instance_combo.addItem(instance)

        logger.info(f"已加载 {len(instances)} 个 Minecraft 实例")

    def _start_migration(self):
        """开始迁移"""
        source_dir = self.source_input.text()
        source_instance = self.instance_combo.currentText()
        target_instance = self.new_instance_combo.currentText()

        # 验证输入
        if not source_dir:
            show_warning("警告", "请先选择源目录！")
            return

        if not source_instance:
            show_warning("警告", "请选择源实例！")
            return

        if not target_instance:
            show_warning("警告", "请选择目标实例！")
            return

        # 确认对话框
        reply = ask_yes_no(
            "确认迁移",
            f"确定要迁移数据吗？\n\n"
            f"源目录: {source_dir}\n"
            f"源实例: {source_instance}\n"
            f"目标实例: {target_instance}",
            default=False  # 默认选"否"，更安全
        )

        if reply:
            logger.info(f"开始迁移: {source_instance} -> {target_instance}")

            # TODO: 实现实际的迁移逻辑
            show_info(
                "迁移功能开发中",
                "迁移功能正在开发中...\n\n"
                "将会复制:\n"
                "• 存档\n"
                "• 资源包\n"
                "• 光影配置\n"
                "• 截图\n"
                "• 模组配置"
            )
