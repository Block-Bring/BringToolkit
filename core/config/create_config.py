"""
创建默认配置文件
如果 config.json 不存在，则创建一个包含默认值的配置文件
"""
import json
import os
from core.app_info import CONFIG_PATH


def create_default_config(config_path=None):
    """
    创建默认配置文件
    
    参数:
        config_path: 配置文件路径，默认使用 core.app_info.CONFIG_PATH
    
    返回:
        str: 配置文件路径
    """
    if config_path is None:
        config_path = CONFIG_PATH
    # 定义默认配置
    default_config = {
        "minecraft_directory": "",
        "settings": {
            "check_update": True,
            "insider_preview": False
        }
    }
    
    # 如果配置文件不存在，则创建
    if not os.path.exists(config_path):
        print(f"配置文件不存在，正在创建: {config_path}")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)  # type: ignore[arg-type]
        print("默认配置文件创建成功")
    else:
        print(f"配置文件已存在: {config_path}")
    
    return config_path
