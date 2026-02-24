# External Integrations

**Analysis Date:** 2026-02-24

## APIs & External Services

**AI Generation:**
- Google GenAI (Gemini text + Veo video) - script and video generation in `productvideo_generator.py`
  - SDK/Client: `google-genai` (`genai.Client`) in `productvideo_generator.py`
  - Auth: `GEMINI_API_KEY` from `.env`/env in `productvideo_generator.py`

**Trends/Discovery:**
- Google Trends - topic discovery in `productvideo_generator.py`
  - SDK/Client: `pytrends` (`TrendReq`) in `productvideo_generator.py`
  - Auth: None (public trends; no env var required)

## Data Storage

**Databases:**
- Not detected

**File Storage:**
- Local filesystem only
  - Output directory: `VIDEO_OUTPUT_DIR` env var used in `productvideo_generator.py`
  - Output files: `*_script.txt`, `*.mp4`, `*_meta.json` written in `productvideo_generator.py`

**Caching:**
- None

## Authentication & Identity

**Auth Provider:**
- Google GenAI API Key
  - Implementation: API key passed to `genai.Client` in `productvideo_generator.py`

## Monitoring & Observability

**Error Tracking:**
- None

**Logs:**
- Console output via `print` statements in `productvideo_generator.py`

## CI/CD & Deployment

**Hosting:**
- Not applicable (local execution)

**CI Pipeline:**
- GitHub Actions workflow in `.github/workflows/ci.yml`

## Environment Configuration

**Required env vars:**
- `GEMINI_API_KEY`, `CHANNEL_NAME`, `CHANNEL_DESCRIPTION`, `VIDEO_OUTPUT_DIR` (enforced in `productvideo_generator.py` and documented in `CONTRIBUTING.md`)

**Secrets location:**
- `.env` file at repo root (exists; contents not read) with template in `.env.example`

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

---

*Integration audit: 2026-02-24*
