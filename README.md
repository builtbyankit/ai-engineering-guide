# AI Agent Engineering Guide

A free, resource-first study guide that takes you from writing a little code to building, evaluating and running production AI agents.

**Read it here: https://builtbyankit.github.io/ai-agent-engineering-guide/**

## What's inside

- **Seven levels and a capstone**, from Python and APIs to production deployment: Foundations, LLM fundamentals, Retrieval and RAG, Tools and agents, Frameworks and multi-agent systems, Evaluation, observability and safety, and Production and scale.
- **33 modules** (28 core, 5 optional). Each has a plain-language overview, hand-picked resources in three tiers (Start here, Go deeper, Reference), practice exercises, a checklist and a "you're ready when" self-test.
- **About 430 resources**: official docs, blogs, free courses, videos, papers and repos. Every link was opened and checked on 16 October 2026. A searchable resource library lets you filter by type, level and cost.
- **A milestone and a portfolio project per level**, each with requirements, stretch goals, a suggested stack, step-by-step guidance and a rubric, plus a capstone.
- **Progress saved in your browser.** Tick resources, tasks and milestone checks; they are stored in `localStorage` and never leave your device. Back up and restore from the "Your progress" page.

At 10 to 12 hours a week, the core path takes about 32 to 43 weeks.

## Repository layout

| Path | What it is |
| --- | --- |
| `curriculum.json` | Levels, modules, projects, ids and hour estimates |
| `content/levels/` | One page per level, including its milestone checks |
| `content/modules/` | One page per module |
| `content/projects/` | One page per level project, plus `capstone.md` |
| `content/pages/start.md` | The "How to use this guide" page |
| `template.html` | The single-page app shell: styles, navigation, progress and the resource library |
| `build.py` | Renders the content into `site/` |
| `check.py` | Validates page structure, resource-line format, checklists and links |
| `WRITING_GUIDE.md` | The format and style rules every page follows |

## Build it locally

```bash
pip install -r requirements.txt
python check.py --all
python build.py
python -m http.server --directory site 8000
```

Then open http://localhost:8000.

## Deploying

Every push to `main` runs `.github/workflows/deploy.yml`. It checks the content, builds the site and publishes `site/` to the `gh-pages` branch, which GitHub Pages serves.

## Contributing

Broken link, outdated resource or a better pick? Open an issue or a pull request. Edit the Markdown in `content/`, follow `WRITING_GUIDE.md`, and run `python check.py --all` before you push.

Progress ids are tied to the order of checklist items and to resource URLs, so reordering checklist items shifts learners' saved ticks. Add new items at the end of a list where you can.
