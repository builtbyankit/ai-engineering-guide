---
title: Staying current and building a portfolio
level: L6
kind: core
hours: 4–6
summary: Build a weekly habit for reading papers and news, publish write-ups and demos of your agents, contribute to open source, and prepare for AI engineering interviews.
checked: 2026-10-16
---

## Why it matters

Agent tooling changes every few months. Frameworks rename themselves, providers ship new caching and batch features, and last year's best practice turns into a footnote. You cannot read everything, so you need a small, steady system for deciding what to read and what to skip.

The other half is being visible. Hiring managers and collaborators judge AI engineers by what they have shipped and explained. A repo with a clear README, a two-minute demo and a post about what broke tells them far more than a list of courses. This module sets up both habits so they outlast this guide.

## What to learn

- **A reading system**: Pick a few sources and a fixed slot, for example 45 minutes twice a week. Skim many titles, read few papers in full, and keep a running notes file of what you tried.
- **Where papers show up**: New work usually lands on arXiv first, in listings such as cs.CL, cs.AI and cs.LG. Hugging Face Daily Papers and Trending Papers filter it by community upvotes and link code repos when they exist, which covers what many people once used Papers with Code for.
- **Reading a paper in passes**: Skim the title, abstract, figures and conclusion first, and stop if the paper is not relevant. Read closely only when it is, and try to reproduce a result only for the few that matter to your work.
- **Reading launch claims critically**: Check what a benchmark measures, who ran it and whether it resembles your task, using [Reading agent benchmarks](#l5-benchmarks). Your own evals on your own data outrank any leaderboard.
- **Writing technical posts**: Write about what you built and what you learned, including failures and numbers. Short "today I learned" notes count. Writing also exposes the gaps in your own understanding.
- **Demo videos**: Keep it to two minutes, one task and real output. Show the problem, the agent working with a trace or progress view, and one failure it handles. A plain screen recording with clear narration is enough.
- **Contributing to open source**: Start with docs fixes, bug reproductions and small "good first issue" tickets in projects you already use, such as agent frameworks, eval tools or MCP servers. Read the CONTRIBUTING file first and keep pull requests small.
- **Interview prep**: AI engineering interviews often include LLM system design. Practise talking through requirements, architecture (retrieval, tools, gateway, caching, guardrails), evals, failure modes, latency and cost for a product such as a support agent, using numbers from your own projects. The optional [AI engineering interviews](#l6-interviews) module adds timed mocks, scoring and coding practice.
- **Portfolio shape**: Two or three deep projects beat ten shallow ones. Give each a README with an architecture diagram, eval results, cost per task and a demo link.

## Resources

### Start here

- [How to Read a Paper](https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf) · S. Keshav · Paper · Free · 20 min — The classic three-pass method for deciding quickly whether a paper deserves ten minutes, an hour or a weekend.
- [Learn In Public](https://www.swyx.io/learn-in-public) · swyx · Article · Free · 10 min — The case for publishing notes, posts and talks while you learn, and how doing so attracts mentors and opportunities.
- [What to blog about](https://simonwillison.net/2022/Nov/6/what-to-blog-about/) · Simon Willison · Article · Free · 5 min — Two easy kinds of post you can start today, covering things you learned and things you built.

### Go deeper

- [Stanford CS230 Lecture 8: Career Advice / Reading Research Papers](https://www.youtube.com/watch?v=733m6qBH-jI) · Andrew Ng · Video · Free · 1 h — How to work through a stack of papers on a new topic, plus practical advice on building a machine learning career.
- [What We've Learned From A Year of Building with LLMs](https://applied-llms.org/) · Applied LLMs · Article · Free · 1.5–2 h — Tactical, operational and strategic lessons from six practitioners, including Eugene Yan, Hamel Husain and Shreya Shankar, and a strong base for system design answers.
- [How to Write Design Docs for Machine Learning Systems](https://eugeneyan.com/writing/ml-design-docs/) · Eugene Yan · Article · Free · 15 min — A template for explaining a system's purpose, method, implementation and rejected alternatives that doubles as a structure for design interviews.
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/) · Open Source Guides · Article · Free · 30 min — Finding and vetting a project, reading its contribution files, opening good issues and pull requests, and handling review.
- [AI Engineering](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) · Chip Huyen · Book · Paid · self-paced — The most complete book on building with foundation models, from evaluation and RAG to inference optimisation and architecture, and a solid interview reference.
- [aie-book](https://github.com/chiphuyen/aie-book) · Chip Huyen · Repo · Free · reference — The book's free companion repo with chapter summaries, study notes, case studies and a curated resource list.

### Reference

- [Daily Papers](https://huggingface.co/papers) · Hugging Face · Tool · Free · reference — New papers ranked by community upvotes by day, week or month, with an optional email digest.
- [Computation and Language (cs.CL)](https://arxiv.org/list/cs.CL/recent) · arXiv · Tool · Free · reference — The raw feed of recent language-model papers; skim the titles weekly and open only what fits your work.
- [Simon Willison's Weblog](https://simonwillison.net/) · Simon Willison · Article · Free · reference — Near-daily, hands-on notes on new models, tools, coding agents and prompt injection from a careful independent tester.
- [Latent Space](https://www.latent.space/) · Latent Space · Article · Free · reference — An AI engineering newsletter and podcast with long interviews of people building agents, models and infrastructure.

## Practice

1. **Set up your feed.** Choose three to five sources from this page, subscribe, and block two 45-minute slots a week. Done when a `reading-notes.md` file has at least five dated entries, each with one line on whether it changes anything you build.
2. **Read one paper in passes.** Pick a recent agent paper from Hugging Face Daily Papers. Do the first pass in 10 minutes and the second in under an hour. Done when you have a 200-word summary covering the claim, the evidence, one weakness and whether you would use the idea.
3. **Publish one post and one demo.** Write about a project from this guide, covering the problem, the design, eval results, cost per task and one thing that broke. Record a two-minute screen demo. Done when both are public and linked from the project README.
4. **Make one open-source contribution.** Find a small issue, docs gap or reproducible bug in an agent, eval or MCP project you have used. Done when you have opened a pull request, or a clear issue with a minimal reproduction.
5. **Practise a system design answer.** Take a prompt such as "design an agent that answers billing questions and can issue refunds up to $50". Talk for 30 minutes through requirements, architecture, evals, safety, latency and cost, then write it up as a one-page design doc. Done when a peer, or you replaying a recording, can follow the main flow without questions.

## Checklist

- [ ] [Must ship] Set a recurring reading slot and log at least five dated entries in a notes file.
- [ ] [Must ship] Publish one technical post about a project from this guide.
- [ ] [Must ship] Record a demo video of two minutes or less and link it from the project README.
- [ ] [Recommended] Open one pull request or detailed issue on an open-source agent project.
- [ ] [Recommended] Write a one-page design doc for an LLM system design question and rehearse it aloud.
- [ ] [Stretch] Reproduce one result from a recent paper and post what you found.

## You're ready when

- You can summarise a new paper's claim, evidence and main weakness in five minutes of talking.
- Your best project has a README with an architecture diagram, eval results, cost per task and a demo link.
- You have at least one public post and one open-source contribution you can point to.
- You can walk through an LLM system design question covering evals, failure modes, latency and cost.
