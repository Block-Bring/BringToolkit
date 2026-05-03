"""
检查更新模块
从 GitHub 上的 latest/app_latest.json 获取最新版本信息，
与本地 APP_VERSION 比较，判断是否需要更新。
"""
import requests
from packaging import version
from core.app_info import APP_VERSION, APP_NAME
from core.logger import logger


UPDATE_URL = (
    "https://ghfast.top/https://raw.githubusercontent.com/Block-Bring/BringToolkit/"
    "refs/heads/master/latest/app_latest.json"
)


def check_for_updates(insider_preview=False):
    """
    联网检查是否有新版本（仅执行检查逻辑，不显示任何 UI）。

    参数:
        insider_preview: bool, 是否检查 Insider Preview 版本

    返回值:
        dict - 包含更新信息的字典：
            {
                "has_update": bool,  # 是否有新版本
                "online_version": str or None,  # 线上版本号
                "url": str or None,  # 下载链接
                "error": str or None,  # 错误信息
                "is_stable": bool  # 是否为稳定版更新
            }
    """
    logger.info(f"正在检查更新... 当前版本：{APP_VERSION}")
    logger.info(f"检查类型：{'Insider Preview' if insider_preview else '稳定版'}")

    result = {
        "has_update": False,
        "online_version": None,
        "url": None,
        "error": None,
        "is_stable": True
    }

    try:
        response = requests.get(UPDATE_URL, timeout=10)

        if response.status_code != 200:
            error_msg = f"HTTP {response.status_code}"
            logger.error(f"检查更新失败：{error_msg}")
            result["error"] = error_msg
            return result

        data = response.json()
        
        # 根据是否检查预览版，选择不同的分支
        if insider_preview:
            update_info = data.get("insider_preview", {})
            online_version = update_info.get("version", "")
            url = update_info.get("url", "")
            has_new = update_info.get("has_insider_preview", False)
            result["is_stable"] = False
        else:
            update_info = data.get("stable", {})
            online_version = update_info.get("version", "")
            url = update_info.get("url", "")
            has_new = update_info.get("has_stable", False)
            result["is_stable"] = True

        # 如果版本号为空，说明没有可用的版本信息
        if not online_version:
            logger.info("没有可用的版本信息")
            return result

        logger.info(f"线上版本：{online_version}")
        logger.debug(f"has_new 标记: {has_new}")
        result["online_version"] = online_version
        result["url"] = url

        # 使用智能版本号比较（支持 1.0.0, 1.0.0a1, 1.0.0b2 等格式）
        try:
            local_ver = version.parse(APP_VERSION)
            online_ver = version.parse(online_version)
            
            if online_ver > local_ver:
                logger.info("发现新版本！")
                result["has_update"] = True
            else:
                logger.info("已是最新版本。")
        except Exception as e:
            # 如果版本号解析失败，回退到简单字符串比较
            logger.warning(f"版本号解析失败 ({e})，使用字符串比较")
            if online_version != APP_VERSION:
                logger.info("发现新版本！")
                result["has_update"] = True
            else:
                logger.info("已是最新版本。")

        return result

    except requests.exceptions.RequestException as e:
        error_msg = f"网络错误 - {e}"
        logger.error(f"检查更新失败：{error_msg}")
        result["error"] = error_msg
        return result
    except Exception as e:
        error_msg = f"未知错误 - {e}"
        logger.error(f"检查更新失败：{error_msg}")
        result["error"] = error_msg
        return result
