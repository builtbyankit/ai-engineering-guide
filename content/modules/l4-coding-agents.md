---
title: Coding agents
level: L4
kind: optional
hours: 8–10
summary: Explain how coding agents search, edit and test code, run one safely in a sandbox, and build a small agent that fixes a failing test by itself.
checked: 2026-10-16
review-by: 2027-01-31 | the free tier includes one-time credits
---

## Why it matters

Coding is where agents already do real work every day. Tools such as Claude Code, Codex CLI, aider and OpenHands take a task in plain English. They search the repository, edit files and rerun the tests until they pass. Knowing how they work makes you far better at directing them.

Coding agents are also the clearest case study in agent design. They need well-shaped tools, a feedback signal, a safe place to run commands and a way to work across many context windows. Every one of those lessons transfers to agents in other domains. This module builds on [The agent loop](#l3-agent-loop) and [Tool calling in depth](#l3-tool-calling).

## What to learn

- **The loop is small**: A coding agent is a model, a few tools and a loop that runs until the model stops calling tools. Readable versions fit in a few hundred lines of code.
- **Core tools**: Most agents expose four kinds of tool: view a file, search (grep, glob, list files), edit, and run a shell command. Some minimal agents give the model only bash and let it use `cat`, `grep` and `sed` for everything.
- **Edit formats**: How the model writes changes matters. Common options are whole-file rewrites, search-and-replace blocks, unified diffs, and an exact string replacement that only applies when the old text matches once. A failed match gives the model a clear error to fix, which beats a silent bad edit.
- **Agent-computer interface (ACI)**: The SWE-agent paper showed that the design of an agent's tools strongly affects how many issues it solves. Good tools return short output, show line numbers and give error messages the model can act on.
- **Tests as the feedback signal**: An agent stops when the work looks done. A test suite, type checker or linter turns "looks done" into a pass or fail that the agent can read and iterate on.
- **Repository context**: No agent can hold a large codebase in its context window. Agents search on demand and may read a compact repo map of key symbols. They also load instruction files such as AGENTS.md or CLAUDE.md with build commands and conventions, plus skills they open only when a task needs them ([Memory and context engineering](#l3-memory-context)).
- **Sandboxing**: A coding agent runs commands written by a model that may have read hostile text. Run them in a container, VM or OS-level sandbox that limits which files it can touch and which hosts it can reach. Keep real credentials outside the sandbox.
- **Permission modes**: Coding tools range from approving every command to running unattended inside a sandbox. Match the mode to the damage a mistake could do ([Human in the loop](#l4-human-in-the-loop)).
- **Harnesses for long-running work**: For multi-session tasks, keep state outside the model in a feature list, progress file, git history and startup script. Each fresh session reads them, finishes one feature and leaves the code in a clean state.
- **SWE-bench**: The standard benchmark gives an agent a real GitHub issue from a Python repository and checks whether hidden tests pass after its patch. SWE-bench Verified is a 500-task, human-checked subset; in 2026 OpenAI stopped reporting it, citing flawed tests and contamination, and moved to SWE-bench Pro. Scores depend on the harness and infrastructure as well as the model, so read them critically ([Reading agent benchmarks](#l5-benchmarks)).

## Resources

### Start here

- [How to Build an Agent](https://ampcode.com/how-to-build-an-agent) · Thorsten Ball · Tutorial · Free · 1 h — Builds a working code-editing agent in Go with three tools (read, list, edit) and shows the whole loop fits in under 400 lines.
- [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) · SWE-agent team · Repo · Free · 1–2 h — A coding agent whose core class is about 100 lines of Python with bash as its only tool; read it end to end, then run it on a small task.
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) · Anthropic · Docs · Free · 45 min — Patterns that apply to any coding agent: give it a check it can run, explore then plan then code, keep instruction files short and manage context.

### Go deeper

- [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet) · Anthropic · Article · Free · 20 min — A minimal SWE-bench agent with only a bash tool and a string-replace edit tool, including the full tool descriptions and the reasoning behind each choice.
- [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) · Yang et al. · Paper · Free · 1.5 h — The paper that named the agent-computer interface and measured how the design of file viewing, search and edit commands changes an agent's results.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · Anthropic · Article · Free · 20 min — Explains an initializer agent plus a coding agent that share a JSON feature list, progress notes and git history so work survives across context windows.
- [Designing agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) · Simon Willison · Article · Free · 15 min — A practitioner's guide to running coding agents with approvals switched off: the risks, sandbox options, tightly scoped credentials and documenting CLI tools for the agent.
- [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) · Anthropic · Article · Free · 15 min — Explains why a coding-agent sandbox needs both filesystem and network isolation, and how a proxy outside the sandbox enforces a domain allowlist.
- [Repository map](https://aider.chat/docs/repomap.html) · aider · Docs · Free · 10 min — Shows how aider fits a large codebase into a small token budget by listing key symbols and ranking files with a dependency graph.

### Reference

- [AGENTS.md](https://agents.md/) · Agentic AI Foundation · Docs · Free · reference — The open format for repository instructions read by many coding agents, with suggested sections and precedence rules for nested files.
- [SWE-bench](https://www.swebench.com/) · SWE-bench team · Tool · Free · reference — Leaderboards for the full set, Verified, Lite, Multilingual and Multimodal, plus a bash-only track that runs every model in the same minimal agent.
- [E2B documentation](https://docs.e2b.dev/) · E2B · Docs · Free tier · reference — Python and JavaScript SDKs for starting disposable Linux sandboxes where an agent can run generated code; the free tier includes one-time credits.
- [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk) · OpenHands · Repo · Free · reference — An open-source Python SDK for coding agents with terminal and file-editor tools and workspaces that run locally or in Docker.
- [Codex CLI](https://github.com/openai/codex) · OpenAI · Repo · Free · reference — The open-source code of OpenAI's terminal coding agent, useful for reading how a production agent is put together.

## Practice

1. **Read a tiny agent.** Clone mini-SWE-agent and read the agent class and its default prompt. Sketch the loop: what goes in, which command runs, what comes back and when it stops. Done when you can explain each step without looking.
2. **Build your own.** Write a Python agent with four tools: `read_file`, `search` (wrapping grep), `edit_file` and `run_tests`. Make `edit_file` an exact string replace that fails unless the old text matches once. Restrict every path to the repo folder and work on a throwaway copy, or set up exercise 3's container first. Give it a small repo with one failing pytest test, for example a recipe-scaling function that rounds wrongly. Done when it makes the test pass without your help and logs every tool call.
3. **Sandbox it.** Make every shell command run inside a Docker container (or an E2B sandbox) with the repo mounted, no network and no host secrets. Done when a deliberate `curl https://example.com` from the agent fails and the agent still fixes the bug.
4. **Write repository instructions.** Write an AGENTS.md for a small project with build and test commands, style rules and two known traps. Give a coding agent the same task with and without the file. Done when you have notes on what changed: steps taken, wrong guesses and time.
5. **Run a mini benchmark.** Create five small bug-fix tasks, each with a hidden test, for example in a todo-list or invoice-total module. Run your agent three times on each. Done when you have a table of pass rate, steps and token cost, and can name the most common failure.

## Checklist

- [ ] [Must ship] Build a coding agent from scratch with read, search, edit and test tools that fixes at least one failing test unaided.
- [ ] [Must ship] Run all of the agent's shell commands inside a container or sandbox with no network access and no real credentials.
- [ ] [Must ship] Write an AGENTS.md for one repository and record its effect on a real task.
- [ ] [Recommended] Log every tool call and result to a JSONL file you can replay.
- [ ] [Recommended] Compare an exact-match edit tool with whole-file rewrites on the same tasks.
- [ ] [Stretch] Add a progress file and git commits so your agent can resume a multi-step task in a fresh context window.
- [ ] [Stretch] Run mini-SWE-agent on a few SWE-bench Lite tasks and read the trajectories of the failures.

## You're ready when

- You can explain which tools a coding agent needs and why exact-match edits and short tool outputs help.
- Your agent fixes a failing test inside a sandbox, and you can show its full trajectory.
- You can name the two sandbox boundaries (filesystem and network) and say what each one prevents.
- You can explain what SWE-bench Verified measures and why the same model scores differently in different harnesses.
- Your AGENTS.md changes an agent's behaviour in a way you can observe and describe.
