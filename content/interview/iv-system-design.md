---
title: Agentic system design rounds
hours: 6–8
summary: Answer an agent design question in 45 minutes with a repeatable structure, worked prompts, failure walks, numbers and the trade-offs interviewers probe.
checked: 2026-10-19
---

## What the round tests

A design round asks you to sketch a system, such as "design an agent that resolves support tickets and can issue refunds". The interviewer is not checking whether you know a particular framework. They want to see how you think. Do you clarify the job, start from a simple baseline, keep authority out of the model, plan for failure, measure quality and reason about cost?

There is rarely one right answer. A good answer states its assumptions, picks the simplest design that meets them and says what evidence would change the choice. Drawing well matters less than walking through what happens when things go wrong.

## A 45-minute timeline

| Minutes | Do this |
| --- | --- |
| 0–5 | Clarify users, the job, what counts as success, risk, traffic and latency. Write the assumptions down where the interviewer can see them. |
| 5–10 | Name a baseline (a person, a fixed workflow or one model call) and say where an agent adds value. Draw the autonomy boundary. |
| 10–20 | Draw the runtime: entry point and identity, control loop, model adapter, tool gateway, retrieval, state store, approvals and external systems. |
| 20–30 | Walk one normal run, then two or three failures, such as a tool timeout, an injected instruction and a crash after a write. |
| 30–38 | Add numbers: calls and tokens per task, peak demand against the provider's limits, cost per useful task and the latency budget. |
| 38–45 | Describe evals, rollout and monitoring, name the main trade-off and say what you would build first. |

If the interviewer steers you somewhere else, follow them. The timeline is a default, not a script.

## A six-step answer structure

1. **Clarify the job.** Who asks for what, how often, and what does a good outcome look like? What happens if the system is wrong, too slow or too expensive?
2. **Choose the least complex design.** Start from one model call, a fixed workflow or a single bounded agent. Add orchestration or more agents only for a need you can name.
3. **Draw the runtime and boundaries.** The model proposes. Code enforces identity, permissions, argument checks, budgets and approvals. Mark where untrusted text enters the system.
4. **Trace one run and its failures.** Follow a request end to end, then break it: a malformed tool call, a timeout, stale data, a retry, a refusal, a partial side effect.
5. **Define evidence and operations.** Say how you would build an eval set, which metrics gate a release, what you trace, how you roll out and how you roll back.
6. **Name the trade-offs.** Quality, latency, cost, autonomy, security surface and operational load. Say which one you are giving up and why.

## Worked prompt: support agent that can issue refunds

**Prompt.** Design an assistant that answers customer questions about orders and can issue refunds up to a set amount.

**Clarify.** What share of tickets are order status, policy questions or refund requests? What is the refund limit, and who may approve above it? What response time do users expect? Is the data in one system or several?

**Baseline and boundary.** Order status and policy questions follow known paths, so a fixed workflow handles most of them without a model loop. A bounded agent handles mixed or unclear requests. The model may look up orders and draft a refund proposal. It may never issue a refund itself.

**Runtime.** The user's identity comes from the session, never from the prompt. A tool gateway checks every call against that identity, validates arguments and enforces budgets. A refund proposal goes to a review step. The approval binds to a digest of the exact proposal, and the decision and an outbox row are written in one transaction. A worker sends the refund with a stable idempotency key.

**Failure walks.**

- A user asks about someone else's order. The order service checks ownership and returns the same denial for missing and forbidden orders.
- A help article contains an injected instruction. The model can only call allowed tools with the user's scope, so the worst case is a wrong draft, not a leak.
- The payment call times out after it was sent. Mark it as outcome unknown, query the provider with the same key and only then decide. Never retry with a new key.

**Evidence and rollout.** Keep a labelled set of tickets by intent, including adversarial ones. Release blockers are any cross-customer disclosure, unapproved refund or duplicate refund. Roll out in stages: shadow mode, read-only canary, proposals only, then approved refunds.

**Trade-off.** Human review adds delay and cost, so reserve it for refunds above a threshold or with low-confidence signals, and keep deterministic rules for the rest.

## Worked prompt: knowledge assistant with permissions

**Prompt.** Design an internal assistant that answers questions from company documents and code, for 10,000 employees, where people can only see what they already have access to.

**Clarify.** How many documents, how often they change, and how fast a permission change must take effect. Which sources (wiki, drive, code), and is the answer allowed to quote them?

**Design.** Split it into an ingestion plane and a query plane. Ingestion parses, chunks and embeds documents and stores each chunk with its source, version and access metadata. The query path runs hybrid search and a reranker, then checks the user's current access against the source system before any text reaches the model. The index is derived data and never the authority on who may read what.

**Failure walks.**

