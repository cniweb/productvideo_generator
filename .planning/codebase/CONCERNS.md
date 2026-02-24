# Codebase Concerns

**Analysis Date:** 2026-02-24

## Tech Debt

**Global mutable configuration/state:**
- Issue: Module-level globals (`GEMINI_API_KEY`, `CHANNEL_NAME`, `OUTPUT_DIR`, `client`, `_initialized`) are mutated at runtime and relied on by instance methods, making behavior order-dependent and harder to test.
- Files: `productvideo_generator.py`
- Impact: Harder to reason about multi-run or concurrent usage; tests must monkeypatch globals carefully; hidden coupling between functions.
- Fix approach: Encapsulate config/client in a dedicated config object passed into `ProductVideoGenerator` and remove module-level globals.

**Magic numbers and implicit timing logic:**
- Issue: Hard-coded timing values (`total_seconds = 8`, `total_seconds += 7`, `time.sleep(10)`) are embedded in video generation logic.
- Files: `productvideo_generator.py`
- Impact: Assumes specific Veo behavior; makes changing durations brittle; harder to tune across models.
- Fix approach: Derive timing from config/env, and centralize timing constants in a single configuration section.

**Unused helper function:**
- Issue: `_extract_video_data` is not used anywhere.
- Files: `productvideo_generator.py`
- Impact: Dead code increases maintenance surface and confusion about intended video response handling.
- Fix approach: Remove unused function or integrate it into video extraction flow.

**Unpinned dependency versions:**
- Issue: `requirements.txt` lists packages without version pins.
- Files: `requirements.txt`
- Impact: Dependency updates can break API compatibility unexpectedly (e.g., `google-genai`, `pytrends`).
- Fix approach: Pin versions (or use constraints) and update CI to track compatible releases.

## Known Bugs

**Aspect ratio mismatch in Veo prompt:**
- Symptoms: The Veo prompt always says “Format 16:9”, while default aspect ratio config is `9:16`.
- Files: `productvideo_generator.py`
- Trigger: Default configuration (no `VIDEO_ASPECT_RATIO` env var) or any non-16:9 setting.
- Workaround: Align prompt string with actual `VIDEO_ASPECT_RATIO` or override env to `16:9`.

**Metadata may reference missing video file after failed generation:**
- Symptoms: `generate_video_with_veo()` catches exceptions and does not raise; main flow proceeds to metadata even when video generation failed, producing metadata with a path to a non-existent file.
- Files: `productvideo_generator.py`
- Trigger: Any Veo generation failure that is not `NOT_FOUND` (or fallback failure).
- Workaround: Add a success flag and skip metadata if video generation failed, or raise to stop the pipeline.

## Security Considerations

**Path traversal / unsafe filenames from user input:**
- Risk: `topic` is used to build filenames with only space replacement, allowing path separators or special characters to escape `VIDEO_OUTPUT_DIR`.
- Files: `productvideo_generator.py`
- Current mitigation: `replace(' ', '_')` only.
- Recommendations: Sanitize `topic` to a safe filename (strip path separators, normalize to alphanumerics) before writing files.

**Local `.env` presence (secrets in repo root):**
- Risk: `.env` file exists in repo root; accidental commits can leak secrets if not ignored or if hooks fail.
- Files: `.env` (present, contents not read)
- Current mitigation: `.gitignore` should exclude `.env` (verify policy).
- Recommendations: Ensure `.env` is ignored and add pre-commit checks if needed.

## Performance Bottlenecks

**Unbounded polling loop for video operations:**
- Problem: `_wait_for_operation` loops indefinitely with fixed 10s sleep and no timeout.
- Files: `productvideo_generator.py`
- Cause: No timeout or max retries for long-running or stuck operations.
- Improvement path: Add timeout, exponential backoff, and a clear failure path to prevent infinite waits.

**Repeated network calls to extend video length:**
- Problem: `_extend_video_if_needed` may call multiple Veo generations in a loop.
- Files: `productvideo_generator.py`
- Cause: Fixed step increments of 7 seconds without checking model limits or costs.
- Improvement path: Make extension optional, cap the number of extensions, and document cost implications.

## Fragile Areas

**GenAI response parsing assumes specific shapes:**
- Files: `productvideo_generator.py`
- Why fragile: Accesses `response.candidates[0].content.parts` and `response.text` without strong validation; any SDK response change can break parsing.
- Safe modification: Add schema checks before indexing; log response structure on unexpected shapes.
- Test coverage: No tests for malformed or partial SDK responses.

**JSON parsing from model output is brittle:**
- Files: `productvideo_generator.py`
- Why fragile: Simple string splitting on markdown fences and `json.loads` without validation; models may return extra text or invalid JSON.
- Safe modification: Use a stricter extraction approach or request a structured response format if supported.
- Test coverage: No tests that exercise malformed JSON or markdown responses.

## Scaling Limits

**Single-threaded, synchronous pipeline:**
- Current capacity: Processes one topic at a time, with blocking network calls.
- Files: `productvideo_generator.py`
- Limit: Scaling to multiple topics requires sequential runs; throughput is limited by external API latency.
- Scaling path: Add batch processing or async orchestration outside the core generator.

## Dependencies at Risk

**SDK behavior drift (google-genai, pytrends):**
- Risk: Upstream SDK changes can alter response formats or method names (`generate_content`, response fields).
- Impact: Breaks script generation or video generation flow without clear compile-time signals.
- Migration plan: Pin versions and add compatibility tests for response parsing.

## Missing Critical Features

**No explicit retry policy for transient API errors:**
- Problem: Only minimal fallback is implemented for Veo `NOT_FOUND`; other transient errors rely on single attempt.
- Blocks: Stable unattended runs in CI or scheduled jobs.

## Test Coverage Gaps

**Error-handling paths are untested:**
- What's not tested: Veo failures, timeout behaviors, fallback model selection, and metadata fallback after invalid JSON.
- Files: `productvideo_generator.py`, `tests/test_productvideo_generator.py`
- Risk: Failures may silently proceed and produce partial outputs without detection.
- Priority: High

**Filename sanitization is untested:**
- What's not tested: Topics with special characters or path separators.
- Files: `productvideo_generator.py`, `tests/test_productvideo_generator.py`
- Risk: Output files written outside `VIDEO_OUTPUT_DIR` or failing to write.
- Priority: Medium

---

*Concerns audit: 2026-02-24*
