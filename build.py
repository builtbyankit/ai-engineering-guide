"""Build the static site into ./site from ./content and ./curriculum.json.

Usage: python3 build.py
Needs: markdown, beautifulsoup4, pygments (pip install -r requirements.txt)
"""
import hashlib
import html
import json
import math
import re
import shutil
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, NavigableString
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUT = ROOT / "site"
PAGES = OUT / "pages"
CUR = json.loads((ROOT / "curriculum.json").read_text(encoding="utf-8"))
REPO_URL = "https://github.com/builtbyankit/ai-agent-engineering-guide"
SITE_TITLE = "AI Agent Engineering Guide"
CHECKED = "16 Oct 2026"
HOURS = (10, 12)  # hours per week, low and high

TIER_NAME = {"M": "Must ship", "R": "Recommended", "S": "Stretch"}
TIER_OF = {v: k for k, v in TIER_NAME.items()}
LANG_LABEL = {"python": "Python", "bash": "Shell", "json": "JSON", "yaml": "YAML", "text": "Text", "sql": "SQL",
              "toml": "TOML", "dockerfile": "Dockerfile", "markdown": "Markdown", "javascript": "JavaScript"}
FMT = HtmlFormatter(nowrap=True)
RES_RE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>https?://[^)\s]+)\) · (?P<source>[^·]+?) · (?P<type>[^·]+?) · "
                    r"(?P<cost>[^·]+?) · (?P<time>[^·]+?) — (?P<note>.+)$")


# ---------------- helpers ----------------
def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60].strip("-")


def rng(s):
    parts = [float(x) for x in s.split("–")]
    return parts[0], parts[-1]


def half(x):
    return math.floor(x * 2 + 0.5) / 2


def fmt_num(x):
    return f"{x:g}"


def fmt_range(lo, hi, unit):
    return f"{fmt_num(lo)} {unit}" if lo == hi else f"{fmt_num(lo)}–{fmt_num(hi)} {unit}"


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, text[m.end():]


def res_id(url):
    return "res-" + hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]


def esc(s):
    return html.escape(str(s), quote=True)


def render_code(lang, body):
    if lang in ("text", ""):
        code = html.escape(body)
    else:
        try:
            code = highlight(body, get_lexer_by_name(lang), FMT)
        except Exception:
            code = html.escape(body)
    label = LANG_LABEL.get(lang, (lang or "text").upper())
    return ('<figure class="code"><figcaption><span class="code-lang">'
            f'{label}</span><button class="copy" type="button">Copy</button>'
            f'</figcaption><div class="code-scroll"><pre><code>{code.rstrip()}'
            '</code></pre></div></figure>')


TYPE_CLASS = {"Course": "course", "Video": "video", "Article": "article", "Docs": "docs", "Tutorial": "tutorial",
              "Paper": "paper", "Book": "book", "Repo": "repo", "Tool": "tool"}


def resource_card(r):
    rid = res_id(r["url"])
    cost = "" if r["cost"] == "Free" else f'<span class="res-cost">{esc(r["cost"])}</span>'
    return (f'<li class="res" data-res="{rid}"><input class="res-box" type="checkbox" id="{rid}" '
            f'aria-label="Mark “{esc(r["title"])}” as done" title="Mark as done">'
            f'<div class="res-body"><a class="res-title" href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">'
            f'{esc(r["title"])}</a>'
            f'<p class="res-meta"><span class="res-type t-{TYPE_CLASS[r["type"]]}">{esc(r["type"])}</span>'
            f'<span>{esc(r["source"])}</span><span>{esc(r["time"])}</span>{cost}</p>'
            f'<p class="res-note">{esc(r["note"])}</p></div></li>')


