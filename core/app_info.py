APP_NAME = "Bring Toolkit"
APP_VERSION = "1.0.0a3"  # 内部版本号，用于比较和存储
CONFIG_PATH = "config.json"
LATEST_LOG_PATH = "latest.log"  # 最新日志文件路径


def format_version_display(version: str) -> str:
    """
    将内部版本号转换为友好的显示格式
    
    例如:
        1.0.0a1   -> 1.0.0 Alpha 1
        1.0.0b2   -> 1.0.0 Beta 2
        1.0.0rc3  -> 1.0.0 RC 3
        1.0.0     -> 1.0.0
    """
    import re
    
    # 匹配版本号模式：主版本号 + 预发布类型 + 预发布编号
    pattern = r'^(\d+\.\d+\.\d+)(a|alpha|b|beta|rc|preview)(\d+)$'
    match = re.match(pattern, version, re.IGNORECASE)
    
    if match:
        base_version = match.group(1)  # 主版本号 (如 1.0.0)
        pre_type = match.group(2).lower()  # 预发布类型 (如 a, alpha, b, beta, rc)
        pre_num = match.group(3)  # 预发布编号 (如 1, 2, 3)
        
        # 转换预发布类型为友好名称
        type_map = {
            'a': 'Alpha',
            'alpha': 'Alpha',
            'b': 'Beta',
            'beta': 'Beta',
            'rc': 'RC',
            'preview': 'Preview'
        }
        
        friendly_type = type_map.get(pre_type, pre_type)
        return f"{base_version} {friendly_type} {pre_num}"
    else:
        # 如果不是预发布版本，直接返回
        return version

APP_VERSION_DISPLAY = format_version_display(APP_VERSION)