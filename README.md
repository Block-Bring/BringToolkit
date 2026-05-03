# 🛠️ Bring Toolkit

> 一个由编程萌新制作的 Minecraft 工具箱练习项目 (｡•̀ᴗ-)✧

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.x-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 💭 这是什么？

这是我学习 Python 时做的一个小练习，主要想做一个能帮 Minecraft 玩家管理游戏的小工具。虽然代码可能不够完美，但我会慢慢改进的！

### ✨ 有什么功能？

- 🎮 **整合包个性化数据迁移** - 把更新整合包前的个性化数据迁移进去

---

## 📁 文件结构

```
BringToolkit/
├── core/                   # 核心功能
│   ├── app_info.py        # 软件名字、版本号
│   ├── config/            # 配置管理
│   ├── logger.py          # 日志记录（彩色的哦）
│   └── update.py          # 检查更新
├── main_window/           # 界面
│   ├── home_tab.py        # 首页
│   ├── func_tab.py        # 功能页
│   ├── settings_tab.py    # 设置页
│   └── about_tab.py       # 关于页
├── ZJCore.py             # 我自己写的小工具函数
├── main.py               # 从这里启动
└── config.json           # 配置文件（自动生成）
```

---

## 🛠️ 用了什么？

- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - 做界面的
- **[requests](https://docs.python-requests.org/)** - 联网检查更新
- **[packaging](https://packaging.pypa.io/)** - 比较版本号
- **[PyInstaller](https://pyinstaller.org/)** - 打包成 exe

---

## 📝 开发进度

### ✅ 已经做完的

- [x] 主窗口和标签页
- [x] 配置保存和读取
- [x] 彩色日志系统
- [x] 检查更新功能（稳定版/预览版）
- [x] 关于页面

### 🚧 正在做的

- [ ] 让界面更好看一点
- [ ] Minecraft 数据迁移功能

## 📄 开源协议

用的是 **MIT License**，你可以随便用、随便改。

详情看 [LICENSE](LICENSE) 文件。

---
