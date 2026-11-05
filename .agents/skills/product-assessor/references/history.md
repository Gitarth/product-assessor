# Project-local history: `.product-assessor/`

Lives at the project root. Project-local only: never copy its content to another project,
to the assistant's global memory, or anywhere shared. Recommend the user add it to
`.gitignore` if the repo is shared beyond the business owners; do not edit `.gitignore`
yourself.

## Layout

```
.product-assessor/
  profile.md            # business classification + stable facts; update, don't append
  ledger.jsonl          # append-only: predictions (from ingest), resolutions, decisions
  research/<topic>.md   # dated external research, one topic per file
  assessments/
    YYYY-MM-DD[-slug].md  # the delivered report, verbatim, with predictions marked
```

### profile.md
Industry, model, acquisition model, cost structure, stage, segments, named competitors,
pricing as of a date, key assumptions. Each line dated or sourced. When a fact changes,
replace it and note the old value with its date.

### ledger.jsonl (managed by `scripts/assess.py`, never hand-edited)

- `ledger ingest <report>` appends each prediction from the report's ledger block
  (idempotent by id; stamps date and skill version).
- `ledger decide <id> accepted|rejected|deferred "<reason>"` records the user's decision.
- `ledger resolve <id> hit|miss "<actual>"` records the outcome. Hit/miss is the user's call;
  `actual` is free text.
- `ledger report` prints: overdue predictions (check_by passed, unresolved), hit rate and
  Brier score, calibration per confidence bucket (high ≥0.75, medium ≥0.5, low), decision
  counts with rejection reasons, results by skill version. Buckets under 3 resolved
  predictions print "insufficient data" and issue no advice.
- `ledger report --share` prints aggregates only, with no recommendation text or reasons.
  That is the only output that may leave the project (see the repo's calibration-report issue
  template).

### Unresolved risks
Keep in `profile.md` under a `## Open risks` heading with the date raised; remove when
resolved and note how.

## Revalidation rule

History is a record, not truth. On each run: pricing and competitor facts older than
~90 days, and market-structure facts older than ~12 months, are `[hypothesis]` until
rechecked. Past assumptions are re-tested against actuals before being reused.

## Never store

Credentials, API keys, tokens, customer PII beyond what an analysis needs (aggregate,
don't list), payment data, employee compensation details, or anything the user marks
confidential beyond the assessment.

## What is always written

The assessment file (`assessments/`) and `ledger.jsonl` are written on every run, because
the lint needs a file and the loop needs the predictions. `profile.md` and `research/` are
written when the project will be assessed again or the user asks to track it.
