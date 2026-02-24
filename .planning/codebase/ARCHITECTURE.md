# Architecture

**Analysis Date:** 2026-02-24

## Pattern Overview

**Overall:** Single-module, script-first pipeline with a single coordinating class in `productvideo_generator.py`.

**Key Characteristics:**
- Linear, step-based orchestration (trends → script → video → metadata) implemented in `productvideo_generator.py`.
- Side-effect driven workflow that writes files directly to disk in `productvideo_generator.py`.
- Configuration and client initialization centralized and lazily loaded in `productvideo_generator.py`.

## Layers

**Configuration & Environment:**
- Purpose: Validate and load env config, set global defaults, and initialize API client.
- Location: `productvideo_generator.py`
- Contains: `_check_env_file`, `_require_env`, `_optional_env`, `_optional_int_env`, `_initialize_config` in `productvideo_generator.py`.
- Depends on: OS environment variables and `.env` file path `productvideo_generator.py`.
- Used by: `ProductVideoGenerator` initialization and all pipeline steps in `productvideo_generator.py`.

**External Service Access:**
- Purpose: Access Google Trends and Gemini/Veo models.
- Location: `productvideo_generator.py`
- Contains: `TrendReq` usage in `ProductVideoGenerator.research_trends` and `genai.Client` usage in `ProductVideoGenerator.generate_sales_script`/`generate_video_with_veo` in `productvideo_generator.py`.
- Depends on: `pytrends` and `google-genai` configured in `requirements.txt`.
- Used by: Pipeline steps in `productvideo_generator.py`.

**Pipeline Orchestration:**
- Purpose: Coordinate the end-to-end workflow and hold per-run state.
- Location: `productvideo_generator.py`
- Contains: `ProductVideoGenerator` class and main `__name__ == "__main__"` runner in `productvideo_generator.py`.
- Depends on: Config layer and external service access in `productvideo_generator.py`.
- Used by: CLI execution via `run.sh` and direct `python productvideo_generator.py` runs.

**Persistence/Outputs:**
- Purpose: Write script, video, and metadata files.
- Location: `productvideo_generator.py`
- Contains: File writing in `generate_sales_script`, `_save_generated_video`, `generate_metadata` in `productvideo_generator.py`.
- Depends on: `VIDEO_OUTPUT_DIR` from environment in `productvideo_generator.py`.
- Used by: Pipeline steps in `productvideo_generator.py`.

## Data Flow

**Video Generation Pipeline:**

1. Read topic input (CLI or piped) in `productvideo_generator.py`.
2. Initialize config/client and validate environment in `productvideo_generator.py`.
3. Resolve topic via trends lookup in `ProductVideoGenerator.research_trends` in `productvideo_generator.py`.
4. Generate sales script with Gemini text model in `ProductVideoGenerator.generate_sales_script` in `productvideo_generator.py`.
5. Generate video with Veo and save MP4 in `ProductVideoGenerator.generate_video_with_veo` and `_save_generated_video` in `productvideo_generator.py`.
6. Generate metadata JSON in `ProductVideoGenerator.generate_metadata` in `productvideo_generator.py`.

**State Management:**
- Runtime state is stored on the `ProductVideoGenerator` instance (`topic`, `script_content`, `video_path`) in `productvideo_generator.py`.
- Global configuration values are stored as module-level globals in `productvideo_generator.py`.

## Key Abstractions

**ProductVideoGenerator:**
- Purpose: Orchestrate the full pipeline and hold per-run state.
- Examples: `ProductVideoGenerator` in `productvideo_generator.py`.
- Pattern: Single coordinator class with step methods and helper methods in `productvideo_generator.py`.

**Video Generation Helpers:**
- Purpose: Encapsulate Veo prompt/config building, polling, and saving.
- Examples: `_build_video_config`, `_build_veo_prompt`, `_run_video_generation`, `_extend_video_if_needed`, `_save_generated_video` in `productvideo_generator.py`.
- Pattern: Private helper methods called by `generate_video_with_veo` in `productvideo_generator.py`.

## Entry Points

**CLI Script Execution:**
- Location: `productvideo_generator.py`
- Triggers: `python productvideo_generator.py` or `run.sh`.
- Responsibilities: Initialize config, read topic input, run pipeline steps in order in `productvideo_generator.py`.

**Shell Wrapper:**
- Location: `run.sh`
- Triggers: `./run.sh` with optional topic argument.
- Responsibilities: Validate `.env`, ensure venv/deps, pipe topic into `productvideo_generator.py` in `run.sh`.

## Error Handling

**Strategy:** Guard configuration early and use best-effort fallbacks for external services, with runtime failures raised for critical steps in `productvideo_generator.py`.

**Patterns:**
- Configuration validation raises `RuntimeError` via `_raise_env_error` in `productvideo_generator.py`.
- External service failures log warnings and fall back (e.g., trends lookup) in `ProductVideoGenerator.research_trends` in `productvideo_generator.py`.
- Video generation errors attempt model fallback in `ProductVideoGenerator.generate_video_with_veo` in `productvideo_generator.py`.

## Cross-Cutting Concerns

**Logging:** Print-based user feedback using `print(...)` in `productvideo_generator.py`.
**Validation:** Environment validation in `_check_env_file` and `_require_env` in `productvideo_generator.py`.
**Authentication:** API key loaded from environment in `_initialize_config` in `productvideo_generator.py`.

---

*Architecture analysis: 2026-02-24*
