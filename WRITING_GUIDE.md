# Writing guide: AI Agent Engineering Guide (resource-first edition)

This guide sets the rules for every page of a free, public study website that takes a learner from "can code a little" to "can build, evaluate and run production AI agents". The site is resource-first: every module points the learner to the best existing blogs, courses, docs, videos, papers and repos, and adds short framing, practice, a checklist and a project. Pages come from several contributors, so follow this guide exactly. Consistency matters as much as quality.

## The reader

Someone who has written a little code (any language) and wants to become an AI agent engineer. They may be a student, a career switcher or a developer from another field. Assume nothing about their employer, stack or project. Explain jargon the first time it appears. Do not assume the reader is building any particular product.

## Source of truth for scope

`curriculum.json` lists every level, module and project with its id, title, kind (core or optional), hours and a `scope` note. Cover what the scope note lists, in roughly that order. Stay inside your module: link to other modules instead of re-teaching them. Read the scope notes of the modules before and after yours so the hand-offs are clean.

## Resource rules (the most important part)

1. **Open every URL you add.** Confirm that the page loads and is the resource you describe (right title, right topic, not a 404, not a parked domain, not a login wall for something you call free). If you cannot open it, do not use it, even if you are confident it exists.
2. **Quality bar.** Prefer, in order: official documentation and guides from the people who build the thing; well-known practitioners and educators (for example Anthropic, OpenAI, Google, Hugging Face, DeepLearning.AI, LangChain, Andrej Karpathy, 3Blue1Brown, Jay Alammar, Lilian Weng, Chip Huyen, Eugene Yan, Hamel Husain, Shreya Shankar, Simon Willison, Sebastian Raschka, Jason Liu, fast.ai, Real Python, freeCodeCamp, MIT/Stanford/CMU course pages, Full Stack Deep Learning); original papers; widely used open-source repos. Avoid content farms, SEO listicles, unknown Medium posts, paywalled newsletters, affiliate links and pages that mostly sell something.
3. **Freshness.** For fast-moving topics (APIs, SDKs, frameworks, MCP, evals tooling, agent patterns) prefer material from 2025 or 2026 and official docs that stay current. For fundamentals (how transformers work, BM25, git, HTTP) older classics are fine.
4. **Free first.** Most resources should be free. Paid ones (books, paid courses) are allowed when clearly the best, and must be marked Paid. Mark courses that are free to audit as "Free to audit".
5. **Mix of types.** Each module needs at least three different types across its resources (for example Docs, Article, Video, Course).
6. **No duplicates on a page.** One URL appears at most once per page. Reusing a famous resource across modules is fine when it is genuinely the best source for both, but prefer fresh picks.
7. **Honest time estimates.** Estimate reading or watching time realistically. A 40-minute video is "40 min". A course is its stated length, or "self-paced". Docs you consult rather than read are "reference".

### Resource line format (the site parses this exactly)

Each resource is one bullet on one line:

```
- [Title](https://example.com/page) · Source · Type · Cost · Time — Why it is worth the reader's time, in one sentence.
```

- `Title`: the resource's real title, tidied (no site name suffix).
- `Source`: author or publisher, short ("Anthropic", "Andrej Karpathy", "DeepLearning.AI", "Hugging Face", "Real Python").
- `Type`: exactly one of `Course`, `Video`, `Article`, `Docs`, `Tutorial`, `Paper`, `Book`, `Repo`, `Tool`.
- `Cost`: exactly one of `Free`, `Free to audit`, `Free tier`, `Paid`.
- `Time`: one of: `25 min`, `1 h`, `1.5 h`, `2–3 h`, `30–45 min` (numbers with `min` or `h`, an en dash for ranges), `self-paced`, or `reference`.
- Separators are ` · ` (space, middle dot U+00B7, space). The note follows ` — ` (space, em dash, space). This is the only place an em dash is allowed.
- The note says what the reader gets from it, specifically. Not "a great resource".

## File formats

All files are Markdown with YAML front matter. Set `checked` to the date you last opened the page's links (YYYY-MM-DD).

### Module page: `content/modules/<module-id>.md`

