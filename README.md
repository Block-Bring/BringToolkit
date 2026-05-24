# 🛠️ Bring Toolkit

> 一个由编程萌新制作的 Minecraft 工具箱练习项目 (｡•̀ᴗ-)✧

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.x-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> [!WARNING]
> 本项目仍处于早期阶段，有相当部分的代码由智能体辅助生成，虽然经过了人工测试，但仍可能包含不稳定性。欢迎[提交 Issue](https://github.com/Block-Bring/BringToolkit/issues)！

---

## 💭 这是什么？

这是我学习 Python 时做的一个小练习，目标是做一个能帮 Minecraft 玩家管理游戏数据的工具箱。虽然代码可能不够完美，但我会慢慢改进的！

### ✨ 有什么功能？

- 🔄 **自动检查更新** - 支持稳定版和 Insider Preview 双通道，下载后自动替换安装
- 🎮 **整合包数据迁移** - 更新整合包时，一键迁移存档、配置、光影等个性化数据

---

## 🚀 怎么运行？

1. 安装 Python 3.11+
2. 克隆项目
   ```bash
   git clone https://github.com/Block-Bring/BringToolkit.git
   cd BringToolkit
   ```
3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
4. 运行
   ```bash
   python main.py
   ```

---

## 🛠️ 技术栈

### 运行时依赖

| 库 | 用途 |
|---|---|
| [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) | GUI 界面 |
| [requests](https://docs.python-requests.org/) | 网络请求（检查更新） |
| [packaging](https://packaging.pypa.io/) | 版本号比较 |

### 打包工具

- [PyInstaller](https://pyinstaller.org/) - 打包成独立 exe

---

## 📝 开发进度

### ✅ 已完成

- [x] 主窗口和标签页导航
- [x] 配置保存和读取
- [x] 彩色日志系统
- [x] 检查更新功能（稳定版 / Insider Preview）
- [x] 自动下载 & 安装更新

### 🚧 进行中

- [ ] Minecraft 数据迁移功能
- [ ] QSS 界面美化

---

## 🤝 参与贡献

欢迎提 Issue、PR，或者直接来聊天！因为是学习项目，任何建议对我都有帮助～

- [提交 Bug 或建议](https://github.com/Block-Bring/BringToolkit/issues)

---

## 📄 开源协议

基于 **MIT License** 开源，可自由使用和修改。详见 [LICENSE](LICENSE)。
