---
title: Workflows and agent design patterns
level: L3
kind: core
hours: 8
summary: Choose and build the simplest design that works, from prompt chains and routers to orchestrator-workers, evaluator loops, plan-and-execute and full agents.
checked: 2026-10-16
---

## Why it matters
Many systems people call agents are mostly workflows. Code decides the path, and the model fills in each step. Workflows are cheaper, faster, easier to test and easier to debug than open-ended agents. Knowing the standard patterns lets you pick the least complex design that meets your quality bar, and add autonomy only where it pays for itself.

The patterns also give you a shared vocabulary with other engineers. Anthropic, OpenAI and Google each publish design guides, and they agree on the core advice. Start simple, measure, and add steps or agents only when your evaluations show a real gain.

## What to learn
- **Workflows vs agents**: In a workflow, your code fixes the sequence of model and tool calls. In an agent, the model decides the next step. Many real systems mix the two, such as a fixed pipeline with one agentic step inside it.
- **Prompt chaining**: Split a task into fixed steps, each a model call, with code checks (gates) between them. For example, write an outline, check it, then write the draft. You trade extra latency for higher accuracy at each step.
- **Routing**: Classify the input first, then send it to a specialised prompt, tool set or model. Routing lets a small, cheap model handle easy cases while a stronger model handles hard ones.
- **Parallelization**: Run independent subtasks at the same time (sectioning), or run the same task several times and combine the answers (voting). Use it for speed or for confidence.
- **Orchestrator-workers**: A lead model breaks a task into subtasks it could not predict in advance, hands them to worker calls and merges the results. It suits work such as multi-file code changes or broad research.
- **Evaluator-optimizer**: One call produces a draft, another grades it against clear criteria, and the loop repeats until the draft passes or hits a limit. It only works when you can state what good output looks like.
- **Plan-and-execute**: A planner writes the steps up front, executors carry them out (possibly with cheaper models), and the planner revises when needed. Variants such as ReWOO and LLMCompiler cut model calls or run steps in parallel.
- **Choosing a pattern**: Start with one well-prompted call plus retrieval. Add a pattern when an eval shows a specific failure it fixes, and weigh the extra latency and cost. Google's guide frames the choice around task complexity, latency, cost and the need for human review.
- **Frameworks or plain code**: Each pattern fits in a few dozen lines of plain Python. Graph frameworks such as [LangGraph](#l4-langgraph) add persistence and streaming but can hide prompts, so build the plain version first. Designs with several cooperating agents belong to [Multi-agent systems](#l4-multi-agent).

## Resources
### Start here
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) · Anthropic · Article · Free · 30 min — The reference definitions of the five workflow patterns and of autonomous agents, with clear advice on when each earns its cost.
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) · OpenAI · Article · Free · 1 h — A roughly 30-page guide to deciding whether you need an agent, designing its model, tools and instructions, and growing from one agent to several.
- [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) · Google Cloud · Docs · Free · 45 min — Google's catalogue of single-agent, sequential, parallel, loop, review, coordinator and human-in-the-loop patterns, organised around how to choose.
### Go deeper
- [Plan-and-Execute Agents](https://www.langchain.com/blog/planning-agents) · LangChain · Article · Free · 20 min — Compares plan-and-execute, ReWOO and LLMCompiler and explains where planning ahead saves time and money.
- [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) · DeepLearning.AI · Course · Free tier · 10 h — Andrew Ng builds reflection, tool use, planning and multi-agent patterns from first principles, with a strong module on evals and error analysis.
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) · HumanLayer · Repo · Free · 1 h — Principles such as owning your prompts, context window and control flow, which push you toward workflows with small agentic steps.
### Reference
- [Building Effective Agents Cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/README.md) · Anthropic · Repo · Free · reference — Runnable notebooks implementing the basic workflows, orchestrator-workers and evaluator-optimizer in plain Python.
- [Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) · LangChain · Docs · Free · reference — Each pattern implemented side by side in LangGraph's two APIs, useful for comparing against your plain-code versions.
- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091) · Wang et al. · Paper · Free · 45 min — The research basis for asking a model to plan before solving, which reduced missing-step errors on reasoning benchmarks.

## Practice
1. **Chain with a gate.** Build a three-step chain that turns a messy support ticket into a summary, a category and a draft reply. Add a code check after the first step, for example that the summary is under 60 words. Done when it runs on 20 tickets and you know which step fails most.
2. **Router.** Route questions about a public API's docs into "billing", "technical" and "other", each with its own prompt, using a small model for the routing call. Done when you have measured routing accuracy on 30 labelled questions and reached a target you set, such as 90%.
3. **Evaluator-optimizer.** Have one call write a product description and another grade it against a five-point rubric, looping up to three times. Done when you have compared first and final drafts on ten products and recorded the extra cost.
4. **Same task, three designs.** Answer "compare these three open-source note-taking apps" with a single call, an orchestrator-workers design and a plan-and-execute agent. Done when you have a table of quality (your 1–5 score), latency and cost for each.

## Checklist
- [ ] [Must ship] Implement prompt chaining, routing and evaluator-optimizer in plain code.
- [ ] [Must ship] Write a one-paragraph design note for a real task, naming the simplest pattern that could work and why.
- [ ] [Recommended] Build orchestrator-workers with parallel worker calls.
- [ ] [Recommended] Compare two patterns on the same task by quality, latency and cost.
- [ ] [Stretch] Build a plan-and-execute agent that re-plans when a step fails.

## You're ready when
- You can explain the difference between a workflow and an agent, with an example of each.
- Given a new task, you can name the simplest suitable pattern and justify the choice.
- You can build any of the five workflow patterns from Anthropic's guide without a framework.
- You can show with numbers when a more complex pattern was worth its cost.
