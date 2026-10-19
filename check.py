"""Validate guide pages: front matter, headings, resource lines, checklists, links and style.

Usage: python3 check.py content/modules/l1-how-llms-work.md [more files...]
       python3 check.py --all
       python3 check.py --due    # list time-sensitive claims whose review-by date has passed
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CUR = json.loads((ROOT / "curriculum.json").read_text(encoding="utf-8"))

IDS = {"home", "start", "resources", "progress", "capstone"}
MODULES, PROJECTS = {}, {}
for lv in CUR["levels"]:
    IDS.add(lv["id"])
    for m in lv["modules"]:
        IDS.add(m["id"]); MODULES[m["id"]] = (lv["id"], m)
    IDS.add(lv["project"]["id"]); PROJECTS[lv["project"]["id"]] = lv["id"]
PROJECTS["capstone"] = "capstone"
INTERVIEW = {pg["id"]: pg for pg in CUR.get("interview", {}).get("pages", [])}
IDS.update(INTERVIEW)

TYPES = {"Course", "Video", "Article", "Docs", "Tutorial", "Paper", "Book", "Repo", "Tool"}
COSTS = {"Free", "Free to audit", "Free tier", "Paid"}
TIME_RE = re.compile(r"^(\d+(\.\d+)?(–\d+(\.\d+)?)? (min|h)|self-paced|reference)$")
RES_RE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>https?://[^)\s]+)\) · (?P<source>[^·]+?) · (?P<type>[^·]+?) · (?P<cost>[^·]+?) · (?P<time>[^·]+?) — (?P<note>.+)$")
TIER_RE = re.compile(r"^\[(Must ship|Recommended|Stretch)\] ")
BANNED = ["lumagine", "it's worth noting", "fast-paced world", "game-changer", "game changer", "delve", "dive into", "unlock", "landscape"]

MODULE_H2 = ["Why it matters", "What to learn", "Resources", "Practice", "Checklist", "You're ready when"]
LEVEL_H2 = ["What you'll be able to do", "Before you start", "How to work through this level", "Milestone"]
PROJECT_H2 = ["The brief", "What you'll practise", "Requirements", "Stretch goals", "Suggested stack",
              "Build it step by step", "How to evaluate it", "Show your work", "Ideas to make it yours", "Helpful resources"]


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


REVIEW_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2}) \| (?P<phrase>.+)$")


def review_items(text):
    """Return (date, phrase, raw) for every 'review-by: YYYY-MM-DD | exact phrase' line in the front matter.

    A review-by line marks a time-sensitive claim (a price, a free tier, a version, a deprecation date).
    The phrase must appear on the page, so the marker is removed when the claim is.
    """
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = []
    if not m:
        return out
    for line in m.group(1).splitlines():
        if line.startswith("review-by:"):
            raw = line.split(":", 1)[1].strip()
            r = REVIEW_RE.match(raw)
            out.append((r.group("date") if r else None, r.group("phrase").strip() if r else None, raw))
    return out


def check_reviews(text, body, errors, warns, today):
    flat = " ".join(body.split())
    for date, phrase, raw in review_items(text):
        if not date:
            errors.append(f"review-by should be 'YYYY-MM-DD | exact phrase from the page', got: {raw[:80]}")
            continue
        try:
            due = datetime.date.fromisoformat(date)
        except ValueError:
            errors.append(f"review-by has an invalid date: {date}")
            continue
        if " ".join(phrase.split()) not in flat:
            errors.append(f"review-by phrase not found on the page: {phrase[:80]}")
        elif due <= today:
            warns.append(f"review-by {date} has passed; re-check against its source: {phrase[:80]}")


def strip_code(body):
    return re.sub(r"^```.*?^```", "", body, flags=re.M | re.S)


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        h = re.match(r"^## (.+)$", line)
        if h:
            cur = h.group(1).strip(); out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def parse_resource(line):
    m = RES_RE.match(line.strip())
    return m.groupdict() if m else None


def check_resources(lines, errors, warns, where):
    found = []
    for ln in lines:
        s = ln.strip()
        if not s.startswith("- ["):
            if s.startswith("- ") or s.startswith("* "):
                errors.append(f"{where}: bullet is not a resource line: {s[:80]}")
            continue
        r = parse_resource(s)
        if not r:
            errors.append(f"{where}: malformed resource line: {s[:100]}")
            continue
        if r["type"] not in TYPES:
            errors.append(f"{where}: bad type '{r['type']}' in {r['url']}")
        if r["cost"] not in COSTS:
            errors.append(f"{where}: bad cost '{r['cost']}' in {r['url']}")
        if not TIME_RE.match(r["time"]):
            errors.append(f"{where}: bad time '{r['time']}' in {r['url']} (use e.g. '25 min', '1.5 h', '2–3 h', 'self-paced', 'reference')")
        if len(r["note"].split()) < 6:
            warns.append(f"{where}: very short note for {r['url']}")
        found.append(r)
    return found


def check_checklist(lines, errors, where, tiers=True):
    items = [l.strip()[6:] for l in lines if l.strip().startswith("- [ ] ")]
    for it in items:
        if tiers and not TIER_RE.match(it):
            errors.append(f"{where}: checklist item lacks a tier tag: {it[:70]}")
        if not tiers and TIER_RE.match(it):
            errors.append(f"{where}: milestone gate should not have a tier tag: {it[:70]}")
    return items


def check_file(path):
    errors, warns = [], []
    p = Path(path).resolve()
    text = p.read_text(encoding="utf-8")
    fm, body = front_matter(text)
    if fm is None:
        return [f"{p}: missing front matter"], []
    check_reviews(text, body, errors, warns, datetime.date.today())
    kind = p.parent.name
    pid = p.stem
    prose = strip_code(body)
    secs = sections(prose)

    if re.search(r"^# ", prose, re.M):
        errors.append("H1 heading found")
    if re.search(r"<[a-zA-Z/][^>]*>", prose.replace("<", "<", 1)) and re.search(r"</?(div|span|img|br|a|p|table)\b", prose):
        errors.append("HTML tags found")
    if "```mermaid" in body:
        errors.append("mermaid block found")
    for fence in re.findall(r"^```(.*)$", body, re.M):
        pass
    opens = re.findall(r"^```(\S*)", body, re.M)
    if len(opens) % 2:
        errors.append("unbalanced code fences")
    for i in range(0, len(opens), 2):
        if not opens[i]:
            errors.append("code fence without a language")
    low = prose.lower()
    for b in BANNED:
        if b in low:
            errors.append(f"banned phrase or word: '{b}'")
    # em dashes outside resource lines
    for ln in prose.splitlines():
        if "—" in ln and not RES_RE.match(ln.strip()):
            warns.append(f"em dash outside a resource line: {ln.strip()[:80]}")
    # internal links
    for target in re.findall(r"\]\(#([^)]+)\)", prose):
        if target not in IDS:
            errors.append(f"internal link to unknown id #{target}")
    for k in ("title", "summary"):
        if not fm.get(k):
            errors.append(f"front matter missing {k}")
    if fm.get("summary") and len(fm["summary"].split()) > 30:
        errors.append("summary longer than 30 words")

    resources = []
    if kind == "modules":
        if pid not in MODULES:
            errors.append(f"unknown module id {pid}")
        else:
            lv, m = MODULES[pid]
            for k, v in (("level", lv), ("kind", m["kind"]), ("hours", m["hours"])):
                if fm.get(k) != v:
                    errors.append(f"front matter {k} should be '{v}', got '{fm.get(k)}'")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm.get("checked", "")):
            warns.append("checked should be a date like 2026-10-16")
        heads = list(secs)
        if heads != MODULE_H2:
            errors.append(f"H2 headings must be exactly {MODULE_H2}, got {heads}")
        res_lines = secs.get("Resources", [])
        subs = [l[4:].strip() for l in res_lines if l.startswith("### ")]
        if subs != ["Start here", "Go deeper", "Reference"]:
            errors.append(f"Resources needs H3s Start here, Go deeper, Reference; got {subs}")
        # count per subsection
        cur, counts = None, {}
        for l in res_lines:
            if l.startswith("### "):
                cur = l[4:].strip(); counts[cur] = 0
            elif l.strip().startswith("- [") and cur:
                counts[cur] += 1
        for name, lo, hi in (("Start here", 2, 3), ("Go deeper", 3, 6), ("Reference", 2, 5)):
            n = counts.get(name, 0)
            if not lo <= n <= hi:
                errors.append(f"'{name}' should have {lo}–{hi} resources, has {n}")
        resources = check_resources([l for l in res_lines if not l.startswith("### ")], errors, warns, "Resources")
        if len({r["type"] for r in resources}) < 3:
            errors.append("resources need at least three different types")
        learn = [l for l in secs.get("What to learn", []) if l.strip().startswith("- ")]
        if not 6 <= len(learn) <= 10:
            errors.append(f"What to learn should have 6–10 bullets, has {len(learn)}")
        for l in learn:
            if not re.match(r"^- \*\*[^*]+\*\*: ", l.strip()):
                errors.append(f"What to learn bullet format should be '- **Concept**: ...': {l.strip()[:60]}")
        prac = [l for l in secs.get("Practice", []) if re.match(r"^\d+\. ", l.strip())]
        if not 3 <= len(prac) <= 5:
            errors.append(f"Practice should have 3–5 numbered exercises, has {len(prac)}")
        items = check_checklist(secs.get("Checklist", []), errors, "Checklist")
        if not 4 <= len(items) <= 7:
            errors.append(f"Checklist should have 4–7 items, has {len(items)}")
        if not any(i.startswith("[Must ship]") for i in items):
            errors.append("Checklist needs at least one [Must ship] item")
        ready = [l for l in secs.get("You're ready when", []) if l.strip().startswith("- ")]
        if not 3 <= len(ready) <= 5:
            errors.append(f"You're ready when should have 3–5 bullets, has {len(ready)}")
        words = len(re.sub(r"^- \[.*$", "", prose, flags=re.M).split())
        if words < 380:
            warns.append(f"prose is short ({words} words excluding resource lines)")
        if words > 1100:
            warns.append(f"prose is long ({words} words excluding resource lines)")
    elif kind == "levels":
        if pid not in {l["id"] for l in CUR["levels"]}:
            errors.append(f"unknown level id {pid}")
        if not fm.get("weeks"):
            errors.append("front matter missing weeks")
        if list(secs) != LEVEL_H2:
            errors.append(f"H2 headings must be exactly {LEVEL_H2}, got {list(secs)}")
        gates = check_checklist(secs.get("Milestone", []), errors, "Milestone", tiers=False)
        if not 4 <= len(gates) <= 6:
            errors.append(f"Milestone should have 4–6 gate checks, has {len(gates)}")
    elif kind == "projects":
        if pid not in PROJECTS:
            errors.append(f"unknown project id {pid}")
        if not fm.get("weeks"):
            errors.append("front matter missing weeks")
        if list(secs) != PROJECT_H2:
            errors.append(f"H2 headings must be exactly {PROJECT_H2}, got {list(secs)}")
        req = check_checklist(secs.get("Requirements", []), errors, "Requirements")
        if not 5 <= len(req) <= 8 or any(not r.startswith("[Must ship]") for r in req):
            errors.append("Requirements should be 5–8 [Must ship] items")
        st = check_checklist(secs.get("Stretch goals", []), errors, "Stretch goals")
        if not 3 <= len(st) <= 5 or any(r.startswith("[Must ship]") for r in st):
            errors.append("Stretch goals should be 3–5 [Recommended]/[Stretch] items")
        if not any(l.strip().startswith("|") for l in secs.get("Suggested stack", [])):
            errors.append("Suggested stack needs a table")
        if not any(l.strip().startswith("|") for l in secs.get("How to evaluate it", [])):
            errors.append("How to evaluate it needs a table")
        resources = check_resources(secs.get("Helpful resources", []), errors, warns, "Helpful resources")
        if not 2 <= len(resources) <= 6:
            errors.append(f"Helpful resources should have 2–6 lines, has {len(resources)}")
    elif kind == "interview":
        if pid not in INTERVIEW:
            errors.append(f"unknown interview page id {pid}")
        elif fm.get("hours") != INTERVIEW[pid]["hours"]:
            errors.append(f"front matter hours should be '{INTERVIEW[pid]['hours']}', got '{fm.get('hours')}'")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm.get("checked", "")):
            warns.append("checked should be a date like 2026-10-16")
        heads = list(secs)
        if len(heads) < 3 or heads[-2:] != ["Checklist", "Resources"]:
            errors.append(f"interview pages end with '## Checklist' then '## Resources', got {heads}")
        if pid == "interview" and "%%PAGES%%" not in body:
            errors.append("the interview overview needs a %%PAGES%% line where the page list goes")
        items = check_checklist(secs.get("Checklist", []), errors, "Checklist")
        if not 3 <= len(items) <= 8:
            errors.append(f"Checklist should have 3–8 items, has {len(items)}")
        res_lines = [l for l in secs.get("Resources", []) if not l.startswith("### ")]
        resources = check_resources(res_lines, errors, warns, "Resources")
        if not 2 <= len(resources) <= 8:
            errors.append(f"Resources should have 2–8 lines, has {len(resources)}")
    else:
        warns.append(f"unknown page kind {kind}")

    urls = [r["url"] for r in resources]
    dup = {u for u in urls if urls.count(u) > 1}
    if dup:
        errors.append(f"duplicate URLs on page: {sorted(dup)}")
    return errors, warns


def list_due():
    today = datetime.date.today()
    due = []
    for f in sorted((ROOT / "content").glob("*/*.md")):
        text = f.read_text(encoding="utf-8")
        for date, phrase, _raw in review_items(text):
            if date and datetime.date.fromisoformat(date) <= today:
                due.append((date, f.relative_to(ROOT), phrase))
    for date, f, phrase in sorted(due):
        print(f"{date}  {f}: {phrase}")
    print(f"{len(due)} claim(s) due for review")


def main(argv):
    if argv == ["--due"]:
        list_due()
        return
    files = argv
    if argv == ["--all"]:
        files = sorted(str(p) for p in (ROOT / "content").glob("*/*.md") if p.parent.name != "pages")
    bad = 0
    for f in files:
        e, w = check_file(f)
        status = "OK" if not e else "FAIL"
        print(f"{f}: {status}")
        for x in e:
            print("  ERROR", x)
        for x in w:
            print("  warn ", x)
        bad += bool(e)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
