import pytest

from config import ConfigurationError, load_config


def test_load_config_resolves_relative_output_dir(tmp_path):
    values = {
        "GEMINI_API_KEY": "secret",
        "CHANNEL_NAME": "Channel",
        "CHANNEL_DESCRIPTION": "Description",
        "VIDEO_OUTPUT_DIR": "finished_videos",
        "VIDEO_MODEL": "video",
        "VIDEO_FALLBACK_MODEL": "fallback",
    }
    config = load_config(values, tmp_path)
    assert config.output_dir == tmp_path / "finished_videos"


def test_load_config_reports_missing_values():
    with pytest.raises(ConfigurationError, match="GEMINI_API_KEY"):
        load_config({}, "/tmp")