def md_to_soup(md):
    """Render markdown; resource lines become cards, fenced code becomes highlighted figures."""
    blocks, resources = [], []

    def stash(m):
        blocks.append(render_code(m.group(1).strip(), m.group(2)))
        return f"\n\nCODEPH{len(blocks) - 1:04d}\n\n"

    md = re.sub(r"^```(\w*)\n(.*?)\n```$", stash, md, flags=re.M | re.S)
    lines = []
    section = ""
    for line in md.splitlines():
        h = re.match(r"^#{2,3} (.+)$", line)
        if h:
            section = h.group(1).strip()
        m = RES_RE.match(line.strip())
        if m:
            r = m.groupdict()
            r["section"] = section
            resources.append(r)
            lines.append(f"- RESPH{len(resources) - 1:04d}")
        else:
            lines.append(line)
    # python-markdown needs a blank line between a paragraph and a list that follows it
    spaced = []
    for line in lines:
        prev = spaced[-1] if spaced else ""
        if (re.match(r"^(?:[-*]|\d+\.) ", line) and prev.strip()
                and not re.match(r"^\s*(?:[-*]|\d+\.) ", prev) and not prev.startswith(("#", "|", "    "))):
            spaced.append("")
        spaced.append(line)
    md = "\n".join(spaced)
    md = re.sub(r"^ {2,3}(?=(?:[-*]|\d+\.) )", "    ", md, flags=re.M)
    out = markdown.markdown(md, extensions=["tables", "sane_lists"])
    for i, b in enumerate(blocks):
        out = out.replace(f"<p>CODEPH{i:04d}</p>", b)
    soup = BeautifulSoup(out, "html.parser")
    for li in soup.find_all("li"):
        t = li.get_text().strip()
        m = re.fullmatch(r"RESPH(\d{4})", t)
        if m:
            card = BeautifulSoup(resource_card(resources[int(m.group(1))]), "html.parser")
            li.replace_with(card)
    for ul in soup.find_all("ul"):
        if ul.find("li", class_="res", recursive=False):
            ul["class"] = "res-list"
    return soup, resources


def finish(soup, page_id, gate_prefix=None, gate_heading="Milestone"):
    """Wrap tables, mark external links, give headings ids, and turn checklists into saved checkboxes."""
    for table in soup.find_all("table"):
        table.wrap(soup.new_tag("div", attrs={"class": "table-scroll"}))
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("http"):
            a["target"] = "_blank"
            a["rel"] = "noopener noreferrer"
    for h in soup.find_all(["h2", "h3"]):
        h["id"] = f"{page_id}--{slug(h.get_text())}"

    gates = todos = 0
    tiers = ""
    if gate_prefix:
        for h in soup.find_all("h2"):
            if h.get_text().strip() != gate_heading:
                continue
            gate = soup.new_tag("section", attrs={"class": "gate", "data-gate": gate_prefix})
            h.insert_before(gate)
            head = soup.new_tag("div", attrs={"class": "gate-head"})
            head.append(h.extract())
            cnt = soup.new_tag("span", attrs={"class": "gate-count", "data-count-for": gate_prefix})
            cnt.string = "0 / 0"
            head.append(cnt)
            gate.append(head)
            nxt = gate.find_next_sibling()
            while nxt is not None and nxt.name in ("p", "ul"):
                following = nxt.find_next_sibling()
                if nxt.name == "ul":
                    nxt["class"] = "checks"
                gate.append(nxt.extract())
                nxt = following

    for ul in soup.find_all("ul"):
        items = ul.find_all("li", recursive=False)
        is_gate = ul.find_parent("section", class_="gate") is not None
        converted = False
        for li in items:
            first = li.contents[0] if li.contents else None
            if not (isinstance(first, NavigableString) and first.lstrip().startswith("[ ] ")):
                continue
            converted = True
            first.replace_with(first.lstrip()[4:])
            first = li.contents[0]
            if is_gate:
                gates += 1
                cid = f"{gate_prefix}-gate-{gates}"
                tier = None
            else:
                todos += 1
                cid = f"{page_id}-todo-{todos}"
                tm = re.match(r"\[(Must ship|Recommended|Stretch)\] ", str(first))
                assert tm, f"{page_id}: task {todos} has no tier tag"
                tier = TIER_OF[tm.group(1)]
                tiers += tier
                first.replace_with(str(first)[tm.end():])
                li["data-tier"] = tier
            label = soup.new_tag("label", attrs={"for": cid})
            box = soup.new_tag("input", attrs={"type": "checkbox", "id": cid})
            span = soup.new_tag("span")
            for c in list(li.contents):
                span.append(c.extract())
            if tier:
                chip = soup.new_tag("span", attrs={"class": f"tier tier-{tier}"})
                chip.string = TIER_NAME[tier]
                span.insert(0, chip)
            label.append(box)
            label.append(span)
            li.append(label)
        if converted and not is_gate:
            ul["class"] = "checks todo"
    return {"gates": gates, "todos": todos, "tiers": tiers}


