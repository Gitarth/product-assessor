---
name: Calibration report
about: Share how well the skill's predictions held up on your project (aggregates only)
title: "calibration: v<version>, <business model>"
labels: calibration
---

Paste the output of `python3 scripts/assess.py ledger report --share`. It contains only
counts, hit rates, Brier scores and the skill version — no recommendation text, no business
facts. Do not add any.

```
<paste here>
```

Business model (one of the rows in metrics-by-model.md):

What the skill got most wrong, in one sentence, without naming your product or market:
