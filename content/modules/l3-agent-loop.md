---
title: The agent loop
level: L3
kind: core
hours: 10
summary: Build an agent from scratch as a model calling tools in a loop, with stop conditions, step and cost budgets, error recovery and judgement about when not to.
checked: 2026-10-16
---

## Why it matters
An agent is a model that calls tools in a loop until it reaches a goal. The loop itself fits in a few dozen lines of code. Building it yourself, before touching any framework, shows you what frameworks hide: how messages pile up, where tokens go and why runs fail.

The loop is also where cost and reliability are decided. Without a step limit, a confused agent can repeat the same search dozens of times. Without a budget, one bad run can cost more than a day of normal use. Without error handling, one timeout ends the run. This module gives you a small, honest agent that stops when it should and tells you why.

## What to learn
- **Model, tools, loop**: An agent sends the conversation and tool definitions to the model, runs any tool calls it returns, appends the results and repeats. It stops when the model answers without calling a tool, or when your code stops it.
- **ReAct**: The ReAct pattern interleaves reasoning ("I need the paper's publication year") with actions and observations. Tool-calling APIs and reasoning models now build this in, and the idea explains why agents can change course mid-task.
- **Owning the loop**: Keep the message list, tool registry and dispatch code in one small module of your own. You will reuse it in the project, and any framework will make more sense afterwards.
- **Stop conditions**: Define success explicitly, as a final answer or a `finish` tool with a structured result. Also stop on max steps, a token or cost budget, a wall-clock timeout or repeated identical calls, and record which condition fired.
- **Budgets**: Read input and output token counts from each response's usage data and convert them to cost. Check the budget before every model call, and warn the model near the limit so it can wrap up with a partial answer.
- **Error recovery**: Retry transient failures such as timeouts and rate limits in code, with backoff. Return other failures to the model as tool errors. Stop after a few consecutive failures instead of looping forever.
- **Planning vs reacting**: A reactive agent decides one step at a time. A planning agent writes a plan first, executes it and re-plans when results surprise it. Plans help on long tasks and make runs easier to inspect.
- **Reflection**: Asking the model to critique its draft or a failed attempt, then try again, often improves results. Reflexion keeps these lessons as text for the next attempt. Reflection costs extra calls, so measure the gain.
- **When an agent is the wrong choice**: If the steps are known in advance, mistakes are expensive or you cannot check the result, use a fixed workflow or a single call. [Workflows and agent design patterns](#l3-workflow-patterns) covers those options.

Here is the whole loop. `call_model` and `run_tools` are thin wrappers you write around one provider SDK.

```python
def run_agent(task, tools, max_steps=10, max_cost=0.50):
    messages = [{"role": "user", "content": task}]
    spent = 0.0
    for step in range(max_steps):
        if spent >= max_cost:
            return None, "stopped: budget"
        reply = call_model(messages, tools)
        spent += reply.cost
        messages.append(reply.message)
        if not reply.tool_calls:
            return reply.text, "done"
        messages.append(run_tools(reply.tool_calls))  # all results, errors included
    return None, "stopped: max steps"
```

## Resources
### Start here
- [How to Build an Agent](https://ampcode.com/how-to-build-an-agent) · Thorsten Ball · Tutorial · Free · 45 min — Builds a working code-editing agent in under 400 lines of Go with three file tools, showing there is no hidden magic in the loop.
- [Introduction to Agents (Unit 1)](https://huggingface.co/learn/agents-course/unit1/introduction) · Hugging Face · Course · Free · 3–4 h — Walks through the thought, action and observation cycle step by step and has you build a dummy agent before using any framework.
- [I think "agent" may finally have a widely enough agreed upon definition to be useful jargon now](https://simonwillison.net/2025/Sep/18/agents) · Simon Willison · Article · Free · 10 min — A short, sharp definition (tools in a loop to achieve a goal) that keeps you from over-engineering what an agent is.
### Go deeper
- [Agents](https://huyenchip.com/2025/01/07/agents.html) · Chip Huyen · Article · Free · 30 min — A thorough tour of tool types, planning, reflection and the ways agents fail, adapted from her AI Engineering book.
- [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) · Lilian Weng · Article · Free · 45 min — The classic overview of planning, memory and tool use, with pointers to the research behind each part.
- [How We Build Effective Agents](https://www.youtube.com/watch?v=D7_ipDqhtwk) · Barry Zhang (Anthropic) · Video · Free · 15 min — A short talk on when agents are worth their cost and on seeing the task from the agent's limited point of view.
- [The Unreasonable Effectiveness of an LLM Agent Loop with Tool Use](https://philz.dev/blog/agent-loop) · philz.dev · Article · Free · 5 min — Shows how far a tiny loop with a single bash tool can go, and where specialised tools still help.
### Reference
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) · Yao et al. · Paper · Free · 1 h — The paper that introduced interleaving reasoning with actions, and the source of the thought-action-observation vocabulary.
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) · Shinn et al. · Paper · Free · 1 h — Shows agents improving across attempts by writing lessons from their failures into memory as text.
- [Running agents](https://openai.github.io/openai-agents-python/running_agents/) · OpenAI · Docs · Free · reference — How a production SDK structures the same loop, including a max_turns limit that raises an error when exceeded.

## Practice
1. **Bare loop.** Write `run_agent()` with one provider SDK and two tools over public APIs, for example a dictionary API and a calculator. Done when it answers a question that needs both tools and prints every step.
2. **Budgets and stop reasons.** Add max steps, a cost cap and a timeout, then give the agent an impossible task, such as finding a recipe that does not exist. Done when it stops cleanly and reports which limit fired and what it spent.
3. **Inject failures.** Make one tool fail at random 30% of the time with a timeout or bad data. Done when transient errors are retried in code, other errors reach the model as tool errors, and no run crashes.
4. **Plan first.** Add an optional step that writes a numbered plan before acting. Run five research-style questions about public papers or Wikipedia topics with and without it. Done when you have a small table comparing steps, cost and your 1–5 quality score.
5. **Agent or not?** Take three tasks: extracting fields from invoices, booking a meeting from an email, and open-ended competitor research. Done when you have written a paragraph per task arguing for a single call, a workflow or an agent.

## Checklist
- [ ] [Must ship] Build an agent loop from scratch with at least two tools and a clear final-answer condition.
- [ ] [Must ship] Enforce max steps and a cost budget, and return a stop reason with every run.
- [ ] [Must ship] Handle tool errors without crashing, retrying transient failures with backoff.
- [ ] [Recommended] Log every step (tool, arguments, tokens, latency) to a JSONL file.
- [ ] [Recommended] Add a planning step and compare it with the reactive version on a few tasks.
- [ ] [Stretch] Add a reflection pass that critiques the final answer, and measure whether it helps.

## You're ready when
- You can write the agent loop from memory and explain each line.
- Your agent always stops, and reports why it stopped and what the run cost.
- A failing tool degrades the answer without crashing the run.
- You can argue, for a given task, whether an agent beats a fixed workflow.
