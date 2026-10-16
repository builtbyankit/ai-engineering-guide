---
title: Stateful agents with LangGraph
level: L4
kind: core
hours: 10–12
summary: Build agents as explicit graphs with typed state, conditional routing, checkpoints, interrupts and streaming, and judge when a graph framework is worth its overhead.
checked: 2026-10-16
---

## Why it matters

In [The agent loop](#l3-agent-loop) you wrote a while loop around a model call. That works until a run has to survive a crash, wait two days for a manager's approval, or show a user what it is doing. Then you start writing your own state store, resume logic and event stream. Most teams end up rebuilding the same pieces.

LangGraph is a low-level orchestration library from LangChain that gives you those pieces. You describe the agent as a graph: nodes that do work, edges that decide what runs next, and a shared state object passed between them. A checkpointer saves that state after every step, so a run can pause, resume or be replayed. The same model sits under most durable agent runtimes, so learning it pays off even if you later pick a different tool.

## What to learn

- **State**: A typed object (TypedDict, dataclass or Pydantic model) that every node reads and updates. Design it first, because it is the contract between your steps.
- **Nodes and edges**: Nodes are plain functions that take the state and return an update. Normal edges fix the next step, and conditional edges call a routing function that picks it.
- **Reducers**: Rules for merging a node's update into the state. The default overwrites a key, while a message reducer such as `add_messages` appends new messages, which is what chat history needs.
- **Command and Send**: `Command` lets a node update state and choose the next node in one return value. `Send` fans work out to many parallel copies of a node, the map-reduce pattern.
- **Checkpointers and threads**: A checkpointer saves a snapshot after each step under a `thread_id`. In-memory savers lose everything on restart, and SQLite or Postgres savers keep it.
- **Interrupts**: Calling `interrupt()` inside a node pauses the run and saves its state. You resume by invoking the graph on the same thread with `Command(resume=...)`, and the node restarts from its top, so keep earlier side effects idempotent.
- **Streaming**: Stream modes let you watch state updates, model tokens or your own progress events while the graph runs. Use them to drive a UI instead of making users wait for the final answer.
- **Graph API and Functional API**: The Graph API makes nodes and edges explicit. The Functional API writes the same logic as ordinary Python with `@entrypoint` and `@task` and keeps persistence and interrupts.
- **When it is overhead**: A single tool-calling loop with no pauses, short runs and no branching rarely needs a graph. Reach for LangGraph when you need persistence, human approval, branching workflows or replay.

## Resources

### Start here

- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) · LangChain · Docs · Free · 20 min — Designs a customer support email agent step by step: map the workflow to nodes, decide what each needs, design the state, then wire the graph.
- [LangGraph quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart) · LangChain · Docs · Free · 30 min — Builds the same small tool-calling agent with the Graph API and the Functional API so you can compare the two styles directly.
- [Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) · LangChain Academy · Course · Free · 6 h — The official 55-lesson course with notebooks on state, reducers, memory, streaming, breakpoints, time travel, subgraphs and long-term memory.

### Go deeper

- [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) · LangChain · Docs · Free · 45 min — The full mental model of state schemas, reducers, conditional edges, `Send` and `Command`, with a short code sample for each.
- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) · LangChain · Docs · Free · 30 min — Explains checkpointers versus stores, threads, and why in-memory savers lose state on restart, plus common troubleshooting cases.
- [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming) · LangChain · Docs · Free · 25 min — Covers each stream mode, from state values and updates to model tokens and custom events, and how to stream out of subgraphs.
- [Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) · LangChain · Docs · Free · 45 min — Implements prompt chaining, routing, parallelisation, orchestrator-worker and evaluator-optimizer in LangGraph, a direct bridge from the Level 3 patterns.
- [AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) · DeepLearning.AI · Course · Free tier · 1.5–2 h — Harrison Chase and Rotem Weiss build an agent from scratch, rebuild it in LangGraph, then add persistence, streaming and human-in-the-loop.
- [How to think about agent frameworks](https://www.langchain.com/blog/how-to-think-about-agent-frameworks) · LangChain · Article · Free · 30 min — Harrison Chase separates orchestration from agent abstractions and argues that persistence, streaming and human-in-the-loop are what a framework should earn its place with; read it as the vendor's own case.

### Reference

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) · LangChain · Docs · Free · reference — Entry point to the official docs, with install steps and links to every core capability.
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) · LangChain · Docs · Free · reference — The exact API for pausing and resuming, plus the rules that bite: nodes re-run from the top, and a bare try/except swallows the pause.
- [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) · LangChain · Repo · Free · reference — Source code, examples and release notes; check here when the docs and your installed version disagree.

## Practice

1. **Draw before you code (1 h).** Pick a support-ticket workflow: classify the ticket, look up an answer in a few text files, draft a reply. Write the state schema and node list on paper, then build it as a graph with one conditional edge. Done when the compiled graph's printed structure matches your sketch.
2. **Survive a crash (1 h).** Swap the in-memory checkpointer for the SQLite one. Make a middle node raise an error on the first attempt, then resume with `graph.invoke(None, config)` on the same `thread_id`. Passing `None` tells LangGraph to continue from the last checkpoint instead of starting a new run. Done when the run finishes without repeating the nodes that already completed.
3. **Add an approval pause (1 h).** Call `interrupt()` before the "send reply" step so the run returns the draft for review. Resume once with an approval and once with an edited draft, each time from a fresh Python process. Done when both paths end in the right final state.
4. **Stream progress (30 min).** Run the graph with `stream_mode="updates"` and print one line per finished node, then switch to `"messages"` to show the draft token by token. Done when each step appears as it finishes, before the run ends.
5. **Check the overhead (45 min).** Rebuild exercise 1 as a plain loop in the style of [The agent loop](#l3-agent-loop). List what you would have to write yourself to match exercises 2 and 3. Done when you can state in three sentences when you would pick each approach.

## Checklist

- [ ] [Must ship] Build a graph with typed state, at least three nodes and one conditional edge.
- [ ] [Must ship] Persist runs with a SQLite or Postgres checkpointer and resume one after a failure.
- [ ] [Must ship] Pause a run with `interrupt()` and resume it with both an approval and an edit.
- [ ] [Recommended] Stream node updates and model tokens to the terminal or a small web page.
- [ ] [Recommended] Complete modules 1 to 3 of the LangChain Academy course.
- [ ] [Stretch] Use `Send` to fan out over a list of inputs and merge the results with a reducer.

## You're ready when

- You can explain what a checkpointer stores, what a thread is, and what happens to in-memory state on restart.
- Your graph resumes after a failure without redoing finished steps.
- Your graph pauses for human input and continues from the same point, even in a new process.
- You can name two situations where a plain loop beats a graph framework and two where it does not.
