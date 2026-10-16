---
title: Capstone: ship a production agent
level: capstone
weeks: 3–4
summary: Design, build, evaluate, secure and deploy a new agent end to end, then present it as portfolio work a reviewer or hiring manager can judge.
---

## The brief

You build one new system from an empty repository and run it on the internet, where its first users can be you and two friends. It answers from your own data and acts through tools on your own MCP (Model Context Protocol) server. It pauses for a human before anything risky and proves its quality with numbers. Pick one of these three briefs, or propose your own of similar size.

- **Meeting-notes agent.** For a small team, it reads meeting transcripts and extracts decisions and action items with owners and dates. It searches past meetings to answer questions such as when a decision was made. It drafts follow-up emails and tickets, and a person approves each one before it is sent.
- **Docs and codebase assistant.** For contributors to an open-source project, it answers questions about the code and docs with citations to files and pages. When an answer exposes a gap in the docs, it drafts a fix and opens a draft pull request once you approve the diff. The optional [Coding agents](#l4-coding-agents) module helps with this one.
- **Small-business operations agent.** For a small shop, it reads supplier invoices, matches them to purchase orders and stock levels, and flags mismatches. It answers questions from the shop's own records and policies. It proposes payments, reorders and supplier emails, and a person approves anything that moves money or stock.

Whichever brief you pick, these constraints apply.

- Use public, synthetic or your own data. Never load other people's private records.
- Send every side effect to a sandbox, such as a test inbox, a repository you own or a payment provider's test mode.
- Support at least two user accounts, so data separation and per-user budgets are real.
- Set a spending cap before you start (for example $20 of model and hosting costs for the whole project) and enforce it in code.
- Start a new repository. Copying small helpers from earlier projects is fine.

## What you'll practise

- [Python for AI engineering](#l0-python-for-ai), [Calling LLM APIs](#l1-llm-apis), [Prompt engineering](#l1-prompt-engineering) and [Structured outputs and function calling basics](#l1-structured-outputs): a typed, tested codebase with versioned prompts, validated outputs and a model choice you can defend on cost and latency.
- [Building a RAG pipeline](#l2-rag-pipeline), [Better retrieval: hybrid search and reranking](#l2-advanced-retrieval) and [Evaluating RAG](#l2-rag-evaluation): grounded answers with citations, and retrieval quality measured separately from answer quality.
- [Tool calling in depth](#l3-tool-calling), [The agent loop](#l3-agent-loop), [Workflows and agent design patterns](#l3-workflow-patterns), [Model Context Protocol (MCP)](#l3-mcp) and [Memory and context engineering](#l3-memory-context): well-designed tools behind your own MCP server, a bounded loop, the simplest pattern that works and a managed context window.
- [Stateful agents with LangGraph](#l4-langgraph) or [Agent SDKs compared](#l4-agent-sdks), plus [Multi-agent systems](#l4-multi-agent) and [Human in the loop](#l4-human-in-the-loop): durable runs that pause for approval and resume, and a reasoned choice between one agent and several.
- [Evals in depth](#l5-evals-in-depth), [Observability and tracing](#l5-observability) and [Security and guardrails](#l5-security): regression evals in CI (continuous integration, automated checks on every push), a trace for every run and an attack suite aimed at your own system.
- [Web APIs, HTTP and JSON](#l0-apis-and-http), [Git, the command line and Docker](#l0-dev-tooling), [Deploying agent applications](#l6-deployment) and [Reliability, latency and cost](#l6-reliability-cost): a containerised API behind CI/CD, with timeouts, fallbacks and per-user budgets.

## Requirements

- [ ] [Must ship] Answer questions from your corpus with hybrid search (keyword plus vector) and a reranker. Cite the source of each claim, and refuse when the retrieved context lacks the answer.
- [ ] [Must ship] Define at least four tools with clear names, typed schemas and validated outputs. Serve every side-effecting tool from an MCP server you wrote, and connect your agent to it as an MCP client.
- [ ] [Must ship] Run the agent in a bounded loop with a step limit, a per-run token and cost budget, and tool errors returned to the model. Trim or summarise context so long runs stay inside the window.
- [ ] [Must ship] Pause for human approval before every side-effecting action, showing the proposed action, the reason and the sources. Support approve, edit and reject, resume runs after a server restart, and log every decision.
- [ ] [Must ship] Build an eval set of at least 50 cases (an example floor; size it to your spec) covering retrieval, tool choice and final output. Check any LLM judge against your own labels, and run the suite in CI so a regression blocks the merge.
- [ ] [Must ship] Trace every run with spans for model calls, retrieval and tool calls. Show tokens, cost and latency per task on a dashboard.
- [ ] [Must ship] Write a threat model that checks your design against the lethal trifecta (private data, untrusted content and a way to send data out). Give each tool least privilege. Run an attack suite of at least 20 cases (example floor), including indirect injection through retrieved documents, and record the results.
- [ ] [Must ship] Deploy a container to a public HTTPS URL, with secrets kept outside the repository and CI/CD that runs tests and evals. Add timeouts, retries, a fallback model and a per-user spending cap.

## Stretch goals

- [ ] [Recommended] Ship a prompt or model change as a canary to a slice of traffic, and compare quality, cost and latency from traces before full rollout.
- [ ] [Recommended] Collect feedback signals, such as thumbs up or down and how often reviewers edit proposed actions. Turn the worst cases into new eval cases each week.
- [ ] [Stretch] Connect a second MCP client, such as Claude Desktop or an IDE, to your server, and document what changes for remote access and authorization.
- [ ] [Stretch] Build a multi-agent or orchestrator-worker version, and keep it only if your evals show better quality per dollar than the single agent.
- [ ] [Stretch] Route one narrow sub-task to a smaller or fine-tuned open model from [Open models, fine-tuning and serving](#l6-open-models), and report the cost and quality trade-off.

## Suggested stack

Pick tools you already used in earlier levels. A familiar stack beats a new one learned under deadline. Postgres can hold vectors, keyword search, run checkpoints and the audit log, so one database is often enough.

| Need | Suggested | Alternatives |
| --- | --- | --- |
| Service and tests | Python, FastAPI, Pydantic, pytest | TypeScript with an equivalent stack |
| Model access | A hosted model through its official SDK, behind LiteLLM for fallbacks | Direct SDK calls only; Ollama for cheap local development |
| Agent orchestration | LangGraph, for checkpoints and interrupts | OpenAI Agents SDK, Claude Agent SDK, Pydantic AI, or a plain loop with a job queue |
| Retrieval | Postgres with pgvector and full-text search, plus an open cross-encoder reranker | Qdrant or Chroma; a hosted reranker such as Cohere Rerank |
| MCP server | Official MCP Python SDK | FastMCP; the official TypeScript SDK |
| Durable runs and approvals | LangGraph checkpointer on Postgres, with a small web page or chat buttons for approve, edit and reject | Temporal or Inngest for durable execution |
| Evals | pytest harness plus promptfoo or Inspect AI | DeepEval, Braintrust, LangSmith datasets |
| Tracing | Langfuse (open source, self-hostable) | Arize Phoenix, LangSmith, OpenLLMetry |
| Security testing | promptfoo red teaming, garak | PyRIT; a guard model such as Llama Guard |
| Deployment and CI | Docker, GitHub Actions and a managed container service such as Google Cloud Run or Render | Fly.io, Railway, Kubernetes |

## Build it step by step

1. **Write the spec and threat model first.** Fill a one-page design doc with users, jobs, the actions the agent may take, target metrics and a cost cap. Mark each tool as read-only or side-effecting, and note where untrusted text enters the system.
2. **Collect data and seed the eval set.** Gather the corpus and 20 to 30 realistic tasks before you write agent code. Label the expected outcome for each, including cases the agent should refuse or escalate.
3. **Build a thin end-to-end slice.** One request enters through the API, the model calls one read-only tool, and an answer comes back with a trace. Deploy this slice in week 1 so hosting problems appear early.
4. **Add retrieval and measure it alone.** Index the corpus with hybrid search and a reranker. Report recall@k (how often the right chunk is in the top k) before the agent uses retrieval as a tool.
5. **Move actions into your MCP server.** Implement the side-effecting tools with narrow inputs and idempotency keys, so a retried call never sends twice. Connect the agent as a client and add step, token and cost limits to the loop.
6. **Add durable approval.** Pause the run on every risky tool call and store its state in a checkpointer. Build a minimal approval screen, then test that a paused run resumes after you restart the server.
7. **Wire evals, tracing and attacks into CI.** Grow the eval set past 50 cases using failures you find in traces, and fail the build on regressions. Run the attack suite in the same pipeline, then fix what breaks with tighter tool permissions and approval rules.
8. **Operate it for a week and write it up.** Use it daily, review traces, and track cost per task and p95 latency (the time 95% of requests finish within). Turn each new failure into an eval case, then produce the items in "Show your work".

## How to evaluate it

Use this table as a rubric. A reviewer should be able to check every cell from the README, the eval report, the traces and 10 minutes with the live system. Thresholds are example targets, so state your own in the spec and justify them.

| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Task success | Meets the spec's target on a held-out set of at least 50 cases, with the case count stated | Also meets it on repeated runs (for example all 3 of 3 attempts pass), with failures grouped by cause |
| Grounding and retrieval | Answers cite sources, and most "not in the corpus" cases are refused | Recall@5 and faithfulness reported separately, for example 90% or more of claims supported by the cited source |
| Action safety | Every side-effecting tool needs approval, and the audit log shows who approved what | Zero unapproved side effects across the full attack suite, and the threat model maps each risk to a control |
| Engineering quality | Tests and evals run in CI on every pull request, and one command starts the system locally | An eval regression has visibly blocked a merge, and prompt and model versions are pinned with a changelog |
| Operations | Every run is traced, and cost per task and p95 latency are known | A dashboard shows cost, latency and quality over time, and budget caps, fallbacks and timeouts are all tested |
| Communication | The README explains what it does, how to run it and how it is built | A stranger can follow the README, demo and write-up and explain your main trade-offs back to you |

## Show your work

- **README**: the problem and who it is for, a 30-second GIF, a quick start, architecture, dated eval results, costs and known limits. Write it for a hiring manager who will spend 3 minutes on it.
- **Architecture diagram**: one screen showing the user, API, agent loop, MCP server, retrieval store, approval step, tracing and hosting, with trust boundaries marked. Draw it as a text diagram in the README or as an image from any drawing tool.
- **Demo video**: 3 to 5 minutes showing a real task, a reviewer editing a proposed action, a blocked injection attempt and the matching trace. Record real, unedited runs so viewers can trust what they see.
- **Eval report**: how you built the dataset, metrics with sample sizes, judge agreement with your labels and attack suite results. End with the three biggest failure types and what you changed.
- **Blog post**: 1,000 to 2,000 words on what you built, what surprised you and what you would do differently, following [Staying current and building a portfolio](#l6-staying-current). Add one CV line with an outcome and a number, for example "Meeting agent: 87% task success on 60 cases at $0.04 per task".

## Ideas to make it yours

- A research-group assistant that answers questions over a shared paper library and drafts reading-list emails for approval.
- A household admin agent that reads bills and warranties, tracks renewal dates and drafts cancellation or renewal emails.
- An issue triage helper for a repository you maintain that finds duplicates, suggests labels and drafts replies.
- A meal-planning agent that plans a week from your pantry, builds a shopping list and asks before placing any order.
- A club or society assistant that answers member questions from past minutes and drafts announcements for the committee to approve.

## Helpful resources

- [Agents from scratch](https://github.com/langchain-ai/agents-from-scratch) · LangChain · Repo · Free · self-paced — Builds an email assistant in stages with triage, human review of tool calls, memory and pytest-based evals, close to the meeting-notes brief.
- [Claude Quickstarts](https://github.com/anthropics/claude-quickstarts) · Anthropic · Repo · Free · reference — Small reference apps, including a customer support agent over a knowledge base and a TypeScript MCP server, to compare against your own structure.
- [Building a Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html) · Chip Huyen · Article · Free · 30 min — Walks through context construction, guardrails, routing, gateways, caching, write actions and observability, which makes a good checklist for your architecture diagram.
- [What We've Learned From a Year of Building with LLMs](https://applied-llms.org/) · Eugene Yan et al. · Article · Free · 1 h — Six practitioners share tactical, operational and strategic lessons on evals, retrieval, human-in-the-loop design and model versioning to test your design choices against.
- [How to Write Design Docs for Machine Learning Systems](https://eugeneyan.com/writing/ml-design-docs/) · Eugene Yan · Article · Free · 15 min — A section-by-section template covering motivation, success criteria, methodology, implementation and rejected alternatives that fits your spec and README.
- [What to blog about](https://simonwillison.net/2022/Nov/6/what-to-blog-about/) · Simon Willison · Article · Free · 5 min — Makes the case that writing up a project is part of finishing it, with practical advice on short posts and animated GIFs.