def headings_of(soup):
    return [h.get_text().strip() for h in soup.find_all(["h2", "h3"])]


# ---------------- load content ----------------
levels = CUR["levels"]
LEVEL_IDS = [lv["id"] for lv in levels]
TIERS_LABEL = {lv["id"]: lv["tier"] for lv in levels}

routes, order = {}, []
gate_totals, task_totals, task_tiers, page_res = {}, {}, {}, {}
library = {}  # url -> resource dict with uses
fragments = {}
level_weeks = {}
optional_ids = set()


def add_resources(page_id, resources):
    ids = []
    for r in resources:
        rid = res_id(r["url"])
        ids.append(rid)
        entry = library.setdefault(r["url"], {
            "id": rid, "url": r["url"], "title": r["title"], "source": r["source"], "type": r["type"],
            "cost": r["cost"], "time": r["time"], "note": r["note"], "uses": []})
        entry["uses"].append([page_id, r["section"]])
    page_res[page_id] = ids


def meta_line(parts):
    return '<p class="page-meta">' + " · ".join(parts) + "</p>"


# start page
start_fm, start_body = front_matter((CONTENT / "pages" / "start.md").read_text(encoding="utf-8"))

# levels, modules, projects
level_info = []
for lv in levels:
    lid = lv["id"]
    lfm, lbody = front_matter((CONTENT / "levels" / f"{lid}.md").read_text(encoding="utf-8"))
    mods = []
    for i, m in enumerate(lv["modules"], 1):
        fm, body = front_matter((CONTENT / "modules" / f"{m['id']}.md").read_text(encoding="utf-8"))
        mods.append((m, fm, body))
        if m["kind"] == "optional":
            optional_ids.add(m["id"])
    pid = lv["project"]["id"]
    pfm, pbody = front_matter((CONTENT / "projects" / f"{pid}.md").read_text(encoding="utf-8"))
    core_lo = sum(rng(m["hours"])[0] for m, _, _ in mods if m["kind"] == "core")
    core_hi = sum(rng(m["hours"])[1] for m, _, _ in mods if m["kind"] == "core")
    opt_lo = sum(rng(m["hours"])[0] for m, _, _ in mods if m["kind"] == "optional")
    opt_hi = sum(rng(m["hours"])[1] for m, _, _ in mods if m["kind"] == "optional")
    p_lo, p_hi = rng(pfm["weeks"])
    weeks = {
        "core": (half(core_lo / HOURS[1] + p_lo), half(core_hi / HOURS[0] + p_hi)),
        "full": (half((core_lo + opt_lo) / HOURS[1] + p_lo), half((core_hi + opt_hi) / HOURS[0] + p_hi)),
        "mods": ((core_lo / HOURS[1] + core_hi / HOURS[0]) / 2, ((core_lo + opt_lo) / HOURS[1] + (core_hi + opt_hi) / HOURS[0]) / 2),
        "proj": (p_lo + p_hi) / 2,
    }
    assert lfm["weeks"] == fmt_range(*weeks["core"], "").strip(), f"{lid}: page weeks {lfm['weeks']} vs computed {weeks['core']}"
    level_weeks[lid] = weeks
    level_info.append((lv, lfm, lbody, mods, pid, pfm, pbody))

cap_fm, cap_body = front_matter((CONTENT / "projects" / "capstone.md").read_text(encoding="utf-8"))
cap_weeks = rng(cap_fm["weeks"])

total = {}
for tr in ("core", "full"):
    lo = sum(level_weeks[l][tr][0] for l in LEVEL_IDS) + cap_weeks[0]
    hi = sum(level_weeks[l][tr][1] for l in LEVEL_IDS) + cap_weeks[1]
    total[tr] = (lo, hi)
DURATION = {tr: {"weeks": fmt_range(*total[tr], "weeks"),
                 "hours": f"about {round(total[tr][0] * HOURS[0], -1):g}–{round(total[tr][1] * HOURS[1], -1):g} hours at 10–12 hours a week"}
            for tr in total}

# ---------------- render pages ----------------
def page_head(eyebrow, timebox, title, standfirst, meta, chips=""):
    tb = f'<span class="timebox">{esc(timebox)}</span>' if timebox else ""
    return (f'<header class="page-head"><p class="eyebrow">{eyebrow}{tb}</p>'
            f'<h1 tabindex="-1">{esc(title)}{chips}</h1>'
            f'<p class="standfirst">{esc(standfirst)}</p>{meta}</header>')


