---
title: Memory and context engineering
level: L3
kind: core
hours: 8
summary: Decide what goes into an agent's context window, keep conversation history within budget, and give agents long-term memory that helps instead of misleading.
checked: 2026-10-16
---

## Why it matters
A model only knows what is in its context window on the current call. Earlier sessions, past mistakes and user preferences are gone unless you put them back. Bigger windows do not solve this. Research on "context rot" shows models get less reliable as inputs grow, even on simple tasks, and every extra token costs money and time.

Context engineering is choosing the smallest set of useful tokens for each step, such as instructions, tool definitions, retrieved facts, memories and recent history. Memory is how you keep useful information across steps and sessions without stuffing everything into every call. Get both right and a modest model stays on track over long tasks. Get them wrong and even a strong model drifts, repeats itself or acts on stale facts.

## What to learn
- **Short-term vs long-term memory**: Short-term memory is the state of the current run or conversation, usually the message list. Long-term memory persists across sessions in a store you control, and you load the relevant parts into context when needed.
- **Managing history**: Trim old turns to a token budget, fold earlier turns into a running summary, and clear bulky old tool results the agent no longer needs. Keep the system prompt and the latest turns intact.
- **Kinds of long-term memory**: Semantic memory holds facts, such as "the user prefers metric units". Episodic memory holds past experiences, such as how a similar task went. Procedural memory holds rules and instructions, often kept as an editable part of the system prompt.
- **Writing and reading memories**: Write in the hot path, with the agent calling a `save_memory` tool, or in the background after a run. Read with keyword or embedding search, filtered by user and ranked by relevance and recency, as in [Embeddings and vector search](#l2-embeddings-vector-search).
- **Memory stores**: Mem0 extracts and retrieves memories for you. LangGraph has a namespaced store with semantic search. Letta, from the MemGPT authors, treats the context window like RAM and external storage like disk, and gives the agent tools to move information between them. A SQLite table or a folder of files is often enough to start.
- **Skills and progressive disclosure**: A skill is a folder with a `SKILL.md` file (a name, a description and instructions) plus optional scripts and reference files. The agent sees only each skill's name and description until a task needs it, then loads the instructions and opens extra files on demand. Agent Skills began at Anthropic and is now an open format read by many agents, so it is a cheap way to give an agent procedures without bloating every prompt.
- **Context engineering moves**: Write notes outside the window, select only the relevant tools and memories, compress history, and isolate subtasks in sub-agents with their own clean context. Decide deliberately what enters each call.
- **Context rot and failure modes**: Long contexts weaken recall and reasoning. Common failures are poisoning (an early error keeps being reused), distraction by a long history, confusion from irrelevant tools, and clashes between conflicting facts.
- **Compaction**: When a run nears its limit, summarise the important state (decisions, open questions, file paths, URLs) and continue in a fresh window. Keep references so dropped details can be fetched again.
- **Memory hygiene**: Memories can be wrong, stale or private. Store sources and dates, let users view and delete what is stored, and never store secrets. Keep trusted state such as the user's identity, permissions and budgets outside the model's context, and recheck it before any write. Prompt caching, which rewards a stable prompt prefix, is covered in [Reliability, latency and cost](#l6-reliability-cost).

## Resources
### Start here
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · Anthropic · Article · Free · 30 min — Frames context as a limited attention budget and explains compaction, structured note-taking, just-in-time retrieval and sub-agents.
- [Context Engineering](https://www.langchain.com/blog/context-engineering-for-agents) · LangChain · Article · Free · 25 min — Sorts context techniques into four moves (write, select, compress, isolate) with examples from real agents.
- [Memory overview](https://docs.langchain.com/oss/python/concepts/memory) · LangChain · Docs · Free · 30 min — A clear conceptual guide to short-term and long-term memory, semantic, episodic and procedural memory, and when to write memories.
### Go deeper
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://www.trychroma.com/research/context-rot) · Chroma · Paper · Free · 30 min — Tests 18 models and shows reliability falling as input grows, even on simple retrieval and copying tasks.
- [How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) · Drew Breunig · Article · Free · 15 min — Names four failure modes (poisoning, distraction, confusion, clash) that you will recognise in your own agent logs.
- [How to Fix Your Context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html) · Drew Breunig · Article · Free · 20 min — The follow-up, with six practical tactics from tool loadouts to pruning, summarisation and offloading.
- [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) · Manus · Article · Free · 20 min — Production lessons such as keeping the prompt prefix stable for caching, using files as memory and leaving errors in context.
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) · Anthropic · Article · Free · 20 min — How a skill packages instructions, scripts and files that an agent loads in three stages, so it can carry many skills at a small context cost.
- [LLMs as Operating Systems: Agent Memory](https://www.deeplearning.ai/short-courses/llms-as-operating-systems-agent-memory/) · DeepLearning.AI · Course · Free tier · 1.5 h — The MemGPT authors teach core and archival memory and build an agent that edits its own memory with Letta.
### Reference
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) · Packer et al. · Paper · Free · 1 h — The paper behind virtual context management, which moves information between in-context and external memory tiers.
- [Cognitive Architectures for Language Agents](https://arxiv.org/abs/2309.02427) · Sumers et al. · Paper · Free · 1.5 h — The CoALA framework, which describes agents in terms of modular memory, an action space and decision-making.
- [Memory](https://docs.langchain.com/oss/python/langgraph/add-memory) · LangChain · Docs · Free · reference — Code for checkpointers, trimming and summarising messages, and long-term stores with semantic search in LangGraph.
- [Open Source Overview](https://docs.mem0.ai/open-source/overview) · Mem0 · Docs · Free · reference — Setup for the self-hosted Mem0 memory layer in library or server mode, with configurable vector stores.
- [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) · Anthropic · Docs · Free · reference — A file-based memory tool design you can copy for any provider, including the path-traversal checks you must implement.

## Practice
1. **History under budget.** Build a chat loop over a public API, such as a book search API, that keeps history under 4,000 tokens (example budget) by trimming and summarising. Done when a 40-turn conversation stays under budget and still recalls a fact from turn 2.
2. **Measure context rot yourself.** Hide one fact in 1,000, 10,000 and 50,000 tokens of public-domain filler text and ask for it ten times at each size. Done when you have a small table of accuracy by length for one model.
3. **Long-term memory.** Give your agent `save_memory` and `search_memory` tools backed by SQLite, adding embeddings if you like. Done when a fact saved in one session, such as a dietary preference for recipe suggestions, changes an answer in a new session.
4. **Compaction.** Make a research-style run exceed a small context limit, then add compaction that summarises state and keeps URLs. Done when the compacted run finishes and its answers match the uncompacted ones on three tasks.
5. **Try a memory library.** Repeat exercise 3 with Mem0 or the LangGraph store. Done when you have a short note comparing effort, control and retrieval quality with your own version.

## Checklist
- [ ] [Must ship] Keep conversation history within a token budget using trimming and a running summary.
- [ ] [Must ship] Add long-term memory with save and search tools, scoped per user.
- [ ] [Must ship] Write down what enters your agent's context on each call and why.
- [ ] [Recommended] Implement compaction for long runs that keeps references to dropped details.
- [ ] [Recommended] Run a small context-length experiment on one model.
- [ ] [Stretch] Compare your memory store with Mem0, Letta or the LangGraph store.
- [ ] [Stretch] Package one repeated procedure as a skill with a `SKILL.md` and a script, and check that your agent loads it only when a task needs it.

## You're ready when
- You can explain short-term, long-term, semantic, episodic and procedural memory with an example of each.
- Your agent keeps working past its context limit without losing key facts.
- You can name the four context failure modes and point to one in a real log.
- Users of your agent can see and delete what it remembers.
