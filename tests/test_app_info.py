"""测试 app_info 模块"""
from core.app_info import format_version_display


def test_format_version_display_alpha():
    assert format_version_display("1.0.0a1") == "1.0.0 Alpha 1"


def test_format_version_display_alpha_long():
    assert format_version_display("1.0.0alpha2") == "1.0.0 Alpha 2"


def test_format_version_display_beta():
    assert format_version_display("2.1.0b3") == "2.1.0 Beta 3"


def test_format_version_display_rc():
    assert format_version_display("3.0.0rc1") == "3.0.0 RC 1"


def test_format_version_display_release():
    assert format_version_display("1.0.0") == "1.0.0"


def test_format_version_display_preview():
    assert format_version_display("1.0.0preview5") == "1.0.0 Preview 5"
