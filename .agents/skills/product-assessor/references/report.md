# Report format

Verdict first, always. **Quick** depth = sections 1, 6, 9 only. **Full** = all nine.
Length follows the evidence: three findings do not need nine pages. Tag every major claim
`[verified]` `[evidence-backed]` `[hypothesis]` `[unknown]` (tiers in research.md).

`scripts/assess.py lint` enforces the shape below. What it checks:

- First line is the stamp `<!-- product-assessor vX.Y.Z depth=quick|full date=YYYY-MM-DD searches=N/M -->`
  (version from SKILL.md; N searches used of M budget; over budget needs a "budget raised" line).
- Section headings are exactly `## 1.` … `## 9.`; quick has only 1, 6, 9; `## 1.` comes first.
- Any line with a figure ($, %, ×, thousands) carries a tag. Table rows are exempt.
- `[evidence-backed]` paragraphs contain a date or URL; `[verified]` paragraphs a date, URL or `file path`.
- Section 1 has a "what would change this verdict" line; full depth has a non-empty **Stop** list.
- Section 6 table has columns Opportunity, Impact, Capture, Cost, Time to value, Conf, Why; 3–7 rows.
- A ```` ```json ledger ```` block (end of section 6) lists one prediction per opportunity:
  `{"id","recommendation","metric","threshold","direction","probability","check_by"}`,
  probability in (0,1), check_by after today. `id` = `YYYY-MM-DD-n`. Probability is your
  honest chance the metric clears the threshold by check_by; it is what Brier scores you on.

## 1. Executive verdict
- Commercial attractiveness (one line, with a plain grade: strong / viable / marginal / weak).
- Biggest opportunity. Biggest weakness. Most important strategic risk.
- Recommended direction (one sentence).
- Confidence: high / medium / low, and **what would change this verdict** (the one or two
  facts that, if different, flip the recommendation).

## 2. Business and market overview
Industry, model, maturity, segments, market opportunity (TAM/SAM/SOM only with sources;
otherwise a bounded estimate labeled hypothesis). Say whether the current target segment is
the best one or just the first one.

## 3. Competitive position
Direct and indirect competitors with pricing and positioning (dated). Where they are
genuinely better. Their weaknesses and which are exploitable. Temporary vs durable
advantages of the subject. Switching costs and network effects, if real.

## 4. Financial analysis
Only the metrics selected from metrics-by-model.md. Revenue opportunities, pricing (model,
metric, level, sensitivity), cost structure and cost-to-serve, unit economics, break-even,
three scenarios with assumptions in a table. Actuals vs projections kept separate.

## 5. Product and technical assessment
Product strengths and weaknesses against the segment's actual needs. Features to build,
improve, remove or deprioritize, each with its commercial reason. Technical and operational
findings only where they have a commercial consequence: infra cost, reliability, velocity,
compliance exposure, scalability, build-vs-buy. Name the file or component when code was
inspected.

## 6. Prioritized opportunities
Three to seven, ranked. One row each:

| # | Opportunity | Revenue / profit impact | Market capture | Cost | Time to value | Confidence | Why it ranks here |

Risk-adjust: expected upside × probability, minus downside exposure, weighted by
reversibility. An irreversible bet with medium confidence ranks below a reversible one with
the same upside.

## 7. Recommended strategic direction
Start / Stop / Continue / Change / Validate — one to three bullets each. "Stop" must have
content; an assessment that stops nothing has not challenged anything.

## 8. Validation plan
For each top opportunity or risky assumption: the experiment, the metric, the threshold
that counts as success, the threshold that kills the idea, and the time box.

## 9. Open questions
Only questions whose answer would materially change the recommendation. For each: why it
matters and how the user could answer it.
