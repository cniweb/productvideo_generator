# Testing Patterns

**Analysis Date:** 2026-02-24

## Test Framework

**Runner:**
- pytest (invoked via `python -m pytest -q` in `ci.sh` and `.github/workflows/ci.yml`).
- Config: Not detected (no `pytest.ini`, `pyproject.toml`, or `setup.cfg` present).

**Assertion Library:**
- Built-in `assert` statements (see `tests/test_productvideo_generator.py`).

**Run Commands:**
```bash
python -m pytest -q              # Run all tests (see `ci.sh`)
python -m pytest -q tests/test_productvideo_generator.py::test_generate_sales_script_writes_file  # Single test
```

## Test File Organization

**Location:**
- Separate `tests/` directory at repository root (e.g., `tests/test_productvideo_generator.py`).

**Naming:**
- Test files named `test_*.py` and functions named `test_*` (see `tests/test_productvideo_generator.py`).

**Structure:**
```
tests/
└── test_productvideo_generator.py
```

## Test Structure

**Suite Organization:**
```python
def test_generate_sales_script_writes_file(tmp_path, monkeypatch):
    pv = _load_module(tmp_path, monkeypatch)
    pv.client = DummyClient(pv)
    gen = pv.ProductVideoGenerator("TestProdukt")
    gen.generate_sales_script()
    assert "Skripttext" in gen.script_content
```

**Patterns:**
- Use pytest fixtures `tmp_path` and `monkeypatch` for isolation and environment control (`tests/test_productvideo_generator.py`).
- Arrange-Act-Assert pattern within a single function (`tests/test_productvideo_generator.py`).

## Mocking

**Framework:**
- Manual test doubles (dummy classes) instead of mocking libraries.

**Patterns:**
```python
class DummyClient:
    def __init__(self, pv):
        self.models = DummyModels(pv)
        self.operations = DummyOperations()
        self.files = DummyFiles()

pv.client = DummyClient(pv)
```

**What to Mock:**
- External services (`google.genai`, `pytrends`) are replaced with dummy implementations (e.g., `DummyClient`, `DummyTrendReq` in `tests/test_productvideo_generator.py`).

**What NOT to Mock:**
- File system interactions are real but isolated to `tmp_path` (e.g., script/video/metadata file writes in `tests/test_productvideo_generator.py`).

## Fixtures and Factories

**Test Data:**
```python
def _load_module(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("CHANNEL_NAME", "Test Channel")
    monkeypatch.setenv("CHANNEL_DESCRIPTION", "Test Desc")
    monkeypatch.setenv("VIDEO_OUTPUT_DIR", str(tmp_path))
```

**Location:**
- Local helper and dummy classes are defined in `tests/test_productvideo_generator.py`.

## Coverage

**Requirements:** None enforced (no coverage config detected).

**View Coverage:**
```bash
Not configured
```

## Test Types

**Unit Tests:**
- Focus on single pipeline steps and file outputs (e.g., `test_generate_sales_script_writes_file` in `tests/test_productvideo_generator.py`).

**Integration Tests:**
- Light integration over file system + dummy external clients (e.g., `test_generate_video_with_veo_writes_video` in `tests/test_productvideo_generator.py`).

**E2E Tests:**
- Not used (no E2E framework detected).

## Common Patterns

**Async Testing:**
- Not used (async not present in tests).

**Error Testing:**
- Not explicit; tests focus on successful paths and fallbacks (e.g., `test_research_trends_fallback` in `tests/test_productvideo_generator.py`).

---

*Testing analysis: 2026-02-24*
