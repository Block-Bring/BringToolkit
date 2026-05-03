"""
加载和管理全局配置
提供一个全局配置对象，让整个软件都能访问配置
"""
import json
import os
from core.app_info import CONFIG_PATH
from core.logger import logger


class ConfigManager:
    """配置管理器 - 单例模式"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """确保只有一个配置管理器实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self, config_path=None):
        """加载配置文件"""
        if config_path is None:
            config_path = CONFIG_PATH
            
        if not os.path.exists(config_path):
            # 如果配置文件不存在，先创建默认配置
            from core.config.create_config import create_default_config
            create_default_config(config_path)
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            logger.info(f"配置加载成功: {config_path}")  # type: ignore
        except Exception as e:
            logger.error(f"配置加载失败: {e}，使用默认配置")  # type: ignore
            # 使用默认配置
            self._config = {
                "minecraft_directory": "",
                "settings": {
                    "check_update": True,
                    "insider_preview": False
                }
            }
    
    def get(self, key, default=None):
        """
        获取配置值
        
        参数:
            key: 配置键名，支持点号分隔的嵌套键，如 "settings.check_update"
            default: 默认值，当配置不存在时返回
        
        返回:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """
        设置配置值
        
        参数:
            key: 配置键名，支持点号分隔的嵌套键，如 "settings.check_update"
            value: 配置值
        """
        keys = key.split('.')
        config = self._config
        
        # 导航到倒数第二层
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置最后一层的值
        config[keys[-1]] = value
    
    def save(self, config_path=None):
        """
        保存配置到文件
        
        参数:
            config_path: 配置文件路径，默认使用 core.app_info.CONFIG_PATH
        """
        if config_path is None:
            config_path = CONFIG_PATH
            
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
            logger.info(f"配置已保存: {config_path}")  # type: ignore
            return True
        except Exception as e:
            logger.error(f"配置保存失败: {e}")  # type: ignore
            return False
    
    def to_dict(self):
        """返回配置的字典副本"""
        return self._config.copy()


# 创建全局配置实例（单例）
config = ConfigManager()


def get_config(key, default=None):
    """
    便捷函数：获取配置值
    
    用法:
        from core.config import get_config
        
        check_update = get_config("settings.check_update")
        mc_dir = get_config("minecraft_directory", "/default/path")
    """
    return config.get(key, default)


def save_config():
    """
    便捷函数：保存配置
    
    用法:
        from core.config import save_config
        
        config.set("settings.check_update", False)
        save_config()
    """
    return config.save()
