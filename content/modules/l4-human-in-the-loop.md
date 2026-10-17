---
title: Human in the loop
level: L4
kind: core
hours: 6–8
summary: Decide which agent actions need human approval, pause and resume durable runs, let reviewers approve or edit proposals, and keep audit trails and rollback paths.
checked: 2026-10-16
---

## Why it matters

An agent that drafts a refund is useful. An agent that issues the refund on its own, to the wrong customer, is a support incident. Most production agents act in the world: they send email, change records, spend money or run code. For the risky subset of those actions, a person should see the proposal and decide before anything happens.

Doing that well is an engineering problem. The run must stop cleanly, wait minutes or days without holding a process open, and continue exactly where it left off. The reviewer needs enough context to decide quickly and the option to edit the proposal as well as approve or reject it. Every decision needs a record, so you can later answer who approved an action and why.

## What to learn

- **Risk-based approval**: Score each tool by impact and reversibility. Reads run freely, low-impact reversible writes run with logging, and irreversible or costly actions wait for a person.
- **Pause and resume**: The run saves its state at the approval point and exits. A later request carrying the decision resumes it from the saved checkpoint, even after a deploy or restart.
- **Durable execution**: LangGraph, the OpenAI Agents SDK, Pydantic AI, Microsoft Agent Framework and Temporal each offer a way to persist a paused run. Whichever you use, store the state outside the process.
- **Approval UIs**: Show the proposed action, its arguments, the evidence behind it and the expected effect. Put requests where reviewers already work, such as an inbox, a chat tool or a ticket queue.
- **Edit, respond, reject**: Let reviewers change arguments before the action runs, reply with feedback, or reject with a reason. Return the decision to the model as a tool result so it can adjust.
- **Audit trails**: Log every proposal, decision, reviewer, timestamp and final effect in append-only storage. Tie each entry to the run and checkpoint ID so you can replay what happened.
- **Undo and rollback**: Prefer reversible actions such as drafts, soft deletes or sends with a short delay. For multi-step changes, record a compensating action for each step, which is called the saga pattern.
- **Confidence-based escalation**: Send unusual or low-confidence cases to a person and let routine ones through. Use signals you can check, such as classifier scores, rule hits or amount limits, because a model's self-reported confidence is weak on its own.
- **Timeouts and defaults**: Decide what happens when nobody answers. Expire the request, escalate to someone else or take the safe default, and log which one happened.
- **Exact approvals and the outbox**: Bind each approval to a digest of the exact proposal (target, amount, reason, policy version and expiry), so any change makes the approval stale. Write the decision and an outbox row in one database transaction, then let a worker send the action with a stable idempotency key, so a crash can neither lose an approved action nor send it twice.

## Resources

### Start here

- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) · HumanLayer · Repo · Free · 1 h — Principles for production agents; factors 5 to 8 cover unified state, launch-pause-resume, contacting humans through tool calls and owning your control flow.
- [Human-in-the-loop middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) · LangChain · Docs · Free · 20 min — Pauses chosen tool calls and lets a reviewer approve, edit, reject or respond, with a checkpointer holding the state in between.
- [Human-in-the-loop in the Agents SDK](https://openai.github.io/openai-agents-python/human_in_the_loop/) · OpenAI · Docs · Free · 20 min — Marks tools as needing approval, serialises the paused run state to JSON, and resumes it later with the decision.

### Go deeper

- [Our framework for developing safe and trustworthy agents](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents) · Anthropic · Article · Free · 15 min — Explains how to balance agent autonomy with human control, using Claude Code's read-only default and approval prompts as the worked example.
- [Practices for Governing Agentic AI Systems](https://openai.com/index/practices-for-governing-agentic-ai-systems/) · OpenAI · Paper · Free · 1 h — A white paper proposing baseline safety practices for anyone who builds or deploys agents, useful when you justify which actions need sign-off.
- [Project: Ambient Agents with LangGraph](https://academy.langchain.com/courses/ambient-agents) · LangChain Academy · Course · Free · 2.5 h — Builds an email assistant that works in the background, with dedicated modules on evaluation, human review and memory.
- [Human-in-the-loop AI agent](https://docs.temporal.io/ai/cookbook/human-in-the-loop-python) · Temporal · Tutorial · Free · 30 min — A framework-neutral recipe where a durable workflow waits for an approval signal and cancels the action if the timeout expires.
- [Saga pattern](https://docs.temporal.io/design-patterns/saga-pattern) · Temporal · Docs · Free · 15 min — Shows how to undo a multi-step process by pairing each step with a compensating action that reverses it.
- [Use time-travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel) · LangChain · Docs · Free · 20 min — Replays a run from an earlier checkpoint or forks it with edited state, which helps with audits and recovery from a bad decision.

### Reference

- [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input) · Anthropic · Docs · Free · reference — The `canUseTool` callback for approving, editing or denying tool calls, and how to defer a decision so the process can exit.
- [Deferred tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/) · Pydantic · Docs · Free · reference — Tool approval and externally executed tools in Pydantic AI, with runs that resume once results arrive.
- [Human-in-the-loop in workflows](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) · Microsoft · Docs · Free · reference — Request and response ports in Microsoft Agent Framework, including how pending requests survive in checkpoints.
- [langchain-ai/agent-inbox](https://github.com/langchain-ai/agent-inbox) · LangChain · Repo · Free · reference — An open-source inbox UI for LangGraph interrupts, with accept, edit, respond and ignore actions.
- [Pattern: Transactional outbox](https://microservices.io/patterns/data/transactional-outbox) · Chris Richardson · Article · Free · reference — The standard description of saving outgoing messages in the same transaction as the business change, including why consumers must handle duplicates.

## Practice

1. **Risk-rank your tools (30 min).** List every tool from an agent you built earlier, such as your [Personal research agent](#p3-research-agent). Score each for impact and reversibility and assign "run", "run and log" or "ask first". Done when every tool has a policy and a one-line reason.
2. **Approval that survives a restart (1.5 h).** Add an approval step to a tool that sends an email by writing it to a local outbox folder. Pause the run, stop the process, start it again and approve. Done when the email lands in the outbox exactly once.
3. **Edit and reject paths (1 h).** Extend exercise 2 so a reviewer can edit the subject and body, or reject with a reason. Done when the agent uses the rejection reason in its next draft.
4. **Audit log (1 h).** Append every proposal and decision to a JSONL file with run ID, reviewer, timestamp and final arguments. Done when one command answers who approved the last email and what they changed.
5. **Escalate by confidence (1 h).** Add a classifier step that labels each request and returns a score. Auto-approve high-scoring routine cases, send the rest to review, and add a timeout. Done when, on 20 test requests, you can report the review rate and every request you labelled risky went to a person.

## Checklist

- [ ] [Must ship] Write an approval policy that assigns every tool to run, log or ask.
- [ ] [Must ship] Pause a run for approval and resume it after a process restart.
- [ ] [Must ship] Support approve, edit and reject, and return the decision to the agent.
- [ ] [Must ship] Log every proposal and decision with who, when and what changed.
- [ ] [Recommended] Add a timeout with a safe default for unanswered requests.
- [ ] [Stretch] Route cases to review with a measurable confidence signal and report the review rate.

## You're ready when

- You can justify, for any tool, whether it needs approval, using impact and reversibility.
- Your agent pauses, survives a restart, and resumes with the reviewer's decision without repeating side effects.
- Your audit log answers who approved what, when, and with which edits.
- You can describe how you would undo a wrong action that has already run.
