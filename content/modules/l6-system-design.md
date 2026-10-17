---
title: Agent system design and capacity planning
level: L6
kind: optional
hours: 8–10
summary: Turn an agent idea into a defensible design with a decision brief, service objectives, capacity, latency and cost numbers, and recorded trade-offs between real alternatives.
checked: 2026-10-17
---

## Why it matters

A working agent is not yet a design another team can build, fund and operate. Before anyone commits, they ask what the agent may and may not do, how many requests it must handle, where it will hit a limit first, what each useful answer costs and what you would change if the numbers came out differently. Senior engineers and architects answer those questions on paper before the code exists.

This module teaches the reasoning behind those answers. You will write a decision brief, turn requirements into service objectives, and work out concurrency, quotas, latency budgets, storage and cost with explicit formulas. You will also record decisions with the alternatives you rejected. The worked examples use invented numbers on purpose. The skill is building the sheet and knowing which assumption dominates, and the same skill carries straight into AI engineering interviews.

## What to learn

- **Decision brief first**: Before drawing boxes, write down the users and their job, the baseline to beat (a person, a fixed workflow or one model call), the autonomy boundary, the systems of record, the cost of each kind of failure and the non-goals. Add a kill criterion, the measured result that would switch the agent off.
- **Objectives from user outcomes**: A service level indicator (SLI) measures something users feel, such as tasks resolved without correction. A service level objective (SLO) sets a target for it over a window. A healthy model endpoint says little about retrieval, authorization or grounding.
- **Planes and ownership**: Split the design into interaction, control (run state, budgets, model adapter, tool broker), data and actions, and evidence (traces, evals, audit). Name the owner of each piece of state; an index is rebuildable, an approval row is an authorization record and a summary is lossy.
- **Little's law and provider limits**: Work in flight equals arrival rate times time in the system. Turn your task mix into model calls and tokens per minute and compare them with your provider's limits. If the quota is the ceiling, more workers will not help; queueing, admission control or a cheaper route will.
- **Latency budgets**: Split a target such as "95% of answers within 10 s" across stages and keep a reserve. Stage percentiles do not add up to the end-to-end percentile, so measure whole requests with spans, and track time to first token separately.
- **Cost per useful task**: Weight token cost by each route's share, add retries and divide by tasks that succeeded. Then double one assumption, such as the share of expensive investigations, to see which number matters most.
- **Storage and rebuild time**: Raw vector storage is chunks times dimensions times bytes, and indexes, replicas and metadata multiply it, so benchmark the overhead. A full re-embedding at your embedding quota sets how fast you can recover from a bad index.
- **Serving memory**: A self-hosted model needs memory for its weights plus a key-value (KV) cache of about 2 × layers × KV heads × head size × tokens × bytes across active requests. Long contexts and big batches can make the cache larger than the weights.
- **Human review capacity**: Reviews per day times minutes each, divided by productive reviewer hours, is a floor on headcount. Never clear a growing queue by approving automatically.
- **Decisions with alternatives**: An architecture decision record (ADR) captures the context, two viable options, the first-release choice, the benchmark that could prove it wrong and the trigger for revisiting it.

## Resources

### Start here

- [Worked Capacity, Latency, and Cost Design](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-worked-capacity-and-cost.md) · Agentic AI Mastery · Tutorial · Free · 45 min — A complete worked example for a 10,000-user knowledge assistant, from chunk and vector storage through quotas, Little's law, latency budgets, cost per useful task and reviewer headcount.
- [Architecture Decision Cases: Compare Viable Alternatives](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-architecture-decision-cases.md) · Agentic AI Mastery · Article · Free · 30 min — Five cases, such as existing database versus dedicated retrieval and managed API versus self-hosting, each with options, a reference decision, a benchmark and a reconsider trigger.
- [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) · Google · Book · Free · 45 min — The SRE book chapter that defines SLIs, SLOs and SLAs and explains how to choose a small set of targets with an error budget.

### Go deeper

- [Module 12: Senior AI Engineer and Architect Practicum](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-module-12-senior-architecture-practicum.md) · Agentic AI Mastery · Tutorial · Free · 1 h — A full design dossier template covering the decision brief, objectives, system planes, contracts, partial failure, cost model, governance and a scored review rubric.
- [Module 8: Production Architecture and Operations Plan](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-module-08-production-architecture-and-operations.md) · Agentic AI Mastery · Article · Free · 45 min — A reference architecture with component ownership, run state machine, release sequence from shadow mode to action pilot, alerts and kill switches.
- [Numerical Workbook: LLMs, Retrieval and Serving](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-numerical-workbook.md) · Agentic AI Mastery · Tutorial · Free · 1 h — Worked calculations for token budgets, attention, similarity, BM25 and rank fusion, ranking metrics, LoRA parameter counts and KV cache memory.
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · Michael Nygard · Article · Free · 10 min — The short post that introduced the ADR format of title, context, decision, status and consequences.
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) · Kwon et al. · Paper · Free · 1 h — Why the KV cache, not the weights, limits how many requests a server can batch, and how vLLM's paged cache reduces that waste.

### Reference

- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits) · Anthropic · Docs · Free · reference — Requests, input tokens and output tokens per minute by tier, including which cached tokens count against the limit.
- [Rate limits](https://developers.openai.com/api/docs/guides/rate-limits) · OpenAI · Docs · Free · reference — Usage tiers, rate-limit headers and the request and token limits to compare with your peak demand.

## Practice

1. **Write a decision brief.** For an agent you built, such as your Level 4 triage workflow, fill in every brief field on one page. Done when a reviewer can name three things the agent must never do and the result that would switch it off.
2. **Build a capacity and cost sheet.** Start from the worked example's inputs or your own traces. Compute work in flight, calls and tokens per minute at peak, monthly cost and cost per useful task, then double your most expensive route and halve the quota. Done when every cell shows its formula and units and you can name the binding constraint each time.
3. **Budget and measure latency.** Split a p95 target for your Level 6 agent across stages, then run 50 traced requests. Done when you can compare budget with measured p95 per stage and explain why the stages do not sum to the end-to-end p95.
4. **Estimate serving memory.** For an open model you might host, estimate weight memory and KV cache memory at your context length with 8 concurrent requests. Done when the arithmetic is written out with units and you can say which term dominates.
5. **Record two decisions.** Write ADRs for two capstone choices, such as your vector store and orchestration runtime. Done when each lists two real alternatives, a first-release choice, a benchmark that could overturn it and a migration trigger.

## Checklist

- [ ] [Must ship] Write a one-page decision brief with a baseline, an autonomy boundary, non-goals and a kill criterion.
- [ ] [Must ship] Build a capacity and cost sheet with formulas, units and the provider limit that binds first.
- [ ] [Must ship] Set a stage-by-stage latency budget and compare it with measured spans.
- [ ] [Recommended] Write two architecture decision records with alternatives and reversal triggers.
- [ ] [Recommended] Estimate weight and KV cache memory for one open model at your context length.
- [ ] [Stretch] Run a 45-minute design review with a peer and score it with the practicum rubric.

## You're ready when

- You can write a decision brief that names the baseline, the boundary and the result that would kill the agent route.
- You can compute peak calls and tokens per minute from a task mix and say whether a quota or your own system limits throughput.
- You can explain why stage p95 values do not sum to the end-to-end p95, and how you would measure the real one.
- You can defend a design choice against a named alternative and say what evidence would change your mind.
