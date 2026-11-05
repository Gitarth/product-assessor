# Changelog

## 0.3.0 — 2026-11-05
- `scripts/assess.py`: deterministic report lint (stamp, sections, tagged figures, dated
  evidence, opportunity table, prediction block) and a calibration ledger (ingest, decide,
  resolve, report with Brier score and per-bucket ADVICE lines, `--share` aggregates).
- Reports carry a version stamp and a `json ledger` block of falsifiable predictions.
- `decisions.md` replaced by `ledger.jsonl`.
- Calibration-report issue template for voluntary aggregate feedback.

## 0.2.0 — 2026-11-04
- Agent Skills layout at `.agents/skills/`; works in Claude Code, Codex, OpenCode, Zed.
- `agents/openai.yaml` display metadata; spec frontmatter (`license`, `metadata`).

## 0.1.0 — 2026-11-04
- Initial skill: SKILL.md + metrics-by-model, report, research, history references.
