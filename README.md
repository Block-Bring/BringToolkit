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

- 🎮 **Minecraft 配置** - 一键设置游戏选项
- 🔧 **实用小工具** - 一些方便的功能
- 💾 **自动保存设置** - 不用担心配置丢失
- 🚀 **轻量快速** - 启动超快，不占内存
- 🎨 **简洁界面** - 看起来舒服就好
- 🔄 **更新检查** - 可以检查新版本（支持稳定版和预览版）

---

## 🚀 怎么运行？

### 需要准备

- **电脑系统**: Windows 10/11
- **Python**: 3.11 版本（我用这个开发的）
- **几个库**: PyQt6, requests, packaging

### 开始使用

1. **下载代码**
   ```bash
   git clone https://github.com/Block-Bring/BringToolkit.git
   cd BringToolkit
   ```

2. **安装需要的库**
   ```bash
   pip install PyQt6 requests packaging
   ```

3. **运行！**
   ```bash
   python main.py
   ```

搞定！🎉

### 想打包成 exe？（可选）

如果你想做成可以直接双击运行的程序：

```bash
pip install pyinstaller
pyinstaller BringToolkit.spec
```

打包好的程序会在 `dist/` 文件夹里。

---

## 📸 长什么样？

*(这里以后放截图，现在先想象一下~)*

- **首页** - 简单明了
- **功能页** - 各种小工具
- **设置页** - 可以改配置
- **关于页** - 版本信息

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

## 🛠️ 用了什么技术？

- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - 做界面的
- **[requests](https://docs.python-requests.org/)** - 联网检查更新
- **[packaging](https://packaging.pypa.io/)** - 比较版本号
- **[PyInstaller](https://pyinstaller.org/)** - 打包成 exe

都是些基础的库，萌新也能看懂！

---

## 📝 开发进度

### ✅ 已经做完的

- [x] 主窗口和标签页
- [x] 配置保存和读取
- [x] 彩色日志系统
- [x] 检查更新功能（稳定版/预览版）
- [x] 关于页面
- [x] 版本号美化显示（比如 `1.0.0 Alpha 2`）
- [x] MacType 字体美化支持

### 🚧 正在做的

- [ ] 让界面更好看一点
- [ ] Minecraft 数据迁移功能

### 📋 以后想加的

- [ ] 深色模式
- [ ] 插件系统（可以自己加功能）
- [ ] 配置云同步

---

## 🤝 一起改进！

欢迎提建议或者帮我找 Bug！如果你也是萌新，我们可以一起学习~

1. **Fork** 这个仓库
2. 创建你的分支 (`git checkout -b feature/新功能`)
3. 提交修改 (`git commit -m '加了个新功能'`)
4. 推送 (`git push origin feature/新功能`)
5. 开个 **Pull Request**

---

## 📄 开源协议

用的是 **MIT License**，你可以随便用、随便改。

详情看 [LICENSE](LICENSE) 文件。

---

## 👥 关于我

**QuickYeah Studio** （其实就是我一个人啦 qwq）

- Block Bring - 啥都干的开发者

---

## 🙏 感谢

- 感谢所有给我 Star 的人！（虽然现在还没有几个 xwx）
- 感谢 Minecraft 社区
- 感谢写这些库的大佬们

---

## 📮 联系我

- **有问题？** [点这里提 Issue](https://github.com/Block-Bring/BringToolkit/issues)
- **GitHub**: [https://github.com/Block-Bring/BringToolkit](https://github.com/Block-Bring/BringToolkit)

---

<div align="center">

**如果觉得还行，给个 Star 呗~ ⭐**

Made with ❤️ and ☕ by QuickYeah Studio

</div>
