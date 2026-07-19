"""
检查更新模块
从 GitHub 上的 latest/core/app_latest.json 获取最新版本信息，
与本地 APP_VERSION 比较，判断是否需要更新。
"""

from dataclasses import dataclass

from packaging import version

from core.app_info import APP_VERSION, GITHUB_RAW_BASE
from utils.downloader import fetch_json
from utils.logger import logger

UPDATE_URL = f"{GITHUB_RAW_BASE}/latest/core/app_latest.json"
EXPECTED_FORMAT_VERSION = 4


@dataclass
class CheckResult:
    """更新检查结果"""

    has_update: bool = False
    latest_version: str | None = None
    download_url: str | None = None
    error: str | None = None
    is_stable: bool = True
    format_mismatch: bool = False
    error_404: bool = False


def _resolve_download_url(url_data) -> str | None:
    """解析下载 URL（兼容新旧格式）"""
    if isinstance(url_data, dict):
        try:
            keys = sorted(url_data.keys(), key=lambda x: int(x) if x.isdigit() else 999)
            for key in keys:
                url = url_data.get(key, "")
                if url:
                    return url
        except (ValueError, TypeError):
            return next(iter(url_data.values()), None)
    elif isinstance(url_data, str):
        return url_data or None
    return None


def check_for_updates(insider_preview=False) -> CheckResult:
    """
    联网检查是否有新版本（仅执行检查逻辑，不显示任何 UI）。

    参数:
        insider_preview: 是否检查 Insider Preview 版本

    返回:
        CheckResult 对象
    """
    logger.info(f"正在检查更新... 当前版本：{APP_VERSION}")
    logger.info(f"检查类型：{'Insider Preview' if insider_preview else '稳定版'}")

    data, error = fetch_json(UPDATE_URL)
    if error:
        if error == "not_found":
            logger.warning("未找到更新配置文件")
            return CheckResult(
                error="未找到更新配置文件，请手动从 GitHub Releases 下载最新版本。", error_404=True
            )
        logger.error(f"检查更新失败：{error}")
        return CheckResult(error=error)

    # 检查 format_version
    format_version = data.get("format_version", 1)
    if format_version != EXPECTED_FORMAT_VERSION:
        logger.warning(
            f"格式版本不匹配：本地支持 {EXPECTED_FORMAT_VERSION}，线上为 {format_version}"
        )
        return CheckResult(
            format_mismatch=True,
            error=(
                "远程更新配置文件格式版本与本地不兼容，请尝试手动更新。\n"
                f"（本地: {EXPECTED_FORMAT_VERSION}, 线上: {format_version}）"
            ),
        )

    # 根据是否检查预览版，选择不同的分支
    if insider_preview:
        update_info = data.get("insider_preview", {})
        result = CheckResult(is_stable=False)
    else:
        update_info = data.get("stable", {})
        result = CheckResult(is_stable=True)

    online_version = update_info.get("version", "")
    url_data = update_info.get("url", {})

    # 如果版本号为空，说明没有可用的版本信息
    if not online_version:
        logger.info("没有可用的版本信息")
        return result

    url = _resolve_download_url(url_data)
    logger.info(f"线上版本：{online_version}")

    # 使用智能版本号比较（支持 1.0.0, 1.0.0a1, 1.0.0b2 等格式）
    try:
        local_ver = version.parse(APP_VERSION)
        online_ver = version.parse(online_version)
        has_update = online_ver > local_ver
    except Exception as e:
        logger.warning(f"版本号解析失败 ({e})，使用字符串比较")
        has_update = online_version != APP_VERSION

    if has_update:
        logger.info("发现新版本！")
    else:
        logger.info("已是最新版本。")

    result.has_update = has_update
    result.latest_version = online_version
    result.download_url = url
    return result
