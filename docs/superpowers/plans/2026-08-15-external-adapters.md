# External Adapter Seams Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hide external trend, Gemini/Veo, and artifact operations behind injectable adapters without changing user-visible behavior.

**Architecture:** Add a focused adapter module with small protocols and production implementations. The generator receives optional adapters and keeps current defaults, retry behavior, and output contracts.

**Tech Stack:** Python 3.10+, pytest, existing `google-genai`, `pytrends`, and filesystem code.

## Global Constraints

- No new runtime dependencies.
- No real network calls in tests.
- Preserve German user-facing output and existing fallback behavior.
- Preserve CLI, manifest schema, output filenames, and current external SDK usage.

### Task 1: Product video adapter contracts

**Files:**
- Create: `adapters.py`
- Test: `tests/test_adapters.py`

- [ ] Write failing tests for injected trend, text, video, and artifact adapters.
- [ ] Run `python -m pytest -q tests/test_adapters.py` and confirm failure because the adapter module/contracts do not exist.
- [ ] Implement the smallest protocols and in-memory test-compatible contracts; keep production SDK construction out of the protocols.
- [ ] Run the focused test and confirm it passes.

### Task 2: Product video wiring

**Files:**
- Modify: `productvideo_generator.py`
- Modify: `tests/test_productvideo_generator.py`

- [ ] Add a failing test that constructs `ProductVideoGenerator` with injected adapters and verifies trend/text/video calls are used.
- [ ] Run the focused test and confirm it fails against direct SDK/global access.
- [ ] Add optional constructor dependencies and production defaults; route `research_trends`, `generate_sales_script`, video generation, and artifact writes through adapters without changing fallback semantics.
- [ ] Run `python -m pytest -q tests/test_adapters.py tests/test_productvideo_generator.py`.

### Task 3: Podcast adapter contracts and wiring

**Files:**
- Create: `adapters.py`
- Test: `tests/test_adapters.py`
- Modify: `podcast_generator.py`

- [ ] Write failing tests for injected trend, text, music, speech, media, and artifact adapters.
- [ ] Run the focused tests and confirm failure before production changes.
- [ ] Implement protocols and route the corresponding generator methods through injected adapters while retaining current retry and fallback behavior.
- [ ] Run `python -m pytest -q tests/test_adapters.py tests/test_pipeline_integration.py tests/test_helpers.py`.

### Task 4: Full verification

**Files:**
- Modify: `README.md` only if the injection seam needs documentation.

- [ ] Run both projects' full test suites with `python -m pytest -q`.
- [ ] Run `python -m compileall` and Ruff checks in both repositories.
- [ ] Review the diff for accidental CLI, schema, secret, or dependency changes.
