---
title: Personal research agent
level: L3
weeks: 2
summary: Build a framework-free agent that researches questions with web search, page fetching and your own MCP notes server, stays within budgets, and writes short cited reports.
---

## The brief
You build a command-line research assistant for yourself. You ask it a question, such as "What are the main ways to run small language models on phones?", and it searches the web, reads the most useful pages, checks your own notes and writes a short report with citations. It remembers past research, so a follow-up question next week starts from what it already found.

You build it without an agent framework, using one LLM provider's SDK and plain Python. Alongside it you build a small MCP server for your personal notes or bookmarks, which the agent uses as a tool and which also works in other MCP-capable apps. Every run has step and cost budgets, and every step goes into a log you can inspect.

## What you'll practise
- [Tool calling in depth](#l3-tool-calling): designing search, fetch and notes tools with clear schemas, capped results and useful errors.
- [The agent loop](#l3-agent-loop): a hand-written loop with stop conditions, step and cost budgets, and error recovery.
- [Workflows and agent design patterns](#l3-workflow-patterns): choosing between a plain agent, plan-and-execute and an evaluator pass on the report.
- [Model Context Protocol (MCP)](#l3-mcp): building a notes or bookmarks server and connecting your agent to it as a client.
- [Memory and context engineering](#l3-memory-context): storing past research, recalling it later and keeping long runs inside the context window.
- [Building a RAG pipeline](#l2-rag-pipeline): grounding claims in fetched sources and citing them.

## Requirements
- [ ] [Must ship] Write the agent loop yourself in Python with one provider SDK and no agent framework, in a single readable module.
- [ ] [Must ship] Provide `web_search` and `fetch_page` tools with clear descriptions, JSON Schemas, a size cap on returned text and error results the model can act on.
- [ ] [Must ship] Build an MCP server for your notes or bookmarks with at least three tools and one resource, test it in the MCP Inspector, and connect your agent to it over stdio.
- [ ] [Must ship] Enforce a maximum number of steps, a cost budget per run and a timeout, and end every run with a stop reason and a partial report if needed.
- [ ] [Must ship] Write a JSONL run log with one line per step (time, tool, arguments, result size, tokens, cost, latency) and a final summary line.
- [ ] [Must ship] Save a summary of each finished run (question, findings, sources, date) and retrieve relevant past research at the start of new runs.
- [ ] [Must ship] Produce a Markdown report of 300–800 words with inline citations, a list of source URLs or note IDs, and an open-questions section.
- [ ] [Must ship] Keep 10 test questions and a script that runs them and prints pass rate, cost and steps per question.

**Safety note:** this agent combines private notes, untrusted web pages and a fetch tool that can send data out, the combination known as the lethal trifecta (see [Security and guardrails](#l5-security)). Keep nothing sensitive in its notes, let `fetch_page` open only URLs that `web_search` returned, and ask for confirmation before `add_note` saves text that came from the web.

## Stretch goals
- [ ] [Recommended] Add a plan-and-execute mode and compare it with the plain loop on your test set.
- [ ] [Recommended] Add an evaluator pass that checks every claim in the report has a citation and asks for a fix if not.
- [ ] [Stretch] Run independent searches and fetches in parallel when the model requests several at once.
- [ ] [Stretch] Add compaction so long runs continue past the context limit without losing sources.
- [ ] [Stretch] Serve your MCP server over Streamable HTTP with a bearer token and use it from a second device.

## Suggested stack
| Need | Suggested | Alternatives |
| --- | --- | --- |
| Model | One provider SDK with tool calling (Anthropic, OpenAI or Gemini) and a small, cheap model | A local model through Ollama that supports tool calling |
| Web search | Tavily (free plan with 1,000 credits a month at the time of writing) | Brave Search API, Exa, or your provider's built-in web search tool |
| Fetch and extract | httpx plus Trafilatura for main-text extraction | readability-lxml, BeautifulSoup |
| MCP server | Official MCP Python SDK | FastMCP |
| MCP testing | MCP Inspector | A desktop chat app or IDE with MCP support |
| Memory store | SQLite with full-text search (FTS5) | Chroma or pgvector for embedding search, Mem0 |
| Run log | JSONL files plus a small summary script | An open-source tracing tool such as Langfuse or Arize Phoenix |
| Config and secrets | A `.env` file loaded with python-dotenv and kept out of git | pydantic-settings |

## Build it step by step
1. **Set up the project.** Create a repo with uv, a `.env` file for keys, and folders for the agent, tools, MCP server and test questions. Write the 10 test questions first so you know what success looks like.
2. **Write the bare loop.** Implement `run_agent()` with a stub tool and a final-answer condition. Print every step so you can watch the message list grow.
3. **Add search and fetch.** Wrap the search API and a page fetcher with clear descriptions, a cap of a few thousand tokens per result, and error results for timeouts and blocked pages. Check that the model picks the right tool for each test question.
4. **Build the MCP server.** Expose `search_notes`, `read_note` and `add_note` (or bookmark equivalents) plus a resource listing all titles. Test it in the MCP Inspector, then in a desktop app or IDE.
5. **Connect the agent to MCP.** Start the server over stdio from your agent, list its tools, convert them to your provider's format and route calls back through the client. Your agent now has search, fetch and notes tools.
6. **Add budgets and the log.** Track tokens and cost from each response, stop on max steps, budget or timeout, and write one JSONL line per step. When a limit fires, make the agent write a partial report instead of nothing.
7. **Add memory.** After each run, save a summary with its sources and date. At the start of a run, search past summaries and put the best two or three into context, labelled with their dates.
8. **Write and check the report.** Ask for a structured report with citations, check in code that every cited URL was actually fetched, and run your test set. Fix the worst failures you find in the logs.

## How to evaluate it
| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Answer quality | 7 of 10 test questions get a report you rate as useful | 9 of 10, judged against a short written rubric |
| Citations | Every cited URL appears in the run log as fetched | Spot-checks of 10 claims find each one supported by its source |
| Budgets | No run exceeds its step or cost limit | Median cost per question is reported and under a target you set |
| Robustness | A failing tool or blocked page never crashes a run | Runs recover from injected tool failures and still produce a report |
| Memory | A follow-up question retrieves the earlier run's summary | Follow-up runs are measurably cheaper or better than first-time runs |
| MCP server | Works in the Inspector and in your agent | Also works in a third-party host and has a short threat note |

## Show your work
- A README with a one-paragraph overview, a text diagram of the loop and its tools, setup steps and one sample report.
- A short demo video or GIF of one research run, showing the step log and the final report.
- A write-up of what broke and how you fixed it, with numbers from your test set such as pass rate, median cost and steps.
- A CV line with your real numbers, for example "Built a framework-free research agent with a custom MCP server, budgets, run logging and long-term memory; 9 of 10 test questions answered under $0.05 each" (example figures).

## Ideas to make it yours
- Research papers instead of the web, using the free arXiv API as the search tool and a reading-list MCP server.
- A recipe researcher that checks your pantry notes and remembers dietary preferences.
- A product comparison helper that tracks prices and reviews across runs and reports what changed.
- A weekly monitor for an open-source project or a local news topic that writes "what's new since last time".
- A study companion that builds on your course notes and points out gaps in them.

## Helpful resources
- [How to Build an Agent](https://ampcode.com/how-to-build-an-agent) · Thorsten Ball · Tutorial · Free · 45 min — The closest template for a framework-free loop with simple tools, and easy to port to Python.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) · Anthropic · Article · Free · 30 min — Lessons from a production research agent on scaling effort to the question, prompting for search and evaluating results.
- [MCP quickstart resources](https://github.com/modelcontextprotocol/quickstart-resources) · MCP project · Repo · Free · reference — Complete example servers and chatbot clients in Python and other languages to start your notes server and client from.
- [Quickstart](https://docs.tavily.com/documentation/quickstart) · Tavily · Docs · Free tier · 15 min — Gets a search API key and a first search running from Python in a few minutes.
- [Trafilatura](https://trafilatura.readthedocs.io/en/latest/) · Trafilatura · Tool · Free · reference — Extracts the main text and metadata from web pages so your fetch tool returns clean content instead of raw HTML.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · Anthropic · Article · Free · 20 min — Shows how progress files and logs let an agent pick up work across sessions, a good model for your run log and memory.
