"""
Minecraft 数据迁移窗口
用于选择源目录和目标实例，执行数据迁移
"""

import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from utils.logger import logger
from utils.nana_tools import ask_yes_no, show_info, show_warning

_MINECRAFT_MARKERS = ["launcher_profiles.json", "versions", "assets", "libraries"]


class MigratorWindow(QDialog):
    """数据迁移窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📦 Bring Craft 数据迁移")
        self.resize(600, 400)
        self._selected_dir = None
        self._init_ui()

    def _init_ui(self):
        """初始化界面布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

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

        # ===== 迁移实例选择 =====
        target_group = QGroupBox("🎯 迁移实例")
        target_layout = QHBoxLayout(target_group)

        old_instance_label = QLabel("选择旧版实例:")
        self.instance_combo = QComboBox()
        self.instance_combo.setMinimumHeight(30)
        self.instance_combo.setPlaceholderText("请先选择源目录")

        new_instance_label = QLabel("选择目标实例:")
        self.new_instance_combo = QComboBox()
        self.new_instance_combo.setMinimumHeight(30)
        self.new_instance_combo.setPlaceholderText("请先选择源目录")

        refresh_btn = QPushButton("🔄 刷新实例列表")
        refresh_btn.clicked.connect(self._refresh_instances)
        refresh_btn.setFixedWidth(120)
        refresh_btn.setMinimumHeight(50)

        combo_layout = QVBoxLayout()
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

    # ---- 目录选择与验证 ----

    def _browse_source_directory(self):
        """浏览并选择 .minecraft 目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择 .minecraft 目录",
            "",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if not directory:
            return

        directory = os.path.normpath(directory)

        if self._is_minecraft_dir(directory):
            self._selected_dir = directory
        else:
            # 看看所选目录下有没有 .minecraft 子目录
            sub_minecraft = os.path.join(directory, ".minecraft")
            if os.path.isdir(sub_minecraft) and self._is_minecraft_dir(sub_minecraft):
                self._selected_dir = sub_minecraft
                directory = sub_minecraft
            else:
                show_warning("无效目录", "所选目录不是有效的 .minecraft 目录\n\n"
                              "请选择包含 versions、assets 等子目录的 .minecraft 文件夹。")
                return

        self.source_input.setText(directory)
        logger.info(f"已选择源目录: {directory}")
        self._load_instances(directory)

    @staticmethod
    def _is_minecraft_dir(path):
        """通过特征子目录/文件判断是否为 .minecraft 目录"""
        return any(os.path.isdir(os.path.join(path, m)) or os.path.isfile(os.path.join(path, m))
                   for m in _MINECRAFT_MARKERS)

    # ---- 实例扫描 ----

    @staticmethod
    def _detect_loader(version_json_path):
        """
        解析 version.json，识别 Mod 加载器类型。
        返回 (loader_type, loader_version) 元组，原版返回 (None, None)。

        检测策略（按优先级）：
        1. arguments.game 中的 --fml.forgeVersion / --fml.neoForgeVersion
        2. libraries 中的主加载器 artifact（net.neoforged:neoforge 等）
        3. libraries 中的辅助 artifact（net.minecraftforge:fmlloader 等）
        4. arguments.game 中的 --launchTarget forgeclient
        5. inheritsFrom 字段
        """
        try:
            with open(version_json_path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return None, None

        # 1) arguments.game — 高版本 Forge/NeoForge 用 Modlauncher 架构，
        #    版本信息仅存在于 game args 而非 libraries
        game_args = data.get("arguments", {}).get("game", [])
        if isinstance(game_args, list):
            for i, arg in enumerate(game_args):
                if isinstance(arg, str):
                    if arg == "--fml.neoForgeVersion" and i + 1 < len(game_args):
                        return "NeoForge", str(game_args[i + 1])
                    if arg == "--fml.forgeVersion" and i + 1 < len(game_args):
                        return "Forge", str(game_args[i + 1])

        # 2) libraries — 主 artifact（精确匹配 group:artifact）
        libraries = data.get("libraries", [])
        for lib in libraries:
            name = lib.get("name", "")
            parts = name.split(":")
            group_artifact = ":".join(parts[:2])

            if group_artifact == "net.neoforged:neoforge":
                return "NeoForge", parts[-1] if len(parts) >= 3 else ""
            if group_artifact == "net.minecraftforge:forge":
                return "Forge", parts[-1] if len(parts) >= 3 else ""
            if group_artifact == "net.fabricmc:fabric-loader":
                return "Fabric", parts[-1] if len(parts) >= 3 else ""
            if group_artifact == "org.quiltmc:quilt-loader":
                return "Quilt", parts[-1] if len(parts) >= 3 else ""

        # 3) libraries — 辅助 artifact（高版本 Forge/NeoForge 的 fmlloader）
        for lib in libraries:
            name = lib.get("name", "")
            parts = name.split(":")
            group_artifact = ":".join(parts[:2])

            if group_artifact == "net.minecraftforge:fmlloader":
                ver = parts[-1] if len(parts) >= 3 else ""
                dash_idx = ver.find("-")
                if dash_idx >= 0:
                    ver = ver[dash_idx + 1:]
                return "Forge", ver

            if group_artifact == "net.neoforged.fancymodloader:loader":
                return "NeoForge", parts[-1] if len(parts) >= 3 else ""

        # 4) arguments.game — launchTarget 回退
        if isinstance(game_args, list):
            for i, arg in enumerate(game_args):
                if (isinstance(arg, str) and arg == "--launchTarget"
                        and i + 1 < len(game_args) and game_args[i + 1] == "forgeclient"):
                    return "Modded", None

        if data.get("inheritsFrom"):
            return "Modded", None

        return None, None

    def _load_instances(self, directory):
        """从指定 .minecraft 目录扫描可用实例"""
        self.instance_combo.clear()
        self.new_instance_combo.clear()

        instances = self._scan_instances(directory)

        if not instances:
            self.instance_combo.addItem("未发现可用实例")
            self.new_instance_combo.addItem("未发现可用实例")
            logger.info("未发现任何 Minecraft 实例")
            return

        for name, loader, loader_ver in instances:
            display = self._format_instance(name, loader, loader_ver)
            self.instance_combo.addItem(display)
            self.new_instance_combo.addItem(display)

        self.instance_combo.setCurrentIndex(0)
        self.new_instance_combo.setCurrentIndex(0)

        logger.info(f"已加载 {len(instances)} 个 Minecraft 实例")

    @staticmethod
    def _format_instance(name, loader, loader_ver):
        """生成下拉框显示文本"""
        if not loader:
            return name
        if loader_ver:
            return f"{name} [{loader} {loader_ver}]"
        return f"{name} [{loader}]"

    def _refresh_instances(self):
        """从当前已选择的目录重新扫描实例"""
        if not self._selected_dir:
            show_warning("提示", "请先选择一个 .minecraft 目录")
            return
        self._load_instances(self._selected_dir)

    @staticmethod
    def _scan_instances(minecraft_dir):
        """扫描 versions/ 子目录并识别加载器类型"""
        versions_dir = os.path.join(minecraft_dir, "versions")
        if not os.path.isdir(versions_dir):
            return []

        instances = []
        try:
            for entry in sorted(os.listdir(versions_dir)):
                entry_path = os.path.join(versions_dir, entry)
                if not os.path.isdir(entry_path):
                    continue
                version_json = os.path.join(entry_path, f"{entry}.json")
                loader, loader_ver = MigratorWindow._detect_loader(version_json)
                instances.append((entry, loader, loader_ver))
        except OSError as e:
            logger.warning(f"无法读取 versions 目录: {e}")

        return instances

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
            default=False,  # 默认选"否"，更安全
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
                "• 模组配置",
            )
