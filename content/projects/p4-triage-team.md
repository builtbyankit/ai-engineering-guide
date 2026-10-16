---
title: Support triage with human approval
level: L4
weeks: 2
summary: Build a support triage workflow that classifies tickets, researches a knowledge base, drafts replies and waits for human approval, with persisted state and an audit log.
---

## The brief

A small software company receives a steady stream of support email: password problems, billing questions, bug reports and the occasional angry customer. One person reads every message, searches the help centre, writes a reply and decides whether an engineer needs to see it. You will build the assistant that does the first pass of that work while the person keeps the final say.

Your workflow reads tickets from a sample inbox and classifies each by category and urgency. It searches a small knowledge base and drafts a reply that cites the articles it used. Then it stops. Nothing is sent until a reviewer approves, edits or rejects the draft. Run state lives in a database, so a crash or redeploy never loses a pending approval, and every step lands in an audit log.

## What you'll practise

- [Stateful agents with LangGraph](#l4-langgraph): typed state, conditional routing, checkpoints and resuming a thread after a restart.
- [Agent SDKs compared](#l4-agent-sdks): choosing LangGraph or an SDK for this job and defending the choice in your README.
- [Multi-agent systems](#l4-multi-agent): deciding whether classify, research and draft are steps in one workflow or separate agents, and measuring the cost of each option.
- [Human in the loop](#l4-human-in-the-loop): an approval policy, approve, edit and reject paths, an audit log and timeouts.
- [Building a RAG pipeline](#l2-rag-pipeline): retrieving help articles and citing them in the draft.
- [Structured outputs and function calling basics](#l1-structured-outputs): reliable classification into a fixed schema.

## Requirements

- [ ] [Must ship] Load at least 50 sample tickets from a file or local mailbox, and a knowledge base of at least 15 help articles.
- [ ] [Must ship] Classify each ticket into a fixed set of categories and an urgency level, validated against a schema.
- [ ] [Must ship] Retrieve relevant articles and draft a reply that cites them, or flag the ticket when no article answers it.
- [ ] [Must ship] Pause before any send action and let a reviewer approve, edit or reject the draft, with a reason required for rejections.
- [ ] [Must ship] Persist run state in SQLite or Postgres so pending approvals survive a process restart, and send each approved reply exactly once.
- [ ] [Must ship] Write an append-only audit log of every step, decision, reviewer and timestamp, keyed by ticket and run ID.
- [ ] [Must ship] Build it with LangGraph or one agent SDK, and explain the choice in the README.
- [ ] [Must ship] Report classification accuracy on a hand-labelled test set of at least 20 tickets.

## Stretch goals

- [ ] [Recommended] Auto-approve low-risk categories above a confidence threshold and report how many tickets still reach a person.
- [ ] [Recommended] Build a small review page or chat-tool integration that shows the ticket, sources and draft side by side.
- [ ] [Stretch] Split research and drafting into separate agents and compare quality, latency and tokens with the single workflow.
- [ ] [Stretch] Escalate approvals that nobody answers within a set time to a second reviewer.
- [ ] [Stretch] Feed reviewer edits back in as examples so later drafts need fewer changes.

## Suggested stack

| Need | Suggested | Alternatives |
| --- | --- | --- |
| Orchestration | LangGraph | OpenAI Agents SDK, Pydantic AI, Claude Agent SDK, Microsoft Agent Framework |
| Persistence | SQLite checkpointer (`langgraph-checkpoint-sqlite`) | Postgres checkpointer, or your SDK's own run-state storage in a database |
| Model | Any tool-calling model with structured output on a free tier | A local open model through Ollama for the classifier |
| Knowledge base search | Chroma or SQLite full-text search | pgvector, Qdrant, plain BM25 |
| Sample tickets | A public synthetic support dataset, or 50 tickets you write | Exported emails from a test mailbox |
| Review interface | Command-line prompt | A FastAPI page, Agent Inbox, a chat-tool bot |
| Audit log | JSONL file or a SQLite table | A Postgres table, or traces in a tool such as Langfuse |

## Build it step by step

1. **Collect the data.** Gather at least 50 tickets and 15 short help articles. Hand-label 20 tickets with the category and urgency you expect, and keep them as your test set.
2. **Design the state.** Write the state schema first: ticket, category, urgency, retrieved articles, draft, review decision and status. Sketch the nodes and the conditional edges between them.
3. **Classify reliably.** Build the classify step with a Pydantic schema and a retry on validation errors. Measure accuracy on your 20 labelled tickets before you move on.
4. **Research and draft.** Add retrieval over the knowledge base and a draft step that cites article titles or IDs. If nothing relevant comes back, mark the ticket "needs human answer" instead of guessing.
5. **Add the human gate.** Put an interrupt, or your SDK's approval mechanism, before the send step. Support approve, edit and reject with a reason, and send rejected drafts back for one more attempt.
6. **Make it durable.** Switch to a SQLite or Postgres checkpointer with one thread per ticket. Kill the process while drafts wait for review, restart it, and confirm every pending approval is still there.
7. **Log and send safely.** Write each step and decision to the audit log. Make sending idempotent, for example by naming outbox files after the ticket ID and skipping tickets already marked sent.
8. **Measure and write up.** Run the full set and report accuracy, the share of drafts approved without edits, average tokens per ticket and time to first draft.

## How to evaluate it

The thresholds below are example targets. Adjust them to your data and say so in your README.

| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Classification accuracy | 80% or more on your 20 labelled tickets | 90% or more, with a confusion table and notes on each miss |
| Draft quality | Most drafts cite a relevant article or correctly flag that none fits | Reviewers approve at least half of drafts without edits |
| Durability | Pending approvals survive one restart | Repeated kills at random points cause no lost or duplicate sends |
| Human control | Approve, edit and reject all work from the terminal | A review page shows ticket, sources and draft, with timeouts and escalation |
| Audit trail | Every decision is logged with reviewer and time | You can reconstruct any ticket's full history from the log and checkpoints |
| Cost | Tokens per ticket are reported | Cost per ticket is reported and compared across two designs |

## Show your work

- A README with an architecture sketch, the state schema, your approval policy, and why you chose LangGraph or an SDK.
- A two-minute demo video or GIF where a ticket arrives, the draft pauses, you restart the process, then approve and the reply lands in the outbox.
- A short write-up of your measurements, including one failure you found and how you fixed it.
- A CV line such as "Built a durable support-triage agent with human approval and audit logging; 90% accuracy on a labelled test set." Use your real numbers.

## Ideas to make it yours

- Triage GitHub issues for an open-source project: label them, find related issues and docs, and draft a maintainer reply.
- Process invoices sent to an accounts inbox: classify them, match them against purchase orders, and hold payments for approval.
- Screen messages sent to a club or community group and route each one to the right volunteer with a suggested reply.
- Support two languages: detect the customer's language, retrieve from translated articles and draft in that language.

## Helpful resources

- [langchain-ai/agents-from-scratch](https://github.com/langchain-ai/agents-from-scratch) · LangChain · Repo · Free · self-paced — Builds an email assistant step by step, with notebooks on the agent, evaluation, human-in-the-loop review and memory; the closest template to this project.
- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) · LangChain · Docs · Free · 20 min — Designs a customer support email agent node by node, including a human review interrupt and checkpointing.
- [openai/openai-cs-agents-demo](https://github.com/openai/openai-cs-agents-demo) · OpenAI · Repo · Free · self-paced — A customer service demo on the OpenAI Agents SDK with a triage agent, specialist handoffs, guardrails and a UI that shows the orchestration.
- [Customer support tickets dataset](https://huggingface.co/datasets/Tobi-Bueck/customer-support-tickets) · Tobi-Bueck on Hugging Face · Repo · Free · reference — Tens of thousands of labelled sample tickets with subject, body, agent answer, queue, priority and language, under a non-commercial licence.
- [langgraph-checkpoint-sqlite](https://pypi.org/project/langgraph-checkpoint-sqlite/) · LangChain · Tool · Free · reference — The SQLite checkpointer package, with sync and async savers, for persisting runs to a local file.
