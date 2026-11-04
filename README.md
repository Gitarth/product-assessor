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
7. **Record** to `.product-assessor/` when the project will be assessed again, so later
   runs compare predictions with outcomes
   ([`history.md`](.agents/skills/product-assessor/references/history.md)).

## Project-local history

When tracking is wanted, the skill keeps `profile.md`, `decisions.md`, dated research and
past assessments in `.product-assessor/` at the project root. It never shares one project's
intelligence with another or with global memory, and never stores credentials or
unnecessary customer data. Add `.product-assessor/` to your `.gitignore` if the repo is
shared beyond the business owners.

## Example (synthetic, quick depth)

```
VERDICT: viable. Confidence: medium.
Biggest opportunity: incumbents bill $X/mo/lane [verified, pricing page 2026-11-04]; a flat
per-store price undercuts by ~40% while holding margin [hypothesis: infra cost/store unknown].
Biggest weakness: one tenant, zero paying customers outside the founder [verified].
Key risk: card payments not live; no card tender = not sellable to retail [verified].
What would change this: evidence that target stores weigh price above switching cost.

# | Opportunity                         | Impact | Capture | Cost | TTV | Conf | Why
1 | Ship card payments before any sales | high   | gating  | med  | 6wk | high | nothing sells without it
2 | Flat per-store pricing vs per-lane  | med    | high    | low  | 2wk | med  | exploitable incumbent weakness
3 | Drop restaurant placeholder scope   | margin | none    | neg  | now | high | zero demand evidence

Open: (1) infra cost per tenant at 10 stores? (2) why did the last 3 prospects not switch?
```

## Layout

```
.agents/skills/product-assessor/   (the skill; Codex, Zed and OpenCode read this path directly)
  SKILL.md                         workflow, scope rule, depth, guardrails
  agents/openai.yaml               Codex / ChatGPT display metadata (optional)
  references/metrics-by-model.md   which metrics apply to which business model, and which to skip
  references/report.md             report sections, ranking formula
  references/research.md           evidence tiers, source rules, research budget
  references/history.md            .product-assessor/ layout and revalidation rules
.claude-plugin/                    Claude Code plugin + marketplace manifests (point at .agents/skills/)
```

## License

MIT
