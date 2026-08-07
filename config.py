from dataclasses import dataclass
from pathlib import Path
import os


class ConfigurationError(RuntimeError):
    """Raised when required product-video configuration is missing or invalid."""


@dataclass(frozen=True)
class ProductVideoConfig:
    gemini_api_key: str
    channel_name: str
    channel_description: str
    output_dir: Path
    video_model: str
    video_fallback_model: str


def load_config(env=None, base_dir=None):
    values = os.environ if env is None else env
    root = Path(base_dir or Path.cwd())
    required = {
        "gemini_api_key": "GEMINI_API_KEY",
        "channel_name": "CHANNEL_NAME",
        "channel_description": "CHANNEL_DESCRIPTION",
        "output_dir": "VIDEO_OUTPUT_DIR",
        "video_model": "VIDEO_MODEL",
        "video_fallback_model": "VIDEO_FALLBACK_MODEL",
    }
    missing = [key for key, name in required.items() if not values.get(name)]
    if missing:
        names = ", ".join(required[key] for key in missing)
        raise ConfigurationError(f"Fehlende Variablen: {names}")
    output_dir = Path(values["VIDEO_OUTPUT_DIR"])
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    return ProductVideoConfig(
        gemini_api_key=values["GEMINI_API_KEY"],
        channel_name=values["CHANNEL_NAME"],
        channel_description=values["CHANNEL_DESCRIPTION"],
        output_dir=output_dir,
        video_model=values["VIDEO_MODEL"],
        video_fallback_model=values["VIDEO_FALLBACK_MODEL"],
    )
