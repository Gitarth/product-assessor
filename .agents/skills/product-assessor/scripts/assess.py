#!/usr/bin/env python3
"""Deterministic checks for product-assessor. Stdlib only. Writes only under .product-assessor/.

  assess.py lint <report.md>                     structural + evidence lint, exit 1 on failure
  assess.py ledger ingest <report.md>            append the report's ```json ledger block to ledger.jsonl
  assess.py ledger resolve <id> hit|miss "<actual>"
  assess.py ledger report [--share]              overdue, hit rate, Brier by confidence, ADVICE lines
  assess.py selftest
"""
import json, re, sys, os, datetime as dt, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = re.compile(r"\[(verified|evidence-backed|hypothesis|unknown)(:[^\]]*)?\]")
FIGURE = re.compile(r"\$\s?\d|\d\s?%|\b\d+(\.\d+)?x\b|\b\d{1,3}(,\d{3})+\b")
DATE = re.compile(r"\b20\d\d-\d\d-\d\d\b")
URL = re.compile(r"https?://\S+")
PATH = re.compile(r"`[^`\s]+\.[a-z]{1,5}`")
STAMP = re.compile(r"<!--\s*product-assessor v(\S+) depth=(quick|full) date=(\d{4}-\d\d-\d\d) searches=(\d+)/(\d+)\s*-->")
LEDGER_FIELDS = ("id", "recommendation", "metric", "threshold", "direction", "probability", "check_by")
MIN_N = 3


def skill_version():
    try:
        s = open(os.path.join(HERE, "..", "SKILL.md")).read()
        return re.search(r'^\s*version:\s*"?([^"\n]+)"?', s, re.M).group(1)
    except Exception:
        return "unknown"


def ledger_path(root="."):
    return os.path.join(root, ".product-assessor", "ledger.jsonl")


# ---------------- lint ----------------
def split(text):
    """Yield (lineno, line, in_fence, in_comment)."""
    fence = comment = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            fence = not fence
            yield i, line, True, comment
            continue
        if "<!--" in line:
            comment = True
        yield i, line, fence, comment
        if "-->" in line:
            comment = False


def paragraphs(text):
    buf, start = [], 1
    for i, line, fence, comment in split(text):
        if fence or comment:
            continue
        if line.strip():
            if not buf:
                start = i
            buf.append(line)
        elif buf:
            yield start, "\n".join(buf)
            buf = []
    if buf:
        yield start, "\n".join(buf)


def ledger_block(text):
    m = re.search(r"```json ledger\n(.*?)\n```", text, re.S)
    if not m:
        return None, "no ```json ledger block"
    try:
        rows = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        return None, f"ledger block is not valid JSON: {e}"
    if not isinstance(rows, list):
        return None, "ledger block must be a JSON list"
    return rows, None


def lint(text, today=None):
    today = today or dt.date.today()
    fails = []
    m = STAMP.search(text)
    if not m:
        fails.append("1: missing header stamp <!-- product-assessor vX depth=quick|full date=YYYY-MM-DD searches=N/M -->")
        depth = "quick"
    else:
        depth = m.group(2)
        used, cap = int(m.group(4)), int(m.group(5))
        if used > cap and "budget raised" not in text.lower():
            fails.append(f"{text[:m.start()].count(chr(10))+1}: searches {used}/{cap} over budget with no 'budget raised' line")

    heads = [(i, int(h)) for i, l, f, c in split(text) if not f and not c
             for h in re.findall(r"^##\s+(\d)\.", l)]
    nums = [n for _, n in heads]
    want = {1, 6, 9} if depth == "quick" else set(range(1, 10))
    for n in sorted(want - set(nums)):
        fails.append(f"-: missing section ## {n}.")
    if nums and nums[0] != 1:
        fails.append(f"{heads[0][0]}: verdict (## 1.) must come first")
    if depth == "quick" and set(nums) - {1, 6, 9}:
        fails.append("-: quick depth must contain only sections 1, 6, 9")
    if not re.search(r"what would change", text, re.I):
        fails.append("-: executive verdict lacks a 'what would change this verdict' line")

    for i, line, fence, comment in split(text):
        if fence or comment or line.lstrip().startswith("|"):
            continue
        if FIGURE.search(line) and not TAG.search(line):
            fails.append(f"{i}: figure without evidence tag: {line.strip()[:70]}")

    for start, para in paragraphs(text):
        tags = {t[0] for t in TAG.findall(para)}
        if "evidence-backed" in tags and not (DATE.search(para) or URL.search(para)):
            fails.append(f"{start}: [evidence-backed] claim has no date or URL in its paragraph")
        if "verified" in tags and not (DATE.search(para) or URL.search(para) or PATH.search(para)):
            fails.append(f"{start}: [verified] claim has no date, URL or `file path` in its paragraph")

    # opportunity table under ## 6.
    sec6 = re.search(r"^##\s+6\..*?(?=^##\s+\d\.|\Z)", text, re.M | re.S)
    if sec6:
        rows = [l for l in sec6.group(0).splitlines() if l.lstrip().startswith("|")]
        header = rows[0].lower() if rows else ""
        for col in ("opportunity", "impact", "capture", "cost", "time", "conf", "why"):
            if col not in header:
                fails.append(f"-: opportunity table header lacks '{col}' column")
        body = [r for r in rows[2:] if r.strip("| -")]
        if not 3 <= len(body) <= 7:
            fails.append(f"-: opportunity table has {len(body)} rows, need 3–7")

    if depth == "full":
        stop = re.search(r"\*\*Stop\*\*[^\n]*\n((?:\s*[-*] .+\n?)+)", text)
        if not stop:
            fails.append("-: full depth needs a non-empty Stop list in ## 7.")

    rows, err = ledger_block(text)
    if err:
        fails.append(f"-: {err}")
    else:
        if not rows:
            fails.append("-: ledger block is empty; every recommendation needs a prediction")
        for r in rows:
            missing = [f for f in LEDGER_FIELDS if f not in r]
            if missing:
                fails.append(f"-: ledger {r.get('id','?')} missing {missing}")
                continue
            if not (0 < float(r["probability"]) < 1):
                fails.append(f"-: ledger {r['id']} probability must be in (0,1)")
            try:
                if dt.date.fromisoformat(r["check_by"]) <= today:
                    fails.append(f"-: ledger {r['id']} check_by must be after today")
            except ValueError:
                fails.append(f"-: ledger {r['id']} check_by not YYYY-MM-DD")
    return fails


