# AI Agent Engineering Guide

A free, resource-first study guide that takes you from writing small programs to building, evaluating and running production AI agents.

**Read it here: https://builtbyankit.github.io/ai-engineering-guide/**

## What's inside

- **Seven levels and a capstone**, from Python and APIs to production deployment: Foundations, LLM fundamentals, Retrieval and RAG, Tools and agents, Frameworks and multi-agent systems, Evaluation, observability and safety, and Production and scale.
- **35 modules** (29 core, 6 optional). Each has a plain-language overview, hand-picked resources in three tiers (Start here, Go deeper, Reference), practice exercises, a checklist and a "you're ready when" self-test.
- **About 475 resources**: official docs, blogs, free courses, videos, papers and repos. Every link was opened and checked on 16 October 2026, and links added later on the date shown in each page's `checked` field. A searchable resource library lets you filter by type, level and cost.
- **Companion exercises** from the [Agentic AI Mastery guide](https://github.com/builtbyankit/agentic-ai-learning-guide): runnable labs for durable runs, approvals, threat models and RAG, plus worked capacity and cost sheets and interview practice, linked from the modules that use them.
- **Agentic AI interview prep**, a separate section outside the levels for the AI-specific interview rounds: system design, a question bank of about 40 questions with model answers, product and customer rounds, evaluation and debugging with worked numbers, coding, enterprise and regulated settings, behavioural stories and five timed mock rounds with scoring.
- **A milestone and a portfolio project per level**, each with requirements, stretch goals, a suggested stack, step-by-step guidance and a rubric, plus a capstone.
- **Progress saved in your browser.** Mark pages complete and tick resources, tasks and milestone checks; they are stored in `localStorage` and never leave your device. Back up and restore from the "Your progress" page.

At 10 to 12 hours a week, the core path takes about 32.5 to 43.5 weeks. Experienced developers can pick the fast track (about 30 to 40 weeks), which skips most of Level 0.

## Repository layout

| Path | What it is |
| --- | --- |
| `curriculum.json` | Levels, modules, projects, ids and hour estimates |
| `content/levels/` | One page per level, including its milestone checks |
| `content/modules/` | One page per module |
| `content/projects/` | One page per level project, plus `capstone.md` |
| `content/interview/` | The Interview prep section, one page per topic |
| `content/pages/start.md` | The "How to use this guide" page |
| `workspace.css` | Responsive workspace design shared by the dashboard, lessons, resources and progress |
| `tests/dashboard.cjs` | Dashboard resume, track selection and completion regression checks |
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

To check the dashboard behavior after building (requires Node.js, no npm dependencies):

```bash
node tests/dashboard.cjs
```

The overview offers a next-step card, selectable learning paths, per-level progress and an expandable timeline. It resumes the last unfinished lesson in the selected path, otherwise picks the first incomplete page. All existing progress keys, resource IDs and page URLs are retained. Theme selection still supports system, light and dark modes.

## Deploying

Every push to `main` runs `.github/workflows/deploy.yml`. It checks the content, builds the site and publishes `site/` to the `gh-pages` branch, which GitHub Pages serves.

## Contributing

Broken link, outdated resource or a better pick? Open an issue or a pull request. Edit the Markdown in `content/`, follow `WRITING_GUIDE.md`, and run `python check.py --all` before you push. Run `python check.py --due` to list time-sensitive claims that are due for a re-check.

Progress ids are tied to the order of checklist items and to resource URLs, so reordering checklist items shifts learners' saved ticks. Add new items at the end of a list where you can.

