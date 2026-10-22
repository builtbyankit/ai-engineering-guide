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
| `learning.js` | Assessment, lesson briefs, project showcase, mastery stages and bookmarks; inlined by the build |
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
node tests/learning.cjs
```

The overview offers a next-step card, selectable learning paths, per-level progress and an expandable timeline. It resumes the last unfinished lesson in the selected path, otherwise picks the first incomplete page. All existing progress keys, resource IDs and page URLs are retained. Theme selection still supports system, light and dark modes.

## Deploying

Every push to `main` runs `.github/workflows/deploy.yml`. It checks the content, builds the site and publishes `site/` to the `gh-pages` branch, which GitHub Pages serves.

## Contributing

Broken link, outdated resource or a better pick? Open an issue or a pull request. Edit the Markdown in `content/`, follow `WRITING_GUIDE.md`, and run `python check.py --all` before you push. Run `python check.py --due` to list time-sensitive claims that are due for a re-check.

Progress ids are tied to the order of checklist items and to resource URLs, so reordering checklist items shifts learners' saved ticks. Add new items at the end of a list where you can.


## Learning experience

- **Find your starting point:** six experience self-checks recommend the earliest level with a skills gap. Choosing a start never completes earlier lessons or changes saved ticks.
- **Lesson at a glance:** prerequisites, effort, readiness outcomes and a practical task come from the curriculum and existing Markdown. Projects also preview their deliverables.
- **Learning stages:** Read, Practiced and Completed are independent self-reported states. Only Completed counts toward the existing page totals. Old completed pages do not acquire invented reading or practice history.
- **Resource priorities:** lesson cards show Essential, Optional deep dive, Reference or companion status. The lesson focus control hides nonessential resources without hiding practice or requirements. The library labels resources essential in at least one module and retains its essential-only filter.
- **Project showcase:** browse all seven level projects and the capstone, with expected outputs and requirement previews. The full project page contains the full rubric.
- **Saved for later:** bookmark pages and resources for revision. Saved items and learning stages are included in version 2 progress backups. Version 1 backups still restore; older versions of the app ignore new keys.
- **Accessibility:** larger text and targets, explicit mobile menu close control, focus containment, inert background content, pressed-state buttons and live status messages.

### Browser smoke check before publishing

Serve `site/` over HTTP after rebuilding. Check desktop and 390px mobile widths, both themes and keyboard-only navigation:

1. Submit the assessment with beginner, backend and agent experience; verify the suggested level and that choosing it preserves completion counts.
2. Open a module. Verify its brief and resource priority labels. Toggle essential focus; practice and requirements must remain visible.
3. Toggle Read, Practiced and Completed independently. Reload and confirm all three persist. Check the stage totals on Your progress.
4. Save a lesson and resource, open Saved for later, follow both links and remove each bookmark.
5. Export a progress backup, restore it using merge and replace, and confirm stages/bookmarks survive. Use disposable browser data for reset testing.
6. Open the project showcase and inspect all eight project links and requirement previews.
7. On mobile, open navigation, cycle Tab/Shift+Tab, and close with Escape or the close button. Background content must stay inert only while the drawer is open. Resize to desktop and verify scrolling is restored.
8. Search lessons and resources, switch tracks, navigate previous/next lessons, and check for console errors or horizontal overflow.

The build, generated-data checks and Node regression tests can run in a restricted environment. They do not replace browser visual or interaction testing.
