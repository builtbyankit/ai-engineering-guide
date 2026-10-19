---
title: Coding and debugging rounds
hours: 6–8
summary: Practise the runtime code agent interviews ask for, with a contract-first method, warm-ups, six timed problems, a trace-debugging round and a scoring guide.
checked: 2026-10-19
---

## What these rounds look like

Agent coding rounds rarely ask for a clever algorithm. More often they ask for runtime code: a tool loop with a budget, a retry with backoff, a parser for streamed tool calls, a scheduler for dependent steps or an idempotent write. Some loops replace coding with debugging, where you get a trace or a failing test and must find the first thing that went wrong.

Interviewers watch how you work as much as what you produce. They want to see you state the contract, think about failure cases before you type, test as you go and explain the trade-offs of your shortcut. Code you can't explain counts for little, so practise talking while you write.

## Work contract first

Use the same five steps on every problem. They keep you calm and show the interviewer your reasoning.

1. **Restate the contract.** What goes in, what comes out, and what the function must never do. Ask about anything unclear, such as limits, error types and whether calls can overlap.
2. **List the invariants and edge cases.** Empty input, duplicates, timeouts, partial failure, cancellation and anything that could run twice.
3. **Write two or three failing tests.** Start with the most important invariant, not the happy path alone.
4. **Implement the simplest version that passes.** Name the shortcut you took and what you would change at scale.
5. **Walk a failure out loud.** Pick one test and narrate what happens line by line.

## Warm-ups

Do these in 10 to 15 minutes each until they feel routine. They come up as small parts of larger questions.

- **Retry with backoff.** Retry a function on transient errors with capped exponential backoff and jitter, and stop after a fixed number of attempts. Test it with a fake that fails twice, then succeeds.
- **Reciprocal rank fusion.** Merge two ranked lists of document IDs with a score of 1 / (k + rank) per list.
- **Recall@k and MRR.** Given ranked results and the relevant ID for each query, compute both metrics.
- **Cosine similarity.** Compute it for two vectors, then return the top 3 matches from a small matrix with NumPy.
- **Token budget.** Given chunks with token counts and scores, pick the best set that fits a budget, keeping the order the model will see.

## Six practice problems

Give yourself the time shown, write tests first and stop when time runs out. Then compare with a reference and note what you missed.

### 1. A bounded agent loop (40 minutes)

Write `run_agent(task, tools, max_steps, max_cost)` around a fake model client that returns either tool calls or a final answer. Run tool calls, append results, track cost and stop on a final answer, the step limit or the budget. Return the answer and a stop reason.

**Check:** a run that never finishes stops at the step limit; a run near the budget stops before the next model call; a tool error is returned to the model as a result, not raised. See [The agent loop](#l3-agent-loop).

### 2. Assemble streamed tool calls (30 minutes)

Input is a stream of events: begin(id, name), delta(id, text) and end(id). Calls can interleave. Build complete argument objects keyed by call ID, and return nothing runnable until the stream ends.

**Check:** reject a delta without a begin, a duplicate begin, an event after end, arguments that aren't a JSON object and arguments over a size limit counted in bytes. One bad call fails the whole batch.

### 3. Run dependent steps with a concurrency limit (40 minutes)

Given steps with IDs and dependencies, run each step once all its dependencies have finished, with at most N running at a time and an overall timeout.

**Check:** reject cycles and unknown dependencies before running anything; independent steps overlap; a failed step blocks its descendants but not unrelated steps; a timeout cancels running work and waits for it to clean up.

### 4. Pick evidence under a token budget (30 minutes)

Given scored chunks with source, version and token count, select chunks for a prompt under a budget. Keep at most one version of each source and never split a chunk.

**Check:** the result fits the budget, prefers higher scores, drops older versions of the same source and returns the reason each chunk was dropped.

### 5. An idempotent write with unknown outcomes (40 minutes)

Write `create_refund(order_id, amount, key)` over a fake provider that sometimes times out after it has already applied the request. Store keys and results locally.

**Check:** the same key returns the first result without a second refund; reusing a key with a different amount is rejected; a timeout records the attempt as unknown, and a later call reconciles it with the provider using the same key before doing anything else. See [Tool calling in depth](#l3-tool-calling).

### 6. Resume an interrupted eval run (30 minutes)

An eval script calls a model for each case and writes results as it goes. It crashed halfway. Make it resume without re-running finished cases, and retry failed cases only when asked.

**Check:** a resumed run makes no calls for finished cases; failed attempts and their cost stay in the record; changing the dataset or model invalidates the saved results instead of mixing them.

## The debugging round

You get a trace, logs or a failing test and must find the first failure, not the last symptom. Read the trace in order and say what you expected at each step. These bugs come up often in agent code:

- A tool result was dropped or sent without its call ID, so the API rejected the next turn.
- The conversation history was sent twice, through both a server-side conversation and a local list.
- Reasoning blocks were removed before a tool result was sent back.
- A retry wrapper sat inside another retry wrapper, so one failure caused dozens of calls.
- A tool returned 50,000 tokens of raw HTML and pushed the instructions out of the context.
- The user ID came from the model's arguments instead of the session.
- A write was retried with a new idempotency key after a timeout and ran twice.

Practise on your own agent: break one thing on purpose, have a friend or a script hide which one, then find it from the trace alone. [Evaluation and debugging rounds](#iv-evals) works through five failures step by step.

## How attempts are scored

Most interviewers judge roughly these four things. Score your own attempts against them.

| Dimension | Weak | Strong |
| --- | --- | --- |
| Contract and edge cases | Starts typing straight away | States inputs, outputs and failure cases, and asks about limits |
| Correctness | Happy path only | Handles partial failure, duplicates, timeouts and cancellation |
| Tests | None, or written at the end | A failing test first for the riskiest invariant |
| Communication | Silent, or can't explain a choice | Narrates trade-offs and names what would change at scale |

## Checklist

- [ ] [Must ship] Do all five warm-ups until each takes under 15 minutes.
- [ ] [Must ship] Solve two of the six problems under time, with tests written before the code.
- [ ] [Must ship] Do one debugging round on your own agent with a bug you didn't plant yourself.
- [ ] [Recommended] Solve the remaining four problems and compare each with a reference solution.
- [ ] [Recommended] Record yourself solving one problem and score it on the four dimensions.
- [ ] [Stretch] Solve one problem in a second language your target team uses.

## Resources

- [Coding Interview Practice: Contracts Before Implementations](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-coding-interview-practice.md) · Agentic AI Mastery · Tutorial · Free · 3 h — Six timed runtime exercises with separate prompts, reference solutions and acceptance checks you can run offline.
- [Interview Workbook: Explain, Defend, Build](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-interview-workbook.md) · Agentic AI Mastery · Tutorial · Free · 1 h — Includes a 45-minute coding and debugging mock that extends a support workflow under fixed turn and tool budgets.
- [How to Build an Agent](https://ampcode.com/how-to-build-an-agent) · Thorsten Ball · Tutorial · Free · 45 min — A complete small agent loop with file tools, the best reference for problem 1.
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) · Anthropic · Docs · Free · reference — The exact rules for returning tool results and errors, which many debugging-round bugs break.
- [Idempotent requests](https://docs.stripe.com/api/idempotent_requests) · Stripe · Docs · Free · reference — A well-documented idempotency key design to model problem 5 on.
- [Timeouts, retries, and backoff with jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter) · Marc Brooker, AWS · Article · Free · 25 min — Why naive retries cause outages and how capped backoff with jitter prevents it, the reasoning behind the first warm-up.
