# Project-local history: `.product-assessor/`

Lives at the project root. Project-local only: never copy its content to another project,
to the assistant's global memory, or anywhere shared. Recommend the user add it to
`.gitignore` if the repo is shared beyond the business owners; do not edit `.gitignore`
yourself.

## Layout

```
.product-assessor/
  profile.md            # business classification + stable facts; update, don't append
  decisions.md          # one row per recommendation the user accepted/rejected/deferred
  research/<topic>.md   # dated external research, one topic per file
  assessments/
    YYYY-MM-DD[-slug].md  # the delivered report, verbatim, with predictions marked
```

### profile.md
Industry, model, acquisition model, cost structure, stage, segments, named competitors,
pricing as of a date, key assumptions. Each line dated or sourced. When a fact changes,
replace it and note the old value with its date.

### decisions.md

| Date | Recommendation (ref assessment) | Decision: accepted / rejected / deferred | Reason given | Predicted outcome + metric | Check by | Actual outcome |

Fill "Actual outcome" when data appears; this is how recommendation performance is judged.
An unfilled "Check by" that has passed is itself a finding — raise it at the next run.

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

## When to write

Only when the user asks to track decisions, asks to reassess, or the project is clearly
going to be assessed again. A one-off quick verdict writes nothing.
