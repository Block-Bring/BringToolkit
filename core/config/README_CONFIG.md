
> ⚠ 这是由智能体生成的内容，仅供参考！
# 配置路径管理说明

## 📍 统一配置路径定义

配置文件路径在 `core/app_info.py` 中统一定义：

```python
CONFIG_PATH = "config.json"
```

## 🎯 好处

1. **集中管理** - 所有配置相关的路径都在一个地方定义
2. **易于修改** - 如果需要更改配置文件名或路径，只需修改一处
3. **避免硬编码** - 代码中不再有散落的 `"config.json"` 字符串
4. **便于维护** - 一眼就能看出项目使用的配置文件位置

## 📖 使用方法

### 方法1：直接使用全局配置（推荐）
```python
from core.config import config

# 自动使用 CONFIG_PATH 加载配置
value = config.get("settings.check_update")
```

### 方法2：获取配置路径常量
```python
from core.config import CONFIG_PATH

print(f"配置文件位于: {CONFIG_PATH}")
# 输出: 配置文件位于: config.json
```

### 方法3：自定义配置路径（高级用法）
```python
from core.config import config, save_config

# 如果需要临时使用其他配置文件
config._load_config("custom_config.json")
save_config("custom_config.json")
```

## 🔄 已更新的文件

- ✅ `core/config/create_config.py` - 使用 CONFIG_PATH 作为默认路径
- ✅ `core/config/load_config.py` - 使用 CONFIG_PATH 作为默认路径
- ✅ `core/config/__init__.py` - 导出 CONFIG_PATH 常量
- ✅ `core/config/example_usage.py` - 示例中包含 CONFIG_PATH 用法

## 💡 最佳实践

**不要在代码中硬编码 `"config.json"`**，而是：

❌ **不推荐**
```python
import json

with open("config.json", 'r') as f:
    data = json.load(f)
```

✅ **推荐**
```python
from core.config import config

# 让配置管理器处理文件读取
value = config.get("key")
```

或者如果确实需要直接访问文件：
```python
import json
from core.app_info import CONFIG_PATH

with open(CONFIG_PATH, 'r') as f:
    data = json.load(f)
```
