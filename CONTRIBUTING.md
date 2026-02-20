# Contributing to productvideo_generator

Thank you for contributing.

## Prerequisites

- Python 3.10+
- A valid `GEMINI_API_KEY` with access to Gemini/Veo models
- A configured `.env` file in the repository root

Required `.env` variables:

- `GEMINI_API_KEY`
- `CHANNEL_NAME`
- `CHANNEL_DESCRIPTION`
- `VIDEO_OUTPUT_DIR`

Optional video settings:

- `VIDEO_MODEL`
- `VIDEO_MAX_SECONDS`
- `VIDEO_ASPECT_RATIO`
- `VIDEO_RESOLUTION`

## Local setup

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Or use:

```bash
./setup.sh
```

## Run locally

```bash
./run.sh "Smarte Kaffeemaschine"
```

Without an explicit topic:

```bash
./run.sh
```

## Lint, compile, and test

Use the same checks as CI:

```bash
python -m ruff check productvideo_generator.py
python -m compileall productvideo_generator.py
python -m pytest -q
```

Run a single test:

```bash
python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file
```

Or run the combined local flow:

```bash
./ci.sh
```

## Repository-specific conventions

- Keep user-facing text in German (scripts, titles, descriptions).
- Keep script style sales/conversion oriented (Hook, Solution, Benefits, CTA).
- Keep visual cues in parentheses in the generated script where useful for Veo prompting.
- Do not add ffmpeg or external TTS/mixing: video, audio, and music are generated via Veo.
- Keep trend behavior DACH-focused (current implementation uses `geo='DE'` for trend lookup).
- Keep config `.env`-driven and never hardcode secrets.
- Prefer resilient fallback behavior for external API issues, especially around trend lookup and model availability.

## Pull request checklist

Before opening a PR:

1. Run lint + tests locally.
2. Keep changes minimal and scoped to the issue.
3. Update docs when behavior, commands, or configuration changed.
4. Include a clear summary of what changed and how it was validated.