def level_table():
    rows = ["| Level | What you learn | Project | Core weeks |", "| --- | --- | --- | --- |"]
    for lv, lfm, *_rest in level_info:
        pid = lv["project"]["id"]
        rows.append(f"| [{lv['num']}. {lv['title']}](#{lv['id']}) | {lv['summary']} | [{lv['project']['title']}](#{pid}) | "
                    f"{fmt_range(*level_weeks[lv['id']]['core'], '')} |")
    rows.append(f"| [Capstone](#capstone) | Build and ship a new production agent that uses every core skill. | "
                f"[Ship a production agent](#capstone) | {fmt_range(*cap_weeks, '')} |")
    return "\n".join(rows)


start_md = (start_body.replace("%%LEVEL_TABLE%%", level_table())
            .replace("%%CORE_WEEKS%%", DURATION["core"]["weeks"])
            .replace("%%FULL_WEEKS%%", DURATION["full"]["weeks"])
            .replace("%%REPO_URL%%", REPO_URL))
soup, _ = md_to_soup(start_md)
finish(soup, "start")
fragments["start"] = (page_head("Start here", "", start_fm["title"], start_fm["summary"], "") +
                      f'<div class="prose">{soup}</div>')
routes["start"] = {"t": start_fm["title"], "k": "page", "s": "start", "e": "Start here", "sum": start_fm["summary"], "h": headings_of(soup)}
order.append("start")


def module_page(lv, idx, n_mods, m, fm, body):
    mid = m["id"]
    soup, resources = md_to_soup(body)
    info = finish(soup, mid)
    task_totals[mid] = info["todos"]
    task_tiers[mid] = info["tiers"]
    add_resources(mid, resources)
    chip = ' <span class="chip chip-opt">Optional</span>' if m["kind"] == "optional" else ""
    meta = meta_line([f'Must ship <span data-must-for="{mid}">0/0</span>',
                      f'Resources done <span data-res-for="{mid}">0/{len(resources)}</span>',
                      f"Links checked {CHECKED}"])
    eyebrow = f'<a href="#{lv["id"]}">Level {lv["num"]}</a> · Module {idx} of {n_mods}'
    fragments[mid] = page_head(eyebrow, f'{m["hours"]} h', fm["title"], fm["summary"], meta, chip) + f'<div class="prose">{soup}</div>'
    learn = [b.get_text().split(":")[0] for b in soup.find_all("strong")][:12]
    routes[mid] = {"t": fm["title"], "k": "module", "s": lv["id"], "e": f"Level {lv['num']}", "sum": fm["summary"],
                   "h": headings_of(soup) + learn, "opt": m["kind"] == "optional", "hrs": m["hours"]}
    return info


def project_page(lv, pid, pfm, pbody, capstone=False):
    soup, resources = md_to_soup(pbody)
    info = finish(soup, pid)
    task_totals[pid] = info["todos"]
    task_tiers[pid] = info["tiers"]
    add_resources(pid, resources)
    meta = meta_line([f'Requirements <span data-must-for="{pid}">0/0</span>',
                      f'Stretch goals <span data-extra-for="{pid}">0/0</span>'])
    eyebrow = "Capstone" if capstone else f'<a href="#{lv["id"]}">Level {lv["num"]}</a> · Project'
    fragments[pid] = page_head(eyebrow, f'{pfm["weeks"]} weeks', pfm["title"], pfm["summary"], meta) + f'<div class="prose">{soup}</div>'
    routes[pid] = {"t": pfm["title"], "k": "capstone" if capstone else "project", "s": "capstone" if capstone else lv["id"],
                   "e": "Capstone" if capstone else f"Level {lv['num']} project", "sum": pfm["summary"], "h": headings_of(soup),
                   "wk": pfm["weeks"]}


