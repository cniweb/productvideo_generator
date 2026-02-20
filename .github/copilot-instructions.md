# copilot-instructions

## Build, test, and lint commands

- Install deps: `python -m pip install -r requirements.txt`
- Lint (same target as CI): `python -m ruff check productvideo_generator.py`
- Compile/syntax check: `python -m compileall productvideo_generator.py`
- Full test suite: `python -m pytest -q`
- Single test: `python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file`
- Combined local CI flow: `./ci.sh`
- End-to-end run: `./run.sh "Smarte Kaffeemaschine"`

## High-level architecture

- Single main module: `productvideo_generator.py` contains configuration loading, Gemini client setup, and the full generation pipeline.
- Runtime flow is orchestrated by `ProductVideoGenerator` in four steps:
  1. `research_trends()` (Google Trends via `pytrends`, currently geo `DE`)
  2. `generate_sales_script()` (Gemini text model for sales script)
  3. `generate_video_with_veo()` (Veo async video generation, optional extension loop)
  4. `generate_metadata()` (Gemini text model to JSON metadata)
- Config is lazily initialized through `_initialize_config()` and loaded from `.env`/environment variables (`GEMINI_API_KEY`, `CHANNEL_NAME`, `CHANNEL_DESCRIPTION`, `VIDEO_OUTPUT_DIR`, optional video settings).
- File outputs are written to `VIDEO_OUTPUT_DIR` with stable naming based on normalized topic:
  - `<topic>_script.txt`
  - `<topic>.mp4`
  - `<topic>_meta.json`
- Shell scripts:
  - `setup.sh`: env/dependency bootstrap
  - `run.sh`: standard execution entrypoint for manual runs
  - `ci.sh`: local lint/import/syntax/tests sequence aligned with `.github/workflows/ci.yml`

## Key repository conventions

- User-visible content is German by default (scripts, titles, descriptions, console messages).
- Script prompt style is sales/conversion focused and should keep explicit CTA coverage.
- Script text should remain mostly spoken prose, with short visual cues in parentheses for Veo prompting.
- Pipeline scope is product/sales videos (not podcast flow).
- Do not introduce ffmpeg or external TTS/mixing; audio/music/video generation is expected from Veo.
- Preserve `.env`-driven config; never hardcode secrets.
- Trend focus should stay DACH-oriented (existing implementation queries Germany with `geo='DE'`).
- Prefer resilient behavior for upstream API issues where already established (e.g., trend lookup fallback, optional video-model fallback path).
