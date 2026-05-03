"""
配置管理模块
提供配置的创建、加载和全局访问功能
"""
from core.config.load_config import config, get_config, save_config
from core.config.create_config import create_default_config
from core.app_info import CONFIG_PATH

__all__ = ['config', 'get_config', 'save_config', 'create_default_config', 'CONFIG_PATH']