def level_page(lv, lfm, lbody, mods, pid, pfm):
    lid = lv["id"]
    soup, _ = md_to_soup(lbody)
    info = finish(soup, lid, gate_prefix=lid)
    gate_totals[lid] = info["gates"]
    # module list and project card go right before the milestone
    rows = []
    for i, (m, fm, _b) in enumerate(mods, 1):
        chip = '<span class="chip chip-opt">Optional</span>' if m["kind"] == "optional" else ""
        rows.append(f'<li{" data-opt" if m["kind"] == "optional" else ""}><a class="topic" href="#{m["id"]}"><span class="t-num">{i:02d}</span>'
                    f'<span class="t-body"><span class="t-title">{esc(fm["title"])}{chip}</span><span class="t-sum">{esc(fm["summary"])}</span></span>'
                    f'<span class="t-meta"><span>{esc(m["hours"])} h</span><span class="t-tasks"><span data-must-for="{m["id"]}">0/0</span> must ship</span></span></a></li>')
    mod_html = (f'<h2 id="{lid}--modules">Modules</h2><p class="topics-intro">{len(mods)} modules, in suggested order. '
                f'Hours cover the Start here resources, the practice and the must-ship tasks.</p><ol class="topics">{"".join(rows)}</ol>'
                f'<h2 id="{lid}--project">Project</h2>'
                f'<a class="project-card" href="#{pid}"><span class="card-eyebrow">Level {lv["num"]} project · {esc(pfm["weeks"])} weeks</span>'
                f'<span class="card-title">{esc(pfm["title"])}</span><span class="t-sum">{esc(pfm["summary"])}</span>'
                f'<span class="card-foot"><span>Requirements <span data-must-for="{pid}">0/0</span></span><span>Open the brief →</span></span></a>')
    gate = soup.find("section", class_="gate")
    gate.insert_before(BeautifulSoup(mod_html, "html.parser"))
    wk = level_weeks[lid]
    timebox = fmt_range(*wk["core"], "weeks")
    if wk["full"] != wk["core"]:
        timebox += f" (+{fmt_num(half(wk['full'][0] - wk['core'][0]))}–{fmt_num(half(wk['full'][1] - wk['core'][1]))} optional)"
    meta = meta_line([f'Milestone <span data-count-for="{lid}">0/{info["gates"]}</span>',
                      f'Must-ship tasks <span data-level-must="{lid}">0/0</span>'])
    eyebrow = f"Level {lv['num']} · {esc(lv['tier'])}"
    fragments[lid] = page_head(eyebrow, timebox, lv["title"], lfm["summary"], meta) + f'<div class="prose">{soup}</div>'
    routes[lid] = {"t": lv["title"], "k": "level", "s": lid, "e": f"Level {lv['num']}", "sum": lfm["summary"],
                   "h": headings_of(soup), "num": lv["num"]}


for lv, lfm, lbody, mods, pid, pfm, pbody in level_info:
    lid = lv["id"]
    order.append(lid)
    level_page(lv, lfm, lbody, mods, pid, pfm)
    for i, (m, fm, body) in enumerate(mods, 1):
        module_page(lv, i, len(mods), m, fm, body)
        order.append(m["id"])
    project_page(lv, pid, pfm, pbody)
    order.append(pid)
project_page(None, "capstone", cap_fm, cap_body, capstone=True)
order.append("capstone")
routes["resources"] = {"t": "Resource library", "k": "page", "s": "resources", "e": "Start here",
                       "sum": "Every link in the guide in one place, searchable by type, level and cost.", "h": []}
routes["progress"] = {"t": "Your progress", "k": "page", "s": "progress", "e": "Start here",
                      "sum": "Milestones, tasks and resources you have finished, with backup and restore.", "h": []}

# ---------------- internal link check ----------------
broken = []
for pid, frag in fragments.items():
    for target in re.findall(r'href="#([^"]+)"', frag):
        if target not in routes and target != "home" and "--" not in target:
            broken.append((pid, target))
assert not broken, broken

