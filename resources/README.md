<!-- 
注意: 这是一个 Markdown 文档，不是 Python 代码文件。
IDE 可能会报告代码示例中的"错误"，这些可以安全忽略。
-->

# 资源文件使用指南

## 📦 PyInstaller 打包后访问资源文件

### 问题
PyInstaller 打包后的 exe 运行时，资源文件被打包在 exe 内部，无法直接用相对路径访问。

### 解决方案

#### 1. 使用 `get_resource_path()` 函数

```python
from core.app_info import get_resource_path

# 获取图标文件路径
icon_path = get_resource_path("resources/icon.ico")

# 在 PyQt6 中使用
from PyQt6.QtGui import QIcon
window.setWindowIcon(QIcon(icon_path))
```

#### 2. 工作原理

`get_resource_path()` 函数会自动检测运行环境：

- **开发环境**：返回项目根目录下的资源路径
- **打包环境**：返回 PyInstaller 临时解压目录下的资源路径

```python
# 内部实现逻辑（不需要自己写）
if hasattr(sys, '_MEIPASS'):
    # PyInstaller 打包后的临时目录
    base_path = sys._MEIPASS
else:
    # 开发环境的项目根目录
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

### 3. 配置 spec 文件

在 `BringToolkit.spec` 的 `datas` 中添加资源文件：

```python
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core/config', 'core/config'),
        ('resources', 'resources'),  # ← 添加这行，打包 resources 目录
    ],
    ...
)
```

⚠️ **重要**：修改 `.spec` 文件后需要重新打包才能生效！

### 4. 常见用法示例

#### 加载图标

在主窗口中设置应用图标：

```python
from core.app_info import get_resource_path
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 获取图标路径并设置
        icon_path = get_resource_path("resources/icon.ico")
        self.setWindowIcon(QIcon(icon_path))
```

#### 加载图片

在 QLabel 或其他控件中显示图片：

```python
from core.app_info import get_resource_path
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

# 获取图片路径
logo_path = get_resource_path("resources/images/logo.png")

# 创建标签并设置图片
logo_label = QLabel()
logo_label.setPixmap(QPixmap(logo_path))
```

#### 加载配置文件

读取 JSON 或其他配置文件：

```python
from core.app_info import get_resource_path
import json

# 获取配置文件路径
config_path = get_resource_path("resources/configs/default.json")

# 读取配置
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)
```

💡 **提示**：打包后的配置文件是只读的，不能修改。如果需要保存用户配置，应该保存到外部文件（如 `config.json`）。

### 5. 注意事项

⚠️ **重要：**
1. 所有资源文件必须在 `.spec` 文件的 `datas` 中声明
2. 路径是相对于项目根目录的
3. 打包后资源会被解压到临时目录，程序退出后自动清理

📁 **推荐的资源目录结构：**
```
Bring Toolkit/
├── resources/
│   ├── icon.ico              # 应用图标
│   ├── images/               # 图片资源
│   │   ├── logo.png
│   │   └── background.jpg
│   ├── sounds/               # 音效文件
│   │   └── notification.wav
│   └── configs/              # 默认配置文件
│       └── default.json
├── core/
├── main_window/
└── main.py
```

### 6. 测试

#### 开发环境测试
```python
# 直接运行 main.py
python main.py

# 应该能看到资源文件正常加载
```

#### 打包后测试
```bash
# 1. 打包
pyinstaller BringToolkit.spec --clean

# 2. 运行生成的 exe
dist\BringToolkit.exe

# 3. 检查资源是否正常加载
```

### 7. 调试技巧

如果资源文件没有正确加载，可以打印路径来调试：

```python
from core.app_info import get_resource_path
import os

icon_path = get_resource_path("resources/icon.ico")
print(f"资源路径: {icon_path}")
print(f"文件是否存在: {os.path.exists(icon_path)}")
```

---

## 💡 总结

✅ **优点：**
- 开发和打包环境自动适配
- 代码无需修改即可在不同环境运行
- 支持多种资源类型

❌ **限制：**
- 只读访问（打包后的资源不能修改）
- 大文件会增加 exe 体积
- 首次运行需要解压时间

🎯 **最佳实践：**
- 小文件（图标、配置）打包进 exe
- 大文件（图片、视频）放在外部，让用户自行下载
