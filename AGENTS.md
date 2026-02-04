# AGENT Guide for GitHub Copilot & AI Assistants

This repository uses GitHub Copilot (and similar agents) to automate video generation. Follow these guardrails and improve them over time.

## Mission

- Keep the pipeline working end-to-end: trend lookup → sales script → Veo video generation → metadata.
- Stay safe: do not leak secrets from .env; avoid destructive git commands.
- Focus: Product review / Sales style videos (not podcasts).

## Operating Rules

- **Default language:** German for user-visible text (scripts, titles, descriptions).
- **Environment:** Rely on \`.env\` variables; never hardcode API keys.
- **Trend region focus:** DACH (DE, AT, CH).
- **Video Logic:** Do NOT attempt to use ffmpeg or external TTS. The pipeline relies entirely on the Veo 3.1 API for audio/video/music generation.

## Script Generation Guidelines

- **Style:** Sales/Conversion focused (Hook, Problem, Solution, Benefits, CTA).
- **Formatting:** Spoken text mainly, but allow visual cues in brackets \`()\` to guide the Veo model prompt (e.g., "(Close up of product)").

## Editing Guidelines

- Prefer minimal diffs; use \`apply_patch\` for single-file edits.
- Keep output paths stable under \`VIDEO_OUTPUT_DIR\`.
- Log non-fatal errors instead of aborting the whole run when possible (e.g., trend lookup failure).

## Quality Checks

- Run \`./run.sh "topic"\` for an end-to-end test.
- Verify that the script contains a clear CTA.
- Ensure the Veo model name in \`productvideo_generator.py\` matches the current API availability.