# ---------------- navigation ----------------
def nav_html():
    out = ['<div class="nav-group"><p class="nav-heading">Start here</p><ul class="nav-list">']
    for rid, num in (("start", "→"), ("resources", "◇"), ("progress", "✓")):
        out.append(f'<li><div class="nav-row"><a href="#{rid}" data-route="{rid}"><span class="nav-num">{num}</span>'
                   f'<span>{esc(routes[rid]["t"])}</span></a></div></li>')
    out.append('</ul></div><div class="nav-group"><p class="nav-heading">Levels</p><ul class="nav-list">')
    for lv, lfm, lbody, mods, pid, pfm, pbody in level_info:
        lid = lv["id"]
        subs = []
        for m, fm, _b in mods:
            tag = '<span class="nav-tag">Optional</span>' if m["kind"] == "optional" else ""
            subs.append(f'<li{" data-opt" if m["kind"] == "optional" else ""}><a href="#{m["id"]}" data-route="{m["id"]}">{esc(fm["title"])}{tag}</a></li>')
        subs.append(f'<li><a href="#{pid}" data-route="{pid}">Project: {esc(pfm["title"])}</a></li>')
        out.append(f'<li class="nav-sec" data-sec="{lid}"><div class="nav-row"><a href="#{lid}" data-route="{lid}">'
                   f'<span class="nav-num">L{lv["num"]}</span><span>{esc(lv["title"])}</span>'
                   f'<span class="nav-count" data-count-for="{lid}">0/0</span></a>'
                   f'<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="sub-{lid}">'
                   f'<span class="sr-only">Show modules in {esc(lv["title"])}</span></button></div>'
                   f'<ul class="nav-sub" id="sub-{lid}" hidden>{"".join(subs)}</ul></li>')
    out.append('</ul></div><div class="nav-group"><p class="nav-heading">Finish</p><ul class="nav-list">'
               '<li class="nav-sec" data-sec="capstone"><div class="nav-row"><a href="#capstone" data-route="capstone">'
               '<span class="nav-num">★</span><span>Capstone</span>'
               '<span class="nav-count" data-must-for="capstone">0/0</span></a></div></li></ul></div>')
    return "".join(out)


# ---------------- home: route chart and cards ----------------
def route_figure(tr):
    rows, t = [], 0.0
    for lv, *_ in level_info:
        w = level_weeks[lv["id"]]
        mods_w = w["mods"][0 if tr == "core" else 1]
        rows.append((lv["id"], f"L{lv['num']} {lv['title']}", fmt_range(*w[tr], "wk"), t, mods_w, w["proj"]))
        t += mods_w + w["proj"]
    cap_mid = sum(cap_weeks) / 2
    rows.append(("capstone", "Capstone", fmt_range(*cap_weeks, "wk"), t, 0.0, cap_mid))
    t += cap_mid
    axis = math.ceil(total[tr][1])
    html_rows = []
    for rid, label, est, start, mw, pw in rows:
        bars = ""
        if mw:
            bars += f'<span class="route-bar" style="left:{start / axis * 100:.3f}%;width:{mw / axis * 100:.3f}%"></span>'
        bars += f'<span class="route-bar route-bar-proj" style="left:{(start + mw) / axis * 100:.3f}%;width:{pw / axis * 100:.3f}%"></span>'
        inner = (f'<span class="route-label"><span class="route-name">{esc(label)}</span><span class="route-est">{est}</span></span>'
                 f'<span class="route-track">{bars}</span>')
        html_rows.append(f'<li class="route-row" data-sec="{rid}"><a href="#{rid}">{inner}</a></li>')
    buf = (f'<span class="route-label"><span class="route-name">Buffer</span><span class="route-est">to {axis} wk</span></span>'
           f'<span class="route-track"><span class="route-bar route-buffer" style="left:{t / axis * 100:.3f}%;width:{(axis - t) / axis * 100:.3f}%"></span></span>')
    html_rows.append(f'<li class="route-row"><div class="route-static">{buf}</div></li>')
    step = 5 if axis <= 50 else 10
    ticks = "".join(f'<span class="tick" style="left:{wk / axis * 100:.3f}%">{wk}</span>' for wk in range(0, axis + 1, step))
    name = "Core path" if tr == "core" else "Everything, including optional modules"
    cap = (f"{name}: {DURATION[tr]['weeks']} at 10–12 hours a week. Each bar starts where the previous level ends and uses the "
           "midpoint of its estimate. Modules are blue, projects amber. The buffer runs to the top of the range.")
    return (f'<figure class="route" data-track-view="{tr}" style="--axis:{axis}"{" hidden" if tr == "full" else ""} '
            f'aria-labelledby="route-title-{tr}"><div class="route-top"><p class="route-title" id="route-title-{tr}">The path, to scale</p>'
            '<ul class="legend"><li><span class="sw sw-stage"></span>Modules</li><li><span class="sw sw-proj"></span>Project</li>'
            '<li><span class="sw sw-buffer"></span>Buffer</li><li><span class="sw sw-done"></span>Milestone complete</li></ul></div>'
            f'<ol class="route-rows">{"".join(html_rows)}</ol>'
            f'<div class="route-axis" aria-hidden="true"><span class="axis-unit">weeks</span><span class="route-ticks">{ticks}</span></div>'
            f'<figcaption>{cap}</figcaption></figure>')