- A user loses access after a document was indexed. The query-time check denies it, even though the stale index still holds the chunk.
- A source is deleted. Ingestion removes its chunks and any cached answers that quote them.
- A rebuild goes wrong. Build the new index beside the live one and switch only when checks pass, so rollback is a pointer change.

**Numbers.** Estimate chunks from document count and size, vector storage from chunks, dimensions and bytes, and the time a full re-embedding takes at your embedding quota. [Agent system design and capacity planning](#l6-system-design) has a worked example.

**Evidence.** Measure retrieval and answers separately: recall@k and MRR for retrieval, faithfulness and correct refusals for answers. Include permission-crossing test cases that must always fail.

## Worked prompt: long-running research with specialists

**Prompt.** Design an agent that produces a sourced research report over 10 to 30 minutes, possibly using several specialist agents.

**Clarify.** How many reports a day, the budget per report, which sources are allowed and whether a partial report is useful.

**Design.** Start with one agent that plans, searches, reads and writes, with step, token and time budgets. Move to an orchestrator with parallel workers only if the single agent is too slow or its context overflows. Give each worker a structured task: objective, allowed tools and sources, deadline, budget and output schema. Treat worker output as evidence to check, not as fact.

**Durability.** A run this long must survive restarts. Record each model and tool call as a durable step, and give the run a lease so only one worker owns it. Stream progress to the user and return a job id for the final report.

**Failure walks.** A worker times out, so the orchestrator returns a partial report and marks the gap. Workers contradict each other, so the merge step flags the conflict instead of picking one. Total cost nears the budget, so the agent writes up what it has.

**Trade-off.** Parallel workers cut wall-clock time but raise total tokens, often by several times. Measure quality per dollar against the single-agent baseline before you keep them.

## Follow-ups interviewers use

Expect the interviewer to change an assumption halfway through. Practise answering these:

- Traffic grows tenfold. What breaks first, and is it your system or the provider's limit?
- The provider is down for an hour. What still works?
- The model starts returning malformed tool calls after a version change. How do you notice and respond?
- A customer reports that the agent revealed another customer's data. Walk through the incident.
- The budget halves. Which quality do you give up first?
- Legal says no data may leave the region. What changes?
- Why not just use a bigger context window instead of retrieval?

## Strong and weak signals

| Strong answer | Weak answer |
| --- | --- |
| Starts from the job, the risk and a simpler baseline | Starts by naming a framework or a model |
| Keeps identity and authority in code, outside the model | Treats the system prompt or a vector filter as a security boundary |
| Plans for unknown outcomes and safe retries | Says retries make an action happen exactly once |
| Measures retrieval and answers separately, with refusals | Reports one overall accuracy number from a demo |
| Puts numbers on calls, tokens, quotas and cost | Promises a latency or cost figure without any working |
| Says what is built, what is assumed and what would change the design | Presents every choice as obvious and final |

## Checklist

- [ ] [Must ship] Answer each of the three worked prompts in 45 minutes, out loud, before reading the outline.
- [ ] [Must ship] Draw the runtime for one prompt with trust boundaries and the points where untrusted text enters.
- [ ] [Must ship] Answer three follow-ups that change an assumption, and revise your design for each.
- [ ] [Recommended] Do the numbers for one prompt with formulas and units, then redo them with doubled traffic.
- [ ] [Recommended] Write up one design as a one-page document with assumptions, trade-offs and a first release.
- [ ] [Stretch] Design a fourth system from your own work or a product you use, and have a peer probe it.

## Resources

- [Architecture Decision Cases: Compare Viable Alternatives](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-architecture-decision-cases.md) · Agentic AI Mastery · Article · Free · 30 min — Five design choices argued both ways, with a reference decision, a benchmark that could overturn it and an interview defence checklist.
- [Worked Capacity, Latency, and Cost Design](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-worked-capacity-and-cost.md) · Agentic AI Mastery · Tutorial · Free · 45 min — The numbers behind a knowledge-assistant design, from vector storage and quotas to cost per useful task, ready to adapt for a whiteboard.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) · Anthropic · Article · Free · 30 min — The workflow and agent patterns interviewers expect you to name, with clear advice on when each one earns its cost.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) · Anthropic · Article · Free · 30 min — A detailed production example of an orchestrator with parallel workers, including token cost and evaluation, useful for the research prompt.
- [Building A Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html) · Chip Huyen · Article · Free · 45 min — Where context construction, guardrails, routing, caching and observability sit in a real LLM system, a good checklist for your diagram.
- [The System Design Primer](https://github.com/donnemartin/system-design-primer) · Donne Martin · Repo · Free · reference — General distributed-systems concepts and a step-by-step approach to design questions for the parts of the round that are not specific to AI.
