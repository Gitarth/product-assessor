# product-assessor

An agent skill (Claude Code, Codex, OpenCode, Zed) that acts as an independent, skeptical commercial advisor. It assesses a
product or business for **realistically achievable market capture** and **risk-adjusted
long-term profitability**, across any industry, business model or stack.

It is built to challenge you, not agree with you: it names weak differentiation, unrealistic
market assumptions, poor pricing, features nobody needs, and technical decisions with no
commercial justification. Every major claim is tagged `[verified]`, `[evidence-backed]`,
`[hypothesis]` or `[unknown]`.

**Advisor only.** It never edits code, files issues, or changes pricing or infrastructure.
The only thing it writes is its own project-local history under `.product-assessor/`.

## Install

Works in Claude Code, Codex, OpenCode and Zed. One skill folder, the
[Agent Skills](https://agentskills.io) format.

**Claude Code** (plugin, one step on 2.1.275 or later):

```
/plugin install product-assessor --marketplace Gitarth/product-assessor
```

**Codex, Zed, OpenCode** (all three read `~/.agents/skills/`):

```
git clone https://github.com/Gitarth/product-assessor
cp -r product-assessor/.agents/skills/product-assessor ~/.agents/skills/
```

OpenCode also reads `~/.config/opencode/skills/` and `~/.claude/skills/`; any of the three
works. Codex and Zed pick new skills up automatically (restart if not).

**Any agent, via the skills CLI:**

```
npx skills add Gitarth/product-assessor
```

**Per project:** clone or copy into `<repo>/.agents/skills/product-assessor/` (Codex, Zed,
OpenCode) or `<repo>/.claude/skills/product-assessor/` (Claude Code, OpenCode). This repo
itself carries the skill at `.agents/skills/`, so opening it in Codex, Zed or OpenCode loads it.

## Use

Say any of:

- "Assess this product commercially."
- "Find opportunities to maximize market share."
- "Evaluate our pricing and profitability."
- "Identify weaknesses in our competitive positioning."
- "Assess this codebase from a commercial perspective."
- "Find the highest-value product improvements."
- "Reassess previous strategic recommendations."

Default depth is **quick**: an executive verdict, a ranked table of 3–7 opportunities, and
the open questions that could change the verdict. Ask for a **full** assessment to get all
nine report sections (market, competition, financials, product and technical, strategic
direction, validation plan).

## How it works

1. **Classify** the business: industry, model, acquisition channel, cost structure, stage,
   competitive setting. Inferred items are marked as such.
2. **Inventory evidence, cheapest first**: existing docs, then targeted code search, then
   web. Reuses any code map that already exists; never scans a whole repository.
3. **Pick metrics for this business model** from
   [`metrics-by-model.md`](.agents/skills/product-assessor/references/metrics-by-model.md).
   A consultancy does not get MRR and churn; a retailer does not get CAC/LTV as a headline.
4. **Research gaps** within a budget (default 8 web lookups, each dated and cited), under
   the evidence rules in [`research.md`](.agents/skills/product-assessor/references/research.md).
5. **Analyze and rank**: upside × probability, minus downside, weighted by reversibility.
6. **Report**, verdict first, per [`report.md`](.agents/skills/product-assessor/references/report.md).
7. **Lint and record.** The report must pass `scripts/assess.py lint` before it is shown.
   Its predictions are filed in `.product-assessor/ledger.jsonl` and scored on later runs
   ([`history.md`](.agents/skills/product-assessor/references/history.md)).

## Project-local history

When tracking is wanted, the skill keeps `profile.md`, `decisions.md`, dated research and
past assessments in `.product-assessor/` at the project root. It never shares one project's
intelligence with another or with global memory, and never stores credentials or
unnecessary customer data. Add `.product-assessor/` to your `.gitignore` if the repo is
shared beyond the business owners.

## Example (synthetic, quick depth)

This is the shape the lint enforces; it passes `scripts/assess.py lint`.

````markdown
<!-- product-assessor v0.3.0 depth=quick date=2026-11-05 searches=3/8 -->
## 1. Executive verdict
Viable. Confidence: medium. Incumbents bill $89/mo per lane [verified] (pricing page, 2026-11-04);
a flat per-store price undercuts by ~40% while holding margin [hypothesis: infra cost per store unknown].
Biggest weakness: one tenant, no paying customers outside the founder [verified] (`README.md`).
Key risk: card payments not live; no card tender means not sellable to retail [verified] (`apps/api/src/payments/`).
What would change this: evidence that target stores weigh price above switching cost.

## 6. Prioritized opportunities
| # | Opportunity | Impact | Capture | Cost | Time to value | Conf | Why |
|---|---|---|---|---|---|---|---|
| 1 | Ship card payments before any sales | high | gating | med | 6wk | high | nothing sells without it |
| 2 | Flat per-store pricing vs per-lane | med | high | low | 2wk | med | exploitable incumbent weakness |
| 3 | Drop restaurant placeholder scope | margin | none | neg | now | high | zero demand evidence |

```json ledger
[{"id":"2026-11-05-1","recommendation":"Ship card payments","metric":"paying stores","threshold":1,"direction":">=","probability":0.8,"check_by":"2027-02-01"},
 {"id":"2026-11-05-2","recommendation":"Flat per-store pricing","metric":"trial-to-paid %","threshold":20,"direction":">=","probability":0.6,"check_by":"2027-01-15"},
 {"id":"2026-11-05-3","recommendation":"Drop restaurant scope","metric":"restaurant requests from paying stores","threshold":0,"direction":"==","probability":0.8,"check_by":"2027-05-01"}]
```

## 9. Open questions
Infra cost per tenant at 10 stores? Resolves the pricing floor.
Why did the last three prospects not switch? Resolves the switching-cost hypothesis.
````

## The feedback loop

Every recommendation is a forecast: a metric, a threshold, a probability and a date. The
skill is scored on them, deterministically, by `scripts/assess.py` (python3, stdlib only,
writes only under `.product-assessor/`):

```
python3 scripts/assess.py lint  <report.md>                      # before a report is shown; exit 1 blocks it
python3 scripts/assess.py ledger ingest  <report.md>             # file the predictions
python3 scripts/assess.py ledger decide  <id> accepted|rejected|deferred "<reason>"
python3 scripts/assess.py ledger resolve <id> hit|miss "<what actually happened>"
python3 scripts/assess.py ledger report                          # overdue, hit rate, Brier, ADVICE lines
```

On the next run the skill reads `ledger report` first. Overdue predictions are surfaced
before new advice. If a confidence bucket is over-claiming by more than 15 points over at
least three resolved predictions, the report emits an `ADVICE:` line that tells the skill to
downgrade its confidence language for this project. That is the only mechanism that changes
its behaviour: no model self-grading, no telemetry.

To help improve the skill for everyone, open a
[calibration report](.github/ISSUE_TEMPLATE/calibration-report.md) with the output of
`ledger report --share`. It contains aggregates and the skill version only.

## Layout

```
.agents/skills/product-assessor/   (the skill; Codex, Zed and OpenCode read this path directly)
  SKILL.md                         workflow, scope rule, depth, guardrails
  agents/openai.yaml               Codex / ChatGPT display metadata (optional)
  scripts/assess.py                report lint + calibration ledger (python3, stdlib)
  references/metrics-by-model.md   which metrics apply to which business model, and which to skip
  references/report.md             report sections, ranking formula
  references/research.md           evidence tiers, source rules, research budget
  references/history.md            .product-assessor/ layout and revalidation rules
.claude-plugin/                    Claude Code plugin + marketplace manifests (point at .agents/skills/)
```

## License

MIT