def home_cards():
    cards = []
    for lv, lfm, *_ in level_info:
        lid = lv["id"]
        cards.append(f'<li><a class="card" href="#{lid}"><span class="card-eyebrow">Level {lv["num"]} · {esc(lv["tier"])}</span>'
                     f'<span class="card-title">{esc(lv["title"])}</span><span class="card-sum">{esc(lv["summary"])}</span>'
                     f'<span class="card-foot"><span>{fmt_range(*level_weeks[lid]["core"], "wk")}</span>'
                     f'<span class="card-prog" data-count-for="{lid}">0/0</span></span></a></li>')
    cards.append(f'<li><a class="card card-cap" href="#capstone"><span class="card-eyebrow">Finish</span>'
                 f'<span class="card-title">Capstone</span><span class="card-sum">{esc(cap_fm["summary"])}</span>'
                 f'<span class="card-foot"><span>{fmt_range(*cap_weeks, "wk")}</span><span class="card-prog" data-must-for="capstone">0/0</span></span></a></li>')
    return f'<section class="home-group"><h2>The path</h2><ul class="cards">{"".join(cards)}</ul></section>'


# ---------------- data and output ----------------
lib = sorted(library.values(), key=lambda r: order.index(r["uses"][0][0]))
data = {
    "routes": routes, "order": order, "gates": gate_totals, "tasks": task_totals, "tiers": task_tiers,
    "pageRes": page_res, "optional": sorted(optional_ids), "resources": lib, "duration": DURATION, "checked": CHECKED,
    "levels": [{"id": lv["id"], "num": lv["num"], "t": lv["title"], "modules": [m["id"] for m, _, _ in mods], "project": pid}
               for lv, lfm, lbody, mods, pid, pfm, pbody in level_info],
}

if OUT.exists():
    shutil.rmtree(OUT)
PAGES.mkdir(parents=True)
for pid, frag in fragments.items():
    (PAGES / f"{pid}.html").write_text(frag, encoding="utf-8")

n_res = len(lib)
n_free = sum(1 for r in lib if r["cost"] == "Free")
n_paid = sum(1 for r in lib if r["cost"] == "Paid")
n_mod_core = sum(1 for lv in levels for m in lv["modules"] if m["kind"] == "core")
n_mod_opt = len(optional_ids)
tpl = (ROOT / "template.html").read_text(encoding="utf-8")
page = (tpl.replace("%%NAV%%", nav_html())
        .replace("%%ROUTE%%", route_figure("core") + route_figure("full"))
        .replace("%%CARDS%%", home_cards())
        .replace("%%DATA%%", json.dumps(data, ensure_ascii=True).replace("</", "<\\/"))
        .replace("%%CORE_WEEKS%%", DURATION["core"]["weeks"])
        .replace("%%FULL_WEEKS%%", DURATION["full"]["weeks"])
        .replace("%%CORE_HOURS%%", DURATION["core"]["hours"])
        .replace("%%N_RES%%", str(n_res))
        .replace("%%N_FREE%%", str(n_free))
        .replace("%%N_CORE_MODULES%%", str(n_mod_core))
        .replace("%%N_OPT_MODULES%%", str(n_mod_opt))
        .replace("%%N_PROJECTS%%", str(len(levels) + 1))
        .replace("%%REPO_URL%%", REPO_URL)
        .replace("%%CHECKED%%", CHECKED))
assert "%%" not in page, re.findall(r"%%\w+%%", page)
(OUT / "index.html").write_text(page, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
(OUT / "404.html").write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    f'<title>Page not found · {SITE_TITLE}</title><meta http-equiv="refresh" content="0; url=./"></head>'
    '<body><p>Page not found. <a href="./">Go to the guide</a>.</p></body></html>', encoding="utf-8")
shutil.copy(ROOT / "favicon.svg", OUT / "favicon.svg")

size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"pages {len(fragments)} | gates {sum(gate_totals.values())} | tasks {sum(task_totals.values())} | "
      f"must {sum(v.count('M') for v in task_tiers.values())} | resources {n_res} ({n_free} free) | "
      f"core {DURATION['core']['weeks']} | full {DURATION['full']['weeks']} | {size / 1e6:.2f} MB")
