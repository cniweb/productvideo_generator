# AGENTS.md

Repository guidance for agentic coding assistants working on
`productvideo_generator`.

## 1) Quick project context

- Project: Product Video Generator (Veo Edition)
- Language/runtime: Python 3.10+
- Main entrypoint: `productvideo_generator.py`
- Main test file: `tests/test_productvideo_generator.py`
- Core flow: `research_trends()` -> `generate_sales_script()` ->
  `generate_video_with_veo()` -> `generate_metadata()`
- Output artifacts per topic:
  - `<normalized_topic>_script.txt`
  - `<normalized_topic>.mp4`
  - `<normalized_topic>_meta.json`

## 2) Setup and local commands

### Environment setup

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Build/lint/test commands (use these first)

- Install deps: `python -m pip install -r requirements.txt`
- Lint target used in CI: `python -m ruff check productvideo_generator.py`
- Compile/syntax check: `python -m compileall productvideo_generator.py`
- Run full tests: `python -m pytest -q`
- Run a single test (important):
  `python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file`
- Run local CI helper script: `./ci.sh`
- End-to-end run: `./run.sh "Smarte Kaffeemaschine"`

### Notes about `ci.sh`

- Creates and activates `.venv` if needed.
- Runs `ruff check --fix` and then `ruff check`.
- Runs markdown format check via `mdformat --check **/*.md`.
- Runs import sanity check and then pytest.

## 3) CI behavior

- Workflow file: `.github/workflows/ci.yml`
- CI runs on Ubuntu with Python 3.13.
- CI installs `ruff==0.6.8`.
- CI sequence: install deps -> static import check -> ruff -> compileall -> pytest.
- Keep local changes compatible with both local scripts and CI workflow behavior.

## 4) Environment variables and config

Required env vars:

- `GEMINI_API_KEY`
- `CHANNEL_NAME`
- `CHANNEL_DESCRIPTION`
- `VIDEO_OUTPUT_DIR`

Optional env vars:

- `VIDEO_MODEL`
- `VIDEO_MAX_SECONDS`
- `VIDEO_ASPECT_RATIO`
- `VIDEO_RESOLUTION`

Rules:

- Never hardcode secrets.
- Never commit `.env` or credentials.
- Keep `.env`-driven configuration model intact.

## 5) Copilot rules (from `.github/copilot-instructions.md`)

These are repository rules and must be preserved in code changes:

- User-facing content should be German by default.
- Script style is sales/conversion focused (Hook, Solution, Benefits, CTA).
- Script output should be spoken prose with short visual cues in parentheses.
- Scope is product/sales video generation (not podcast flow).
- Do not add ffmpeg or external TTS/mixing pipelines.
- Keep trend behavior DACH-focused (current implementation uses `geo='DE'`).
- Prefer resilient fallback behavior for external API outages/errors.

## 6) Cursor rules status

- No Cursor rules were found in `.cursor/rules/`.
- No `.cursorrules` file was found.

## 7) Code style guidelines

### Imports

- Standard library imports first, third-party second, local imports last.
- Keep one import per line when practical.
- Avoid wildcard imports.
- Prefer explicit imports and stable ordering.

### Formatting

- Follow Ruff-compatible style.
- Use 4-space indentation.
- Prefer readable, small functions over large monoliths.
- Prefer f-strings for interpolation.
- Keep multiline calls/dicts formatted consistently, with trailing commas where useful.

### Types

- Type hints are optional in this repo.
- Add type hints only when they improve clarity and maintenance.
- Avoid heavy/complex typing patterns that reduce readability.

### Naming conventions

- Classes: `CamelCase`
- Functions/methods/variables: `snake_case`
- Constants/module-level fixed values: `UPPER_SNAKE_CASE`
- Use descriptive names for prompts, outputs, and filesystem paths.

### Error handling and resilience

- Raise `RuntimeError` for user-visible or critical pipeline failures.
- Keep best-effort behavior for external services (Gemini/Veo/pytrends).
- Log/print actionable warnings for fallback paths.
- Do not silently swallow exceptions unless there is an intentional fallback.

### I/O and output files

- Write generated artifacts under `VIDEO_OUTPUT_DIR`.
- Preserve normalized topic naming convention for script/video/metadata files.
- Use UTF-8 for text/json writes.

## 8) Testing guidance

- Framework: `pytest`
- Tests should be deterministic and isolated.
- Do not make live network/API calls in unit tests.
- Reuse existing dummy client/stub pattern from `tests/test_productvideo_generator.py`.
- Add or update tests whenever behavior changes in parsing, config, or pipeline flow.

## 9) Change scope and git hygiene

- Keep changes minimal and focused on the requested task.
- Do not refactor unrelated areas “while you are here”.
- Update docs when commands, behavior, or conventions change.
- Avoid introducing new dependencies unless clearly justified.

## 10) Useful files for fast orientation

- `productvideo_generator.py`
- `tests/test_productvideo_generator.py`
- `README.md`
- `CONTRIBUTING.md`
- `ci.sh`
- `run.sh`
- `.github/copilot-instructions.md`
- `.github/workflows/ci.yml`

## 11) Practical agent workflow (recommended)

1. Read this file and `.github/copilot-instructions.md`.
2. Make the smallest possible code change for the task.
3. Run at least targeted tests; run full `pytest -q` for broader changes.
4. Run lint/compile checks before finishing.
5. Report what changed, what was tested, and any follow-up risk.

## 12) Context7 via MCP/Tool (recommended)

- Use Context7 via MCP/Tool for third-party library documentation before changing
  integration code.
- Prefer this for `google-genai`, `pytrends`, `pytest`, and `python-dotenv`
  related work.
- Do not guess method names, parameter names, or response fields when Context7 can
  provide current docs.

Suggested usage pattern:

1. Resolve the library ID first in Context7.
2. Query task-specific docs (include Python version and exact use case).
3. Apply the smallest possible code change aligned with repository conventions.
4. Add or update deterministic tests if API behavior/signatures are affected.
5. Mention the doc-driven rationale briefly in the final report/PR text.

## 13) Firecrawl via MCP/Tool (recommended)

Use Firecrawl via MCP/Tool for web research tasks during agent-driven
development or prompt enrichment work. Do NOT add Firecrawl as a runtime
dependency to `requirements.txt`.

Useful scenarios in this project:

- **Product research**: Scrape manufacturer or shop pages to extract
  product features, USPs, or pricing before refining the Gemini prompt
  in `generate_sales_script()`.
- **Trend fallback**: If `pytrends` fails due to rate limiting (HTTP 429),
  use Firecrawl to scrape Google Trends or DACH news sources for current
  trend signals.
- **Competitor context**: Extract structured product data from competitor
  pages to enrich the sales script with concrete comparisons.
- **Documentation lookup**: Scrape API docs or changelogs not covered by
  Context7 (e.g., Veo release notes, Gemini model capability pages).

Guardrails:

- Firecrawl is an agent/research tool only — not a runtime dependency.
- Do not replace `pytrends` with Firecrawl in production code; use it
  as a best-effort fallback signal during agent research phases only.
- Scraped content fed into Gemini prompts must stay within token limits.
- Respect robots.txt and site terms of service.
- Keep DACH focus: prefer German-language sources (`.de`, `google.de`).
