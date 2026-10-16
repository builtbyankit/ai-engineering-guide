---
title: Agent SDKs compared
level: L4
kind: core
hours: 8
summary: Compare the main agent SDKs by what they abstract, build the same small agent in two of them, and choose one for a project with evidence.
checked: 2026-10-16
---

## Why it matters

Every major model provider and several open-source teams now ship an agent SDK. They all wrap the loop you built in [The agent loop](#l3-agent-loop): call the model, run tools, repeat. They differ in what they add on top, such as handoffs, guardrails, sessions, tracing or graph workflows. They also differ in how closely they tie you to one model vendor.

Picking one by popularity or by the latest launch post often ends in a rewrite. This module gives you a short list of questions to ask of any SDK. It also gives you a hands-on way to answer them by building the same agent twice. That skill outlasts any single framework, which matters because these SDKs change quickly.

## What to learn

- **What every SDK abstracts**: The tool-calling loop, tool schemas generated from typed functions, conversation history and run limits. Most also add tracing and structured output.
- **OpenAI Agents SDK**: A lightweight SDK built around agents, tools, handoffs, guardrails, sessions, human approval and built-in tracing. Agents can also be exposed as tools to a manager agent.
- **Claude Agent SDK**: Claude Code's harness as a Python or TypeScript library. It includes file, shell and web tools, hooks, subagents, MCP, permissions and sessions, and suits agents that work on files.
- **Google Agent Development Kit (ADK)**: An open-source kit for Python, TypeScript, Go, Java and Kotlin. It adds multi-agent orchestration, graph workflows, built-in evaluation and a local web UI for debugging.
- **Pydantic AI**: A typed, model-agnostic Python framework from the Pydantic team. Swapping providers is a one-string change, and durable execution runs on engines such as Temporal and DBOS.
- **CrewAI**: Models work as crews of role-playing agents that complete tasks, plus Flows for stateful, event-driven workflows. It is quick for prototyping role-based multi-agent setups.
- **Microsoft Agent Framework**: The successor to AutoGen and Semantic Kernel, for .NET, Python and Go, with agents plus graph-based workflows. AutoGen is in maintenance mode, so do not start new projects on it.
- **How to compare**: Ask each SDK the same questions. How locked in to one model vendor are you? How does state persist? How does human approval work? What tracing do you get? How much of the final prompt can you see and change?
- **Same agent, two SDKs**: The most honest comparison is to build one small agent twice. Then compare the code, the traces and the behaviour when a tool fails.

## Resources

### Start here

- [Open-Source AI Agent Frameworks: Which One Is Right for You?](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) · Langfuse · Article · Free · 30 min — Short profiles of 13 frameworks, including every SDK in this module; written by an observability vendor, so treat its verdicts as a starting point.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) · OpenAI · Docs · Free · 1 h — Official docs for agents, tools, handoffs, guardrails, sessions and tracing, with a small set of primitives that is easy to read end to end.
- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) · Anthropic · Docs · Free · 45 min — Shows how Claude Code's tools, agent loop and context management become a library, and compares it with calling the API directly.

### Go deeper

- [Building agents with the Claude Agent SDK](https://claude.com/resources/articles/building-agents-with-the-claude-agent-sdk) · Anthropic · Article · Free · 20 min — Frames agent design as gather context, take action, verify work, and shows where subagents, compaction and code generation fit.
- [Agent Development Kit](https://adk.dev/) · Google · Docs · Free · 1 h — Google's documentation for building, evaluating and deploying agents, including graph workflows and multi-agent orchestration in ADK 2.0.
- [Pydantic AI](https://pydantic.dev/docs/ai/overview/) · Pydantic · Docs · Free · 45 min — A typed agent framework with dependency injection, structured outputs, tool approval and durable execution on engines such as Temporal.
- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview) · Microsoft · Docs · Free · 30 min — Explains how the framework merges AutoGen's agent abstractions with Semantic Kernel's enterprise features, and when to use an agent versus a workflow.
- [CrewAI documentation](https://docs.crewai.com/) · CrewAI · Docs · Free · 45 min — Covers agents, tasks, crews and Flows; skim it to see the role-based style of multi-agent design.

### Reference

- [openai/openai-agents-python](https://github.com/openai/openai-agents-python) · OpenAI · Repo · Free · reference — Source and runnable examples for agents as tools, handoffs, guardrails, sessions, human approval and tracing.
- [google/adk-python](https://github.com/google/adk-python) · Google · Repo · Free · reference — The ADK source, with the graph workflow runtime, the task API for agent delegation, and the `adk web` debugging UI.
- [microsoft/autogen](https://github.com/microsoft/autogen) · Microsoft · Repo · Free · reference — Now in maintenance mode; useful for reading older tutorials, and it points new users to Microsoft Agent Framework.

## Practice

1. **Build a comparison sheet (45 min).** Make a table with one row per SDK in this module. Add columns for languages, model lock-in, persistence, human approval, tracing and multi-agent support. Done when every cell has a value or "unclear" with a link to the page you checked.
2. **Build a recipe helper twice (2–3 h).** Pick two SDKs. In each, build an agent that takes a list of ingredients and calls one tool to search a local JSON file of recipes. It returns three suggestions as a typed object. Done when both pass the same five test inputs.
3. **Break them the same way (1 h).** Make the tool time out, return bad JSON and return nothing. Then send a request that needs two tool calls. Done when you have a small table showing what each SDK did, what code you had to add, and what its trace showed.
4. **Add an approval gate (1 h).** In one SDK, add a "save to shopping list" tool that needs approval, and approve or reject it from the terminal. Done when a rejected call never writes to the list.
5. **Write the decision (30 min).** In under 300 words, say which SDK you would choose for a support-ticket assistant and why, citing your table and failure tests. Done when a reader could disagree with a specific point.

## Checklist

- [ ] [Must ship] Fill in a comparison table for at least five SDKs from their official docs.
- [ ] [Must ship] Build the same small agent in two SDKs with the same tool and test inputs.
- [ ] [Must ship] Record how each SDK behaves when a tool fails.
- [ ] [Recommended] Add a human approval step to one tool in one SDK.
- [ ] [Recommended] Compare the traces each SDK produces for the same request.
- [ ] [Stretch] Port your [Personal research agent](#p3-research-agent) to the SDK you prefer and note what got simpler.

## You're ready when

- You can explain what each SDK in this module adds on top of a plain tool-calling loop.
- You can say why AutoGen is a poor starting point for a new project and what replaced it.
- Your two implementations pass the same tests, and you can point to the code that differs in effort.
- You can defend an SDK choice for a given project with at least three concrete criteria.
