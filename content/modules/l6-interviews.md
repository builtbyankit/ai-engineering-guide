---
title: AI engineering interviews
level: L6
kind: optional
hours: 6–8
summary: Prepare for AI engineering interview loops with a design answer structure, timed mock rounds, contract-first coding practice and honest stories drawn from the projects you built.
checked: 2026-10-17
---

## Why it matters

AI engineering interviews test more than recall. A typical loop mixes an LLM or agent system design round, a coding round, questions on model and retrieval fundamentals, and a behavioural round, often with an incident or evaluation review added for senior roles. Interviewers want to see you start from requirements, choose the simplest design that works, find the failure cases, quantify trade-offs and say what evidence would change your mind.

The projects in this guide give you the material. This module turns it into answers you can deliver under time pressure. You practise a repeatable structure, take timed mocks and score them honestly, and write stories whose numbers trace back to code, traces or eval reports. Formats differ between companies, so ask the recruiter which rounds to expect and weight your practice to match.

## What to learn

- **The loop**: Expect some mix of system design, coding or debugging, fundamentals (tokens, decoding, embeddings, retrieval metrics, serving), an evaluation or incident review and behavioural questions. Senior and architect roles add more on trade-offs, cost and ownership.
- **A design answer structure**: Clarify users, success, risk, traffic, latency and cost. Choose the least complex design that could work and say why. Draw the runtime (identity, model adapter, tool broker, state, retrieval, human review). Trace one normal run and several failures, then close with evaluation, rollout and the main trade-off.
- **Signals interviewers look for**: Strong answers start from requirements, keep authority out of the model, plan for unknown outcomes after timeouts, evaluate retrieval and generation separately and put numbers on cost and latency. Weak answers start by naming a framework, treat a prompt or a vector filter as a security boundary, or promise that retries make an action happen exactly once.
- **Numbers on a whiteboard**: Be ready to estimate tokens and cost per task, calls and tokens per minute against a quota, vector storage and KV cache memory, and recall or MRR from a small example. [Agent system design and capacity planning](#l6-system-design) covers the formulas.
- **Coding rounds**: Many agent coding tasks are runtime problems, such as assembling streamed tool calls, running dependent steps with bounded concurrency, picking evidence under a token budget or making a write idempotent. State the contract and invariants first, write a failing test, then implement.
- **Incident and evaluation reviews**: Walk a failure in order, such as an approved action whose worker timed out after the provider accepted it. Reconcile using the original idempotency key before retrying. When reading eval results, ask for sample sizes, a holdout set and separate retrieval and answer metrics.
- **Stories you can defend**: Prepare two or three stories, such as an architecture change driven by evidence and a failure you designed for. Use situation, task, action and result, then add what you would change now. Separate your own work from the team's, and keep every number traceable.
- **Mock, score, retake**: Time each mock and score it on requirements, mechanism, failure control, numbers, evidence and communication. Retake your weakest dimension with a new scenario instead of rehearsing the same words.
- **Honesty about evidence**: Label what you built and measured, what you designed but did not test and what you assumed. Never claim experience you do not have; a clear "I have not run this in production, here is how I would test it" beats a vague claim.

## Resources

### Start here

- [Agentic AI Interview Preparation](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-interview-preparation.md) · Agentic AI Mastery · Article · Free · 45 min — Thirty-five senior-level questions with model answers on design, tools, durability, RAG, context, evaluation and operations, plus an interviewer scorecard of strong and weak signals.
- [Interview Workbook: Explain, Defend, Build](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-interview-workbook.md) · Agentic AI Mastery · Tutorial · Free · 1 h — Follow-up questions for every answer, four timed mock rounds (design, coding, incident and evaluation review) and a six-dimension scoring scheme.
- [Behavioral interviews for Software Engineers](https://www.techinterviewhandbook.org/behavioral-interview/) · Tech Interview Handbook · Article · Free · 30 min — How to build a small set of STAR stories from your strongest projects and prepare for the questions almost every loop asks.

### Go deeper

- [Coding Interview Practice: Contracts Before Implementations](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-coding-interview-practice.md) · Agentic AI Mastery · Tutorial · Free · 3 h — Six timed runtime exercises with separate prompts, reference solutions and checks, from streamed tool-call assembly to recovering an interrupted eval run.
- [Technical Leadership and Experience Interview Practice](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-leadership-interview-practice.md) · Agentic AI Mastery · Article · Free · 30 min — Ten scenarios such as disagreeing about multi-agent design, leading an incident and explaining uncertainty to executives, with guidance on verifiable narratives.
- [Mastery and Interview Preparation Plan](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-mastery-and-interview-plan.md) · Agentic AI Mastery · Article · Free · 15 min — A six-week path and a fourteen-day sprint, each with weekly deliverables, an evidence pack and completion gates.
- [Introduction to Machine Learning Interviews](https://huyenchip.com/ml-interviews-book/) · Chip Huyen · Book · Free · self-paced — A 2021 book on ML roles, the interview process and over 200 knowledge questions; use it for fundamentals rounds rather than agent design.

### Reference

- [Numerical Workbook: LLMs, Retrieval and Serving](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-numerical-workbook.md) · Agentic AI Mastery · Tutorial · Free · reference — Worked answers for the calculations that come up in fundamentals and design rounds, from token budgets to KV cache memory.
- [The System Design Primer](https://github.com/donnemartin/system-design-primer) · Donne Martin · Repo · Free · reference — General distributed-systems concepts, a step-by-step approach to design questions and practice problems for the parts of a design round that are not specific to AI.

## Practice

1. **Take a diagnostic mock.** Do the 45-minute system design round from the workbook, recording yourself, before you study anything else. Score it on the six dimensions from 0 to 4. Done when you have scores and have named your weakest dimension.
2. **Two-minute answers.** Pick ten questions spread across design, tools, durability, RAG and evaluation. Answer each aloud in two minutes, then answer one follow-up that changes an assumption. Done when each question has a written revision that fixes what the follow-up exposed.
3. **Contract-first coding.** Do two of the coding exercises under time, writing invariants and failing tests before code. Done when your own tests pass and you can name one case your first attempt missed.
4. **Write two stories.** Draw them from projects in this guide or your job, using situation, task, action, result and what you would change. Done when every number in each story links to a commit, trace or eval report, and your personal contribution is stated separately from the team's.
5. **Retake and track.** Run the incident and evaluation review mocks, then a fresh design mock on a new scenario. Done when you have scores for three different mocks and a short note on what improved.

## Checklist

- [ ] [Must ship] Complete one timed system design mock and score it on the six dimensions.
- [ ] [Must ship] Write two-minute answers to ten questions and revise each after a changed-assumption follow-up.
- [ ] [Must ship] Write two project stories whose numbers link to code, traces or eval reports.
- [ ] [Recommended] Solve two runtime coding exercises under time with tests written first.
- [ ] [Recommended] Complete an incident mock and an evaluation review mock.
- [ ] [Stretch] Reach 18 of 24 on three different mocks with no dimension below 2.

## You're ready when

- You can answer an agent system design question with a clear structure, a simpler baseline and named failure modes in 45 minutes.
- You can do the core capacity and cost arithmetic out loud without notes.
- You can walk an unknown-outcome incident from detection to reconciliation without proposing a blind retry.
- You can tell two stories about your own work with numbers you can back up, and say plainly what you have not done.
