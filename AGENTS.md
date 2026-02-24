# AGENTS.md
# Guardrails and repo guidance for coding agents

This file summarizes how to work in this repository.
It is intended for AI agents and human contributors.

## Quick repo context
- Project: Product Video Generator (Veo Edition)
- Language: Python
- Main entrypoint: `productvideo_generator.py`
- Tests: `tests/test_productvideo_generator.py`
- Primary flow: trends -> script -> video -> metadata

## Commands: build, lint, test
- Install deps: `python -m pip install -r requirements.txt`
- Lint (same target as CI): `python -m ruff check productvideo_generator.py`
- Compile/syntax check: `python -m compileall productvideo_generator.py`
- Full test suite: `python -m pytest -q`
- Single test: `python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file`
- Combined local CI flow: `./ci.sh`
- End-to-end run: `./run.sh "Smarte Kaffeemaschine"`

## Setup flow
- Create venv: `python -m venv .venv`
- Activate (Windows Git Bash): `source .venv/Scripts/activate`
- Upgrade pip: `python -m pip install --upgrade pip`
- Install deps: `python -m pip install -r requirements.txt`
- Copy env template: `cp .env.example .env` (then fill in keys)
- Run end-to-end: `./run.sh "Smarte Kaffeemaschine"`

## Copilot instructions (must follow)
These rules are from `.github/copilot-instructions.md`.
- Keep user-facing content in German by default.
- Keep script style sales/conversion oriented (Hook, Solution, Benefits, CTA).
- Script text should be spoken prose with short visual cues in parentheses.
- Pipeline scope is product/sales videos (not podcast flow).
- Do not introduce ffmpeg or external TTS/mixing; Veo handles audio/music/video.
- Keep trend behavior DACH-focused (geo='DE').
- Preserve `.env`-driven config; never hardcode secrets.
- Prefer resilient fallback behavior for external API issues.

## Cursor rules
- No Cursor rules found in `.cursor/rules/` or `.cursorrules`.

## Project structure and runtime flow
- `productvideo_generator.py` contains configuration loading, client setup, and the pipeline.
- The main class is `ProductVideoGenerator`.
- Steps:
  1) `research_trends()` using Google Trends (pytrends, geo DE)
  2) `generate_sales_script()` using Gemini text model
  3) `generate_video_with_veo()` using Veo video model
  4) `generate_metadata()` to JSON

## Environment configuration
Required environment variables (via `.env` or OS env):
- `GEMINI_API_KEY`
- `CHANNEL_NAME`
- `CHANNEL_DESCRIPTION`
- `VIDEO_OUTPUT_DIR`
Optional video settings:
- `VIDEO_MODEL`
- `VIDEO_MAX_SECONDS`
- `VIDEO_ASPECT_RATIO`
- `VIDEO_RESOLUTION`
Never commit secrets or `.env`.

## Output files
- Outputs are written to `VIDEO_OUTPUT_DIR`.
- File naming is based on normalized topic:
  - `<topic>_script.txt` (sales script)
  - `<topic>.mp4` (generated video)
  - `<topic>_meta.json` (metadata)

## Code style guidelines
### Imports
- Use standard library imports first, then third-party, then local modules.
- One import per line, no wildcard imports.
- Keep import ordering stable; prefer explicit imports.

### Formatting
- Follow Ruff defaults; keep line lengths reasonable.
- Use 4-space indentation.
- Prefer f-strings for string interpolation.
- Use trailing commas in multi-line calls or dicts when it improves diffs.

### Types
- This codebase does not enforce static typing.
- Add type hints only when they improve clarity and are low-maintenance.
- Avoid introducing complex typing just for formality.

### Naming conventions
- Classes: `CamelCase`.
- Functions/variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Use descriptive names for prompts, outputs, and file paths.

### Error handling
- Raise `RuntimeError` for user-visible failures or critical pipeline failures.
- For external services (pytrends, Gemini/Veo), prefer best-effort behavior:
  fall back when possible and log a helpful warning.
- Avoid swallowing errors silently unless there is an explicit fallback path.

### Files and output
- Output files are written to `VIDEO_OUTPUT_DIR`.
- Naming is based on normalized topic:
  - `<topic>_script.txt`
  - `<topic>.mp4`
  - `<topic>_meta.json`

## Testing guidance
- Tests use pytest and a dummy client for API stubs.
- Avoid network calls in tests.
- When adding tests, keep them deterministic and file-system isolated.

## Linting guidance
- Ruff is the primary linter (see CI and `ci.sh`).
- CI pins Ruff `0.6.8` in `ci.sh` and `.github/workflows/ci.yml`.
- Keep code compatible with Python 3.10+.

## CI notes
- CI runs lint, compile, and pytest on Ubuntu with Python 3.13.
- Static import sanity checks run for `google.genai`, `pytrends`, `dotenv`, `pytest`.

## Repository conventions
- German is the default language for user-visible content.
- Keep sales script structure: Hook, Solution, Benefits, CTA.
- Keep short visual cues in parentheses for Veo prompts.
- Do not add ffmpeg or external TTS/mixing tools.
- Keep trend behavior DACH-focused and resilient to API issues.

## Git hygiene
- Do not add or modify `.env` or secrets.
- Keep changes minimal and scoped.
- Update docs if commands or behavior change.

## Useful files
- `productvideo_generator.py`
- `tests/test_productvideo_generator.py`
- `run.sh`
- `ci.sh`
- `CONTRIBUTING.md`
- `.github/copilot-instructions.md`
- `.github/workflows/ci.yml`

## Notes for agents
- This repo is intentionally small; avoid adding unnecessary complexity.
- If you need a new dependency, justify it clearly in your change summary.
- Prefer code clarity and resilient error handling over cleverness.
