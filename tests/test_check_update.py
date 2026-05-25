"""测试 check_update 模块"""
from core.check_update import CheckResult, _resolve_download_url


class TestCheckResult:
    def test_default_values(self):
        result = CheckResult()
        assert result.has_update is False
        assert result.latest_version is None
        assert result.download_url is None
        assert result.error is None
        assert result.is_stable is True

    def test_custom_values(self):
        result = CheckResult(has_update=True, latest_version="2.0.0", download_url="https://example.com")
        assert result.has_update is True
        assert result.latest_version == "2.0.0"
        assert result.download_url == "https://example.com"


class TestResolveDownloadUrl:
    def test_dict_format(self):
        url_data = {"1": "https://example.com/v1", "2": "https://example.com/v2"}
        assert _resolve_download_url(url_data) == "https://example.com/v1"

    def test_dict_single(self):
        url_data = {"1": "https://example.com/v1"}
        assert _resolve_download_url(url_data) == "https://example.com/v1"

    def test_string_format(self):
        assert _resolve_download_url("https://example.com") == "https://example.com"

    def test_empty_dict(self):
        assert _resolve_download_url({}) is None

    def test_empty_string(self):
        assert _resolve_download_url("") is None

    def test_none(self):
        assert _resolve_download_url(None) is None
