# Coding Conventions

**Analysis Date:** 2026-02-24

## Naming Patterns

**Files:**
- Single-module layout in repository root (no `src/`), main logic in `productvideo_generator.py`.
- Tests named with `test_*.py` in `tests/` (e.g., `tests/test_productvideo_generator.py`).

**Functions:**
- Use `snake_case` for functions (e.g., `_initialize_config`, `generate_sales_script` in `productvideo_generator.py`).
- Internal helpers prefixed with `_` to indicate module-private usage (e.g., `_require_env`, `_optional_int_env` in `productvideo_generator.py`).

**Variables:**
- Use `snake_case` for locals and instance attributes (e.g., `script_content`, `video_path` in `productvideo_generator.py`).
- Constants are `UPPER_SNAKE_CASE` (e.g., `SCRIPT_MODEL`, `VIDEO_MODEL` in `productvideo_generator.py`).

**Types:**
- No enforced typing; type hints are not used in `productvideo_generator.py`.

## Code Style

**Formatting:**
- Follow Ruff defaults; formatting is enforced by lint step in `ci.sh` and `.github/workflows/ci.yml`.
- Use 4-space indentation (consistent across `productvideo_generator.py`).

**Linting:**
- Ruff is the primary linter (`python -m ruff check productvideo_generator.py`) as shown in `ci.sh` and `.github/workflows/ci.yml`.
- Avoid wildcard imports; use explicit imports (see `productvideo_generator.py`).

## Import Organization

**Order:**
1. Standard library imports first (e.g., `import os`, `import json`, `import time` in `productvideo_generator.py`).
2. Third-party imports next (e.g., `from pytrends.request import TrendReq`, `from google import genai`, `from dotenv import load_dotenv` in `productvideo_generator.py`).
3. No local module imports (single-file module).

**Path Aliases:**
- Not detected.

## Error Handling

**Patterns:**
- Raise `RuntimeError` for user-visible or critical failures (e.g., `_raise_env_error`, `generate_sales_script`, `_run_video_generation` in `productvideo_generator.py`).
- Use best-effort fallbacks and warning prints for external APIs (e.g., `research_trends` catches exceptions and continues; `_list_video_models` logs failures in `productvideo_generator.py`).
- For non-critical metadata parsing, fall back to defaults instead of failing (see `generate_metadata` in `productvideo_generator.py`).

## Logging

**Framework:** console `print` statements.

**Patterns:**
- Step-based progress logs with emoji prefixes (e.g., "🔍", "✍️", "🎬" in `productvideo_generator.py`).
- Warnings use "⚠️" and errors use "❌" in `productvideo_generator.py`.

## Comments

**When to Comment:**
- Use section dividers to denote pipeline stages (e.g., "# 1. TRENDS", "# 2. VERKAUFS-SKRIPT" in `productvideo_generator.py`).
- Keep inline comments focused on intent or fallback behavior (e.g., trend fallback notes in `productvideo_generator.py`).

**JSDoc/TSDoc:**
- Not applicable (Python codebase). Docstrings are used for functions and methods in `productvideo_generator.py`.

## Function Design

**Size:**
- Methods are medium-sized with single responsibility per pipeline step (e.g., `research_trends`, `generate_sales_script`, `generate_video_with_veo`, `generate_metadata` in `productvideo_generator.py`).

**Parameters:**
- Prefer explicit parameters and dependency injection via module globals for external clients (e.g., `client` assigned in `_initialize_config`, used in `ProductVideoGenerator`).

**Return Values:**
- Return domain values where useful (`research_trends` returns topic string in `productvideo_generator.py`), otherwise rely on side effects (file writes and instance fields).

## Module Design

**Exports:**
- Single module `productvideo_generator.py` with top-level helpers and a single main class `ProductVideoGenerator`.

**Barrel Files:**
- Not applicable.

---

*Convention analysis: 2026-02-24*
