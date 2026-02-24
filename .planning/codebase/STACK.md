# Technology Stack

**Analysis Date:** 2026-02-24

## Languages

**Primary:**
- Python 3.10+ - main runtime for generator in `productvideo_generator.py`, test harness in `tests/test_productvideo_generator.py`

**Secondary:**
- Shell (bash) - automation scripts in `run.sh`, `setup.sh`, `ci.sh`

## Runtime

**Environment:**
- CPython 3.10+ (CI uses 3.13 in `.github/workflows/ci.yml`)

**Package Manager:**
- pip (invoked in `run.sh`, `setup.sh`, `ci.sh`)
- Lockfile: missing (no `poetry.lock` / `Pipfile.lock` detected; `requirements.txt` used)

## Frameworks

**Core:**
- Google GenAI SDK (`google-genai`) - Gemini/Veo client usage in `productvideo_generator.py`
- pytrends - Google Trends access in `productvideo_generator.py`
- python-dotenv - .env loading in `productvideo_generator.py`

**Testing:**
- pytest - test runner in `tests/test_productvideo_generator.py`, CI in `.github/workflows/ci.yml`

**Build/Dev:**
- ruff - linting in `ci.sh` and `.github/workflows/ci.yml`
- mdformat - markdown linting in `ci.sh`

## Key Dependencies

**Critical:**
- `google-genai` - required to call Gemini text and Veo video models in `productvideo_generator.py`
- `pytrends` - required for trend lookup in `productvideo_generator.py`
- `python-dotenv` - required for config loading in `productvideo_generator.py`

**Infrastructure:**
- `pytest` - required for local/CI tests in `tests/test_productvideo_generator.py`

## Configuration

**Environment:**
- Config is read from `.env` or OS env via `dotenv.load_dotenv` in `productvideo_generator.py`
- Required vars: `GEMINI_API_KEY`, `CHANNEL_NAME`, `CHANNEL_DESCRIPTION`, `VIDEO_OUTPUT_DIR` (enforced in `productvideo_generator.py` and documented in `CONTRIBUTING.md`)
- Optional vars: `VIDEO_MODEL`, `VIDEO_MAX_SECONDS`, `VIDEO_ASPECT_RATIO`, `VIDEO_RESOLUTION` in `productvideo_generator.py`
- Example env template exists at `.env.example` (do not read `.env`)

**Build:**
- CI defined in `.github/workflows/ci.yml`
- Local automation: `ci.sh`, `setup.sh`, `run.sh`

## Platform Requirements

**Development:**
- Python 3.10+ with venv support (`README.md`, `CONTRIBUTING.md`)
- Bash-capable shell for scripts (`run.sh`, `setup.sh`, `ci.sh`)

**Production:**
- Scripted local execution of `productvideo_generator.py` via `run.sh` (outputs to `VIDEO_OUTPUT_DIR`)

---

*Stack analysis: 2026-02-24*
