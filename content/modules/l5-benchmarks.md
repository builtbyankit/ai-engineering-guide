---
title: Reading agent benchmarks
level: L5
kind: optional
hours: 4–6
summary: Know what the major agent benchmarks measure, compute pass@k and pass^k, spot contamination and leaderboard pitfalls, and read a model launch claim critically.
checked: 2026-10-16
---

## Why it matters

Every model launch comes with a table of benchmark scores. You will use those numbers to pick models for your agents, and colleagues will quote them to you. A score only means something once you know the tasks, how success is checked, which scaffold ran the model, how many attempts it got and whether the test data leaked into training.

This optional module teaches you to read those tables like a reviewer. It also makes you a better builder. The flaws that weaken public benchmarks, such as weak tests, lenient graders and ignored cost, also weaken the private evals you write in [Evals in depth](#l5-evals-in-depth).

## What to learn

- **SWE-bench and SWE-bench Verified**: Agents fix real GitHub issues in Python repositories, and hidden unit tests decide success. Verified is a 500-task subset screened by human annotators. Later analyses found it concentrated in a few repositories, mostly short fixes and heavily contaminated, and in February 2026 OpenAI stopped reporting it in favour of SWE-bench Pro.
- **τ-bench (tau-bench)**: Simulated customer-service conversations in which an LLM plays the user and the agent must follow a domain policy while using tools. Success is checked against the final database state. τ²-bench extends it to more domains.
- **GAIA**: Questions that are simple for people but need browsing, file reading and several reasoning steps. Short factual answers make automatic scoring reliable.
- **WebArena and OSWorld**: Agents operate self-hosted websites or a full desktop, and scripts check the end state. [Browser and computer-use agents](#l4-computer-use) covers them in detail.
- **Terminal-Bench**: Hard command-line tasks, each with its own container, a human-written solution and verification tests. The version 2.0 paper describes 89 tasks, and newer versions have followed, so check which one a claim uses.
- **pass@k and pass^k**: pass@k counts a task as solved if any of k attempts succeeds, so it rises as k grows. pass^k needs all k attempts to succeed, so it falls as k grows and better reflects production reliability.
- **Contamination and overfitting**: Public tasks leak into training data, and teams tune their scaffolds to a benchmark. Held-out or private test sets and freshly written tasks reduce both problems.
- **Scaffold, cost and validity**: Scores depend on the agent harness as much as the model, and on how much compute was spent. Cost-aware leaderboards plot accuracy against dollars. Also ask whether each task tests the claimed skill and whether the grader accepts only real successes.
- **Reading a launch claim**: Ask which benchmark version and split was used, which scaffold, how many attempts, pass@1 or best-of-n, what it cost, who ran it and whether competing models got the same setup.

## Resources

### Start here

- [What skills does SWE-bench Verified evaluate?](https://epoch.ai/blog/what-skills-does-swe-bench-verified-evaluate) · Epoch AI · Article · Free · 15 min — Breaks the 500 tasks down by repository, difficulty and age, and shows how much scaffolds and contamination shape the scores.
- [Why SWE-bench Verified no longer measures frontier coding capabilities](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) · OpenAI · Article · Free · 10 min — A 2026 audit that found flawed tests and memorised solutions, and explains the move to SWE-bench Pro and privately written evals.
- [Sierra's τ-bench is shaping the development and evaluation of agents](https://sierra.ai/blog/tau-bench-shaping-development-evaluation-agents) · Sierra · Article · Free · 10 min — Explains the tool-agent-user setup and the pass^k metric, including how reliability drops when the same task is repeated.

### Go deeper

- [AI Agents That Matter](https://arxiv.org/abs/2407.01502) · Kapoor et al. · Paper · Free · 1.5 h — Argues for cost-controlled comparisons and proper holdout sets, showing how accuracy-only leaderboards reward needlessly expensive agents.
- [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825) · Zhu et al. · Paper · Free · 1.5 h — The Agentic Benchmark Checklist, with concrete flaws found in popular benchmarks that misstate agent performance.
- [SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?](https://arxiv.org/abs/2509.16941) · Deng et al. · Paper · Free · 1 h — A harder successor with 1,865 tasks split into public, held-out and commercial sets to resist contamination.
- [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](https://arxiv.org/abs/2601.11868) · Merrill et al. · Paper · Free · 1 h — How a modern agent benchmark is built, from per-task containers and verification tests to an error analysis of agent failures.
- [GAIA: a benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983) · Mialon et al. · Paper · Free · 45 min — Questions that are easy for people but hard for agents, designed so short answers can be scored automatically.
- [Measuring AI Ability to Complete Long Software Tasks](https://arxiv.org/abs/2503.14499) · Kwa et al. · Paper · Free · 1 h — Defines the 50% time-horizon metric often quoted in launches and its doubling trend, with a frank section on limits to external validity.

### Reference

- [SWE-bench](https://www.swebench.com/) · SWE-bench team · Tool · Free · reference — The official site and leaderboards for SWE-bench and its variants.
- [τ²-bench](https://github.com/sierra-research/tau2-bench) · Sierra · Repo · Free · reference — MIT-licensed simulator for tool-agent-user evaluations across airline, retail, telecom and other domains, linked to a public leaderboard.
- [Terminal-Bench](https://www.tbench.ai/) · Terminal-Bench team · Tool · Free · reference — The current Terminal-Bench leaderboard with resolution rate, cost and token columns, plus instructions for running it.
- [HAL: Holistic Agent Leaderboard](https://hal.cs.princeton.edu/) · Princeton SAgE · Tool · Free · reference — Third-party, cost-aware leaderboard that runs agents on GAIA, τ-bench, a SWE-bench Verified subset and more with one shared harness.
- [AI benchmarks & capabilities](https://epoch.ai/benchmarks) · Epoch AI · Tool · Free · reference — Independent benchmark runs and collected results for leading models, free to browse and download.

## Practice

1. **Compute pass@k and pass^k.** Take 10 tasks from your own eval set and run your agent 8 times on each. Compute pass@1, pass@8 and pass^8 per task and overall. Done when you can explain the gap between pass@8 and pass^8 in one paragraph.
2. **Audit a launch claim.** Pick a recent model announcement that includes an agent benchmark table. For each number, record the benchmark version, scaffold, attempts, cost and who ran it. Done when every claim is marked comparable, not comparable or unknown.
3. **Read real tasks.** Read five SWE-bench Verified or τ-bench tasks end to end, including their tests or goal state. Done when you have noted for each task whether a wrong solution could pass or a right one could fail.
4. **Cost against accuracy.** From HAL or the Terminal-Bench leaderboard, plot accuracy against cost for 8 to 10 entries. Done when you can name the entry you would choose for a budget-limited agent and explain why.

## Checklist

- [ ] [Must ship] Calculate pass@1, pass@k and pass^k for your own agent on at least 10 tasks.
- [ ] [Must ship] Write a one-page critique of the agent benchmark claims in one model launch.
- [ ] [Must ship] Read the task format and grader of two benchmarks from this module.
- [ ] [Recommended] Apply three items from the Agentic Benchmark Checklist to your own eval suite and fix one weakness.
- [ ] [Stretch] Run a small public benchmark subset, for example through Inspect or the τ²-bench repo, on two models and compare with published numbers.

## You're ready when

- You can say in one sentence what SWE-bench Verified, τ-bench, GAIA, WebArena, OSWorld and Terminal-Bench each measure.
- You can explain why pass^k matters more than pass@k for an agent people rely on.
- You can name three ways a benchmark score can mislead and the question that exposes each.
- You can choose between two models for your agent using benchmark data together with your own evals.