```
---
title: <module title from curriculum.json>
level: L1
kind: core
hours: 8–10
summary: One sentence, at most 30 words, saying what the learner will be able to do.
checked: 2026-10-16
---

## Why it matters
One or two short paragraphs (80–150 words). The concrete problem this module solves for someone building agents.

## What to learn
6–10 bullets. Each: `- **Concept**: one or two plain sentences explaining it.` This is the mental model; the resources go deeper.

## Resources
### Start here
2–3 resource lines. The minimum path: doing only these plus Practice fits inside the module's hours.
### Go deeper
3–6 resource lines.
### Reference
2–5 resource lines: official docs, specs, papers, repos to keep open while building.

## Practice
3–5 numbered exercises. Concrete and small (30 min to 3 h each). Say what to build or measure and what "done" looks like. Use generic, relatable examples (recipes, support tickets, papers, invoices, a personal notes folder, a public API).

## Checklist
4–7 items, each `- [ ] [Must ship] ...`, `- [ ] [Recommended] ...` or `- [ ] [Stretch] ...`. Must-ship items fit in the module hours. Start each item with a verb.

## You're ready when
3–5 bullets, each a testable statement ("You can explain ...", "Your script ...").
```

Total prose (excluding resource lines) about 450–800 words. Short is fine; padding is not.

### Level page: `content/levels/<L#>.md`

```
---
title: <level title>
summary: One sentence, at most 30 words.
weeks: 3–4
---

## What you'll be able to do
4–6 bullets of outcomes.

## Before you start
One short paragraph: what to know first (link earlier modules as [Title](#module-id)).

## How to work through this level
One or two short paragraphs: suggested order, how to split time between resources, practice and the project, and which optional modules suit whom.

## Milestone
One sentence, then 4–6 gate checks as `- [ ] ...` (no tier tags). Each is a testable outcome that proves the level is done, usually tied to the level project.
```

The site adds the module list and project card automatically. Do not list them yourself.

### Project page: `content/projects/<project-id>.md`

```
---
title: <project title>
level: L1
weeks: 1–1.5
summary: One sentence, at most 30 words.
---

## The brief
Two short paragraphs: what you build and for whom. Generic and realistic.

## What you'll practise
3–6 bullets linking the modules used: `- [Module title](#module-id): what this project exercises.`

## Requirements
5–8 items, all `- [ ] [Must ship] ...`.

## Stretch goals
3–5 items, `- [ ] [Recommended] ...` or `- [ ] [Stretch] ...`.

## Suggested stack
A table: `| Need | Suggested | Alternatives |`. Free or free-tier tools first.

## Build it step by step
5–8 numbered steps, each a bold short title then one to three sentences.

## How to evaluate it
A table: `| Criterion | Good enough | Excellent |` with 4–6 rows, measurable where possible.

## Show your work
3–5 bullets: README contents, a short demo video or GIF, a write-up, what to put on a CV.

## Ideas to make it yours
3–5 bullets with alternative themes or datasets.

## Helpful resources
2–6 resource lines in the standard format: example repos, templates, tutorials closest to this build.
```

## Markdown conventions

- Never use `#` (H1). Use exactly the H2 headings above, in order; H3 only where shown.
- Internal links use the id as an anchor: `[Prompt engineering](#l1-prompt-engineering)`, `[Level 2](#L2)`, `[the capstone](#capstone)`. Only link ids that exist in curriculum.json.
- Fenced code blocks must name a language (`python`, `bash`, `json`, `text`). Keep code short; this is not a code-heavy site.
- Tables are pipe tables with a header row. Nested list items are indented 4 spaces.
- No HTML, no images, no emoji, no mermaid.

## Style

- Plain words. Sentences under about 25 words. Paragraphs of at most 4 sentences. Active voice. Address the reader as "you".
- Lead with the point. No hype, no filler.
- Do not use em dashes in prose (only in resource lines), "not X, but Y" framing, colon-then-reveal sentences, or stock phrases ("it's worth noting", "in today's fast-paced world", "game-changer", "delve", "dive into", "unlock", "landscape").
- Numbers carry units. Label illustrative numbers as examples.
- Name tools neutrally. When several tools do the same job, say so and say how to choose.

## Accuracy

- Do not invent facts, URLs, course lengths, prices, version numbers or API names. If a fact about a tool's current state matters, check it against official documentation or phrase it generically.
- Course lengths and costs come from the course page you fetched.
- Never reproduce copyrighted text. Paraphrase. Quotes under 15 words, at most one per source.

## Before you finish

Run `python check.py --all` and fix every ERROR. Fix warnings where reasonable. Then run `python build.py` and look at your pages in a browser.
