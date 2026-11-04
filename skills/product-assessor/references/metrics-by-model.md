# Metrics and methods by business model

Pick the row(s) that match the classified business. A business may span two rows (e.g. a
hardware product with a SaaS subscription); union the "Use" columns and say so. "Skip"
metrics are ones that produce misleading precision for that model — do not report them
even if the user asks for "all the SaaS metrics" on a consultancy; explain why instead.

| Model | Use | Skip / adapt | Decisive questions |
|---|---|---|---|
| **SaaS / subscription** | MRR/ARR, gross margin, logo + revenue churn, NRR, CAC, CAC payback, LTV:CAC, ARPA, activation and expansion rates | Inventory, foot traffic, utilization | Who pays, who uses, who decides? Is churn a product or a segment problem? What is the price-metric (seat, usage, tier) and does it track value? |
| **Enterprise software** | ACV, sales cycle length, win rate, pipeline coverage, implementation cost per deal, gross margin after services, concentration (top-5 % of revenue) | Self-serve funnel metrics | Is the buyer the user? Procurement/compliance blockers? Who owns the integration cost? |
| **Marketplace / platform** | GMV, take rate, liquidity (fill rate, time-to-match), supply vs demand CAC, repeat rate both sides, contribution margin per transaction | MRR, seat counts | Which side is the constraint? Is there multi-homing? Where does disintermediation leak value? |
| **Ecommerce / DTC** | AOV, contribution margin after shipping + returns + payment, repeat purchase rate, blended and paid CAC, return rate, inventory turns | NRR, ACV | Is growth paid-dependent? What is contribution margin on a first order vs repeat? |
| **Physical products / hardware** | Unit gross margin (BOM + landed + warranty), inventory turns and cash cycle, channel margin stack, attach rate of any recurring layer, MOQ exposure | Churn (unless a service layer exists) | Who owns distribution? Working-capital need at 2× volume? Commoditization timeline? |
| **Retail / hospitality (physical locations)** | Sales per sq ft or per seat, gross margin by category, labor %, shrink, basket size, visit frequency, four-wall EBITDA, payback per location | CAC/LTV as primary, MRR | Is the economics of one location proven before the second? Lease and labor sensitivity? Local competitive density? |
| **Professional services / consulting** | Utilization, realized hourly or project rate, gross margin per engagement, pipeline, repeat/referral %, revenue per head, concentration | MRR (unless retainers), churn %, activation | Is this time-for-money or productized? Can delivery be de-skilled or templated? Would a product cannibalize or expand it? |
| **Internal business tool** | Hours saved × loaded cost, error/rework reduction, cycle time, adoption %, build + maintain cost vs buy price, opportunity cost of the team | Revenue metrics, CAC, market size | Would a bought tool do 80 % at 20 % of the cost? Who is on the hook when the builder leaves? |
| **AI product / AI-enabled** | All of the host model's metrics plus: inference cost per unit of value, gross margin at scale, eval-backed quality vs incumbents, data/feedback moat evidence, model-dependency risk | Treating "uses AI" as differentiation | Is the value the model or the workflow around it? What happens when the foundation model gets cheaper or better for free? |
| **Consumer app / freemium** | DAU/MAU, retention curves (D1/D7/D30), conversion to paid, ARPU, viral factor, paid CAC vs organic share | ACV, utilization | Is retention flattening above zero? Would users pay, or only advertisers? |

## Universal (every model)

- Gross and contribution margin, break-even, cash runway or cash conversion cycle.
- Customer concentration, pricing power evidence (price increases retained? discounting?).
- Build-vs-buy and capital allocation: what else could the same money and time do?
- Three scenarios (conservative / base / optimistic) with named assumptions.

## When the business is pre-revenue

Report no unit economics as fact. Use: problem evidence (who complains, how much do they
spend on workarounds), willingness-to-pay signals, competitor pricing as a ceiling,
cost-to-serve estimate. Everything downstream is `[hypothesis]`.