# ---------------- ledger ----------------
def read_ledger(path):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path) if l.strip()]


def append(path, row):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")


def ingest(text, path, today=None):
    rows, err = ledger_block(text)
    if err:
        sys.exit(f"ingest: {err}")
    m = STAMP.search(text)
    stamp_date = m.group(3) if m else str(today or dt.date.today())
    version = m.group(1) if m else skill_version()
    seen = {r["id"] for r in read_ledger(path) if r.get("kind") == "prediction"}
    n = 0
    for r in rows:
        if r["id"] in seen:
            continue
        r = dict(r, kind="prediction", date=stamp_date, skill_version=version, decision="pending")
        append(path, r)
        n += 1
    print(f"ingested {n} prediction(s) → {path}")


def resolve(path, pid, outcome, actual, today=None):
    if outcome not in ("hit", "miss"):
        sys.exit("resolve: outcome must be hit or miss")
    if pid not in {r["id"] for r in read_ledger(path) if r.get("kind") == "prediction"}:
        sys.exit(f"resolve: unknown id {pid}")
    append(path, {"kind": "resolution", "id": pid, "outcome": outcome, "actual": actual,
                  "resolved_on": str(today or dt.date.today())})
    print(f"resolved {pid} as {outcome}")


def decide(path, pid, decision, reason):
    if decision not in ("accepted", "rejected", "deferred"):
        sys.exit("decide: decision must be accepted|rejected|deferred")
    append(path, {"kind": "decision", "id": pid, "decision": decision, "reason": reason,
                  "date": str(dt.date.today())})
    print(f"{pid}: {decision}")


def bucket(p):
    return "high" if p >= 0.75 else "medium" if p >= 0.5 else "low"


