"""
注意：这是 AI 智能体生成的
配置系统使用示例
展示如何在项目的任何地方访问和修改配置
"""

# ===== 示例1：在任何地方读取配置 =====
def example_read_config():
    """示例：读取配置"""
    from core.config import config
    
    # 读取单个配置项
    check_update = config.get("settings.check_update")
    print(f"启动时检查更新: {check_update}")
    
    mc_dir = config.get("minecraft_directory", "")
    print(f"Minecraft 目录: {mc_dir}")
    
    # 读取时提供默认值
    some_value = config.get("non_existent_key", "默认值")
    print(f"不存在的键: {some_value}")


# ===== 示例2：使用便捷函数读取 =====
def example_get_config():
    """示例：使用便捷函数"""
    from core.config import get_config
    
    # 更简洁的写法
    insider = get_config("settings.insider_preview")
    print(f"Insider Preview: {insider}")


# ===== 示例3：修改并保存配置 =====
def example_save_config():
    """示例：修改并保存配置"""
    from core.config import config, save_config
    
    # 修改配置（仅在内存中）
    config.set("settings.check_update", False)
    config.set("minecraft_directory", "C:/Games/Minecraft")
    
    # 保存到文件
    if save_config():
        print("配置已保存")
    else:
        print("保存失败")


# ===== 示例4：在程序启动时加载配置 =====
def example_app_startup():
    """示例：应用程序启动时的典型用法"""
    from core.config import config, CONFIG_PATH
    
    # 配置会自动加载，无需手动操作
    # 单例模式确保全局只有一个配置实例
    
    print(f"配置文件路径: {CONFIG_PATH}")
    
    # 可以直接使用
    if config.get("settings.check_update"):
        print("启动时应该检查更新")
    
    # 在整个应用中，任何地方获取的都是同一个配置对象
    from core.config import config as global_config
    assert config is global_config  # True - 是同一个对象


if __name__ == "__main__":
    print("=" * 50)
    print("配置系统使用示例")
    print("=" * 50)
    
    print("\n【示例1】读取配置:")
    example_read_config()
    
    print("\n【示例2】便捷函数:")
    example_get_config()
    
    print("\n【示例3】修改并保存:")
    example_save_config()
    
    print("\n【示例4】应用启动:")
    example_app_startup()
    
    print("\n" + "=" * 50)
    print("所有示例执行完成！")
