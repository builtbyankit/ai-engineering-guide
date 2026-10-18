---
title: Multi-agent systems
level: L4
kind: core
hours: 8
summary: Choose between single-agent and multi-agent designs, apply supervisor, handoff and parallel patterns, control their token cost, and connect agents across vendors with A2A.
checked: 2026-10-16
---

## Why it matters

Once one agent has twenty tools and a long prompt, it starts picking the wrong tool and losing track of the task. Splitting the work across several agents looks like the obvious fix. Sometimes it works. Anthropic's research feature runs parallel subagents and beat a single agent by a wide margin on its internal research evaluation.

It also used far more tokens, and other teams found that agents working on separate pieces made conflicting assumptions. This module teaches the main multi-agent patterns and the evidence on when they pay off. You will learn to start with one agent and measure where it fails. Then you add agents only where context limits or parallel work justify the extra cost.

## What to learn

- **Single agent first**: One agent with good tools is easier to build, debug and evaluate. Move to several agents when context overflows, domains are clearly separate, or work can run in parallel.
- **Supervisor or orchestrator-worker**: A lead agent plans, calls worker agents as tools, and combines their results. Workers start with a clean context and return only a summary.
- **Handoffs**: Control passes from one agent to another, and the new agent talks to the user directly. This suits staged flows such as triage, then billing, then refunds.
- **Swarms and routers**: In a swarm, agents hand off to each other without a central boss. A router classifies the request once and sends it to one or more specialists, then combines the answers.
- **Debate and review**: Several agents answer independently, critique each other over rounds and converge. It can improve reasoning on hard questions at a multiple of the cost.
- **Shared state or message passing**: Agents can read and write one shared state object, or exchange only messages and results. Shared state keeps context together; message passing keeps agents isolated and easier to test.
- **Token cost and failure modes**: Anthropic reports that its multi-agent system used about 15 times the tokens of a chat. A study of over 1,600 annotated traces groups failures into poor system design, misalignment between agents, and weak verification.
- **Context sharing**: Cognition argues that agents working in parallel make conflicting hidden decisions. Pass full context to each agent, or keep dependent steps on a single thread.
- **Delegation contracts**: Give each worker a structured task with an objective, allowed tools and sources, the user it acts for, a deadline, a turn and token budget and an output schema. Each worker gets less authority than its parent, and the parent treats worker output as untrusted evidence to check, never as fact.
- **A2A protocol**: An open standard, now hosted by the Linux Foundation, for agents from different vendors. Agents discover each other through Agent Cards and exchange tasks. MCP connects an agent to tools; A2A connects agents to agents.

## Resources

### Start here

- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) · Anthropic · Article · Free · 30 min — The most detailed public account of an orchestrator-worker system in production, covering architecture, prompting lessons, token cost and evaluation.
- [Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) · Cognition · Article · Free · 15 min — Walden Yan's case for single-threaded agents, built on two principles: share full context, and remember that every action carries implicit decisions.
- [Choosing the Right Multi-Agent Architecture](https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture) · LangChain · Article · Free · 20 min — Compares subagents, skills, handoffs and routers with model-call and token counts for the same task, then maps requirements to patterns.

### Go deeper

- [Benchmarking Multi-Agent Architectures](https://www.langchain.com/blog/benchmarking-multi-agent-architectures) · LangChain · Article · Free · 15 min — Tests a single agent, a swarm and a supervisor on a τ-bench variant and shows how a supervisor loses information when it relays answers.
- [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/) · OpenAI · Docs · Free · 15 min — Contrasts orchestration by the model with orchestration in code, and agents-as-tools with handoffs, in a few clear pages.
- [Module 9: Orchestration Patterns and Multi-Agent Design](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-module-09-orchestration-and-multi-agent-design.md) · Agentic AI Mastery · Article · Free · 30 min — Compares workflow, single agent, handoff, manager and fan-out designs on one worked case, with a sample delegation contract and the cost, latency and failure maths.
- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) · Cemri et al. · Paper · Free · 1 h — Builds a taxonomy of 14 failure modes from traces across seven frameworks; use it to label the failures in your own runs.
- [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) · Du et al. · Paper · Free · 45 min — The original debate paper, where several model instances argue over rounds and converge, improving maths reasoning and factual accuracy.
- [Multi AI Agent Systems with crewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/) · DeepLearning.AI · Course · Free tier · 3 h — João Moura builds role-based crews for support, research and outreach tasks, showing sequential, parallel and hierarchical cooperation.

### Reference

- [Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent) · LangChain · Docs · Free · reference — Code for the subagents, handoffs, skills, router and custom-workflow patterns in LangChain and LangGraph.
- [Handoffs](https://openai.github.io/openai-agents-python/handoffs/) · OpenAI · Docs · Free · reference — How handoffs appear to the model as tools, plus input filters that control which history the next agent sees.
- [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents) · Anthropic · Docs · Free · reference — Defines subagents with their own prompts and tool limits, and shows how to cap nesting depth, concurrency and spend.
- [Core Concepts and Components in A2A](https://a2a-protocol.org/latest/topics/key-concepts/) · A2A Project · Docs · Free · reference — Defines Agent Cards, tasks, messages, parts and artifacts, the core vocabulary of the protocol.
- [a2aproject/A2A](https://github.com/a2aproject/A2A) · A2A Project · Repo · Free · reference — The protocol specification, with links to the official SDKs and sample agents.

## Practice

1. **Find the breaking point (1.5 h).** Give one agent tools from three domains, for example weather, recipes and unit conversion. Run the same 20 requests with 5, 10 and 20 tools available and record how often it picks the right tool. Done when you have a small table of accuracy by tool count.
2. **Supervisor versus handoffs (2 h).** Split those tools across three specialist agents. Build a supervisor version and a handoff version. Done when you have accuracy, model calls and total tokens for each on the same 20 requests.
3. **Parallel research (1.5 h).** Build a lead agent that splits a question about a public topic into three sub-questions. It runs three workers in parallel and merges their answers with sources. Done when you can compare its token cost and answer quality with a single agent on the same question.
4. **Label your failures (45 min).** Take five bad runs from exercises 2 and 3. Tag each with a failure mode from the MAST taxonomy in the Cemri et al. paper. Done when you can name the most common category and one fix for it.
5. **Optional: talk A2A (1.5 h).** Use an official A2A SDK to wrap one specialist as a server with an Agent Card. Call it from a separate client process. Done when the client reads the card and gets a completed task back.

## Checklist

- [ ] [Must ship] Measure where a single agent's tool choice degrades as you add tools.
- [ ] [Must ship] Build supervisor and handoff versions of the same system and compare accuracy and tokens.
- [ ] [Must ship] Write down when you would and would not use multiple agents, citing your own numbers.
- [ ] [Recommended] Run workers in parallel with separate contexts and merge their results.
- [ ] [Recommended] Tag failed runs with a published failure taxonomy.
- [ ] [Stretch] Expose one agent over A2A and call it from another process.

## You're ready when

- You can explain the supervisor, handoff, router, swarm and debate patterns and give a use case for each.
- You can state the token cost trade-off of a multi-agent design with a number from your own tests.
- You can argue both the Anthropic and the Cognition positions and say which fits a given task.
- You can explain what A2A adds that MCP does not.