def report(path, share=False, today=None):
    today = today or dt.date.today()
    rows = read_ledger(path)
    preds = {r["id"]: r for r in rows if r.get("kind") == "prediction"}
    res = {r["id"]: r for r in rows if r.get("kind") == "resolution"}
    decs = {r["id"]: r for r in rows if r.get("kind") == "decision"}
    out = [f"product-assessor calibration (skill v{skill_version()}, {today})",
           f"predictions: {len(preds)}  resolved: {len(res)}"]

    overdue = [p for i, p in preds.items() if i not in res and dt.date.fromisoformat(p["check_by"]) < today]
    if overdue:
        out.append(f"OVERDUE ({len(overdue)}): resolve these first")
        if not share:
            for p in overdue:
                out.append(f"  {p['id']}  due {p['check_by']}  {p['metric']} {p['direction']} {p['threshold']}  — {p['recommendation'][:60]}")

    scored = [(float(preds[i]["probability"]), res[i]["outcome"] == "hit") for i in res if i in preds]
    if scored:
        hits = sum(h for _, h in scored)
        brier = sum((p - h) ** 2 for p, h in scored) / len(scored)
        out.append(f"hit rate: {hits}/{len(scored)} ({100*hits//len(scored)}%)  Brier: {brier:.3f} (0 best, 0.25 = coin flip)")
        by = {}
        for p, h in scored:
            by.setdefault(bucket(p), []).append((p, h))
        for b in ("high", "medium", "low"):
            if b not in by:
                continue
            xs = by[b]
            rate = sum(h for _, h in xs) / len(xs)
            mean_p = sum(p for p, _ in xs) / len(xs)
            line = f"  {b:6} n={len(xs)} stated {mean_p:.2f} actual {rate:.2f}"
            if len(xs) < MIN_N:
                line += "  (insufficient data)"
            elif mean_p - rate > 0.15:
                line += f"\nADVICE: '{b}' confidence predictions hit {rate:.0%} vs {mean_p:.0%} stated. Downgrade {b}-confidence language in this project until calibration recovers."
            elif rate - mean_p > 0.15:
                line += f"\nADVICE: '{b}' predictions under-claim ({rate:.0%} hit vs {mean_p:.0%} stated). Confidence may be raised one step."
            out.append(line)
    else:
        out.append("no resolved predictions yet")

    if decs:
        counts = {}
        for d in decs.values():
            counts[d["decision"]] = counts.get(d["decision"], 0) + 1
        out.append("decisions: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
        rej = [d for d in decs.values() if d["decision"] == "rejected"]
        if len(decs) >= MIN_N and len(rej) / len(decs) > 0.5:
            out.append("ADVICE: more than half of recommendations rejected. Re-read rejection reasons before classifying; the model of this business is probably wrong.")
        if rej and not share:
            out.append("rejection reasons:")
            out += [f"  {d['id']}: {d['reason']}" for d in rej]

    vers = {}
    for i, r in res.items():
        if i in preds:
            vers.setdefault(preds[i].get("skill_version", "?"), []).append(r["outcome"] == "hit")
    if len(vers) > 1:
        out.append("by skill version: " + ", ".join(f"v{v} {sum(x)}/{len(x)}" for v, x in sorted(vers.items())))
    return "\n".join(out)


# ---------------- selftest ----------------
EXAMPLE = """<!-- product-assessor v0.3.0 depth=quick date=2026-11-05 searches=3/8 -->
## 1. Executive verdict
Viable. Confidence: medium. Incumbents bill $89/mo per lane [verified] (pricing page, 2026-11-04).
Biggest weakness: one tenant [verified] (`README.md`). What would change this: evidence stores weigh price over switching cost.

## 6. Prioritized opportunities
| # | Opportunity | Impact | Capture | Cost | Time to value | Conf | Why |
|---|---|---|---|---|---|---|---|
| 1 | Ship card payments | high | gating | med | 6wk | high | nothing sells without it |
| 2 | Flat per-store pricing | med | high | low | 2wk | med | incumbent weakness |
| 3 | Drop restaurant scope | margin | none | neg | now | high | zero demand evidence |

```json ledger
[{"id":"2026-11-05-1","recommendation":"Ship card payments","metric":"paying stores","threshold":1,"direction":">=","probability":0.8,"check_by":"2027-02-01"},
 {"id":"2026-11-05-2","recommendation":"Flat per-store pricing","metric":"trial-to-paid %","threshold":20,"direction":">=","probability":0.6,"check_by":"2027-01-15"},
 {"id":"2026-11-05-3","recommendation":"Drop restaurant scope","metric":"restaurant feature requests","threshold":0,"direction":"==","probability":0.8,"check_by":"2027-02-15"}]
```

## 9. Open questions
Infra cost per tenant at 10 stores?
"""


def selftest():
    today = dt.date(2026, 11, 5)
    assert lint(EXAMPLE, today) == [], lint(EXAMPLE, today)
    bad = EXAMPLE.replace("## 9.", "Margin up 30% after repricing.\n\n## 9.")
    f = lint(bad, today)
    assert any("figure without evidence tag" in x for x in f), f
    f = lint(EXAMPLE.replace("## 9.", "Churn is low [verified].\n\n## 9."), today)
    assert any("no date, URL or" in x for x in f), f
    with tempfile.TemporaryDirectory() as d:
        p = ledger_path(d)
        ingest(EXAMPLE, p, today)
        ingest(EXAMPLE, p, today)  # idempotent
        assert len(read_ledger(p)) == 3
        resolve(p, "2026-11-05-1", "hit", "2 stores paying", today)
        resolve(p, "2026-11-05-2", "miss", "11% trial-to-paid", today)
        decide(p, "2026-11-05-3", "rejected", "owner wants restaurant for a prospect")
        r = report(p, today=dt.date(2027, 3, 1))
        assert "hit rate: 1/2 (50%)  Brier: 0.200" in r, r      # (0.8-1)^2=0.04, (0.6-0)^2=0.36, mean 0.20
        assert "OVERDUE (1)" in r and "2026-11-05-3  due 2027-02-15" in r, r
        assert "(insufficient data)" in r
        s = report(p, share=True, today=dt.date(2027, 3, 1))
        assert "Ship card payments" not in s and "owner wants" not in s, s
    print("selftest ok")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        sys.exit(__doc__)
    cmd = argv[0]
    if cmd == "selftest":
        return selftest()
    if cmd == "lint":
        fails = lint(open(argv[1]).read())
        print("\n".join(fails) if fails else "lint ok")
        sys.exit(1 if fails else 0)
    if cmd == "ledger":
        sub, args = argv[1], argv[2:]
        p = ledger_path()
        if sub == "ingest":
            return ingest(open(args[0]).read(), p)
        if sub == "resolve":
            return resolve(p, args[0], args[1], " ".join(args[2:]))
        if sub == "decide":
            return decide(p, args[0], args[1], " ".join(args[2:]))
        if sub == "report":
            return print(report(p, share="--share" in args))
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
