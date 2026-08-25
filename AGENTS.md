# Repository Instructions

## Scope and Flow

- This is a Python CLI for German product/sales videos: `research_trends()` -> `generate_sales_script()` -> `generate_video_with_veo()` -> `generate_metadata()` -> output QA/manifest.
- Main code is `productvideo_generator.py`; tests are in `tests/test_productvideo_generator.py`.
- Veo generates the complete video, including voice and music. Do not add FFmpeg, external TTS, or audio-mixing pipelines.
- Trends remain DACH-focused (`geo='DE'`), and external API failures should use existing fallback paths.
- Outputs are `<normalized_topic>_script.txt`, `<normalized_topic>.mp4`, `<normalized_topic>_meta.json`, and `<normalized_topic>_run.json`.

## Commands and CI

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux; use .venv/Scripts/activate on Windows
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- `./ci.sh` is the primary local check. It installs development dependencies and Ruff, then runs imports, Ruff, compileall, pytest with coverage, pip-audit, and `python -m pymarkdown -c .pymarkdown.toml scan .`.
- Direct checks: `python -m ruff check productvideo_generator.py`, `python -m compileall productvideo_generator.py`, and `python -m pytest -q`.
- Focused example: `python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file`.
- `./run.sh "Smarte Kaffeemaschine"` performs an end-to-end API run, not a unit test.
- CI uses Python 3.12 and 3.13. Unit tests use dummy Gemini, Veo, and trend clients; do not add live network calls.

## Configuration Gotchas

- Required `.env`: `GEMINI_API_KEY`, `CHANNEL_NAME`, `CHANNEL_DESCRIPTION`, `VIDEO_OUTPUT_DIR`, `VIDEO_MODEL`, and `VIDEO_FALLBACK_MODEL`.
- Optional `.env`: `VIDEO_MAX_SECONDS`, `VIDEO_ASPECT_RATIO`, and `VIDEO_RESOLUTION`.
- `SCRIPT_MODEL` is currently hardcoded in `productvideo_generator.py` as `gemini-3-pro-preview`; do not add an env override without changing code and tests together.
- Read `.github/copilot-instructions.md` before changing prompts: output is German, sales-oriented, and uses short visual cues in parentheses.

## Safety

- Never commit `.env` or credentials. Keep generated outputs under `VIDEO_OUTPUT_DIR` and preserve normalized topic naming.
- Keep tests deterministic and reuse existing dummy-client patterns. Add tests for parsing, configuration, pipeline, QA, or manifest behavior changes.
- Make focused changes; update README/CONTRIBUTING when commands or behavior change.
