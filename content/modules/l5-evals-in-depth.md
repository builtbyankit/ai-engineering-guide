---
title: Evals in depth
level: L5
kind: core
hours: 10–12
summary: Run error analysis on agent traces, build an LLM judge calibrated against human labels, evaluate trajectories and block regressions with evals in CI.
checked: 2026-10-16
review-by: 2026-12-01 | OpenAI is retiring its hosted Evals platform (read-only from 31 October 2026 and shut down on 30 November 2026)
---

## Why it matters

In [Your first evals](#l1-first-evals) you checked single outputs against a small golden set. Agents are harder to measure. One run can include a dozen model and tool calls, and it can fail in ways no generic metric predicts. Teams that skip careful measurement often end up with a dashboard of generic scores, such as "helpfulness", that stays flat while users complain.

This module turns evals into an engineering habit. You will find failure modes by reading real traces, write cheap code checks where you can and build an LLM judge only where you must. You will prove that the judge agrees with a human, score the path an agent took as well as its result, and wire it all into CI. After that, a prompt or model change cannot quietly make your agent worse.

## What to learn

- **Error analysis first**: Read 50 to 100 real traces and write a short note on the first thing that went wrong in each. Group the notes into failure categories and count them. The counts tell you what to fix and what to evaluate.
- **Eval-driven development**: Write the eval for a failure mode before you change the prompt or code, then iterate until it passes. Every bug you fix becomes a permanent test case.
- **Code checks before judges**: Many failures can be caught with plain code: invalid JSON, the wrong tool, a missing citation, a banned phrase. Code checks are fast, cheap and deterministic, so write them first.
- **LLM-as-a-judge done right**: Use a judge only for failures code cannot catch. Give it one narrow criterion, ask for a binary pass or fail, and include a few labelled examples with written critiques.
- **Calibrating the judge**: Label 100 or more outputs yourself and split them into train, dev and test sets. Report the judge's true positive rate (TPR) and true negative rate (TNR) on the test set, because raw agreement hides problems when failures are rare. Expect your own criteria to shift as you label; Shankar and colleagues call this criteria drift.
- **Trajectory and tool-use evals**: For agents, grade the outcome (was the ticket filed, did the tests pass) and, where it helps, the path: which tools ran, with what arguments, in what order and in how many steps. Prefer outcome checks, since strict path checks can fail valid alternative routes.
- **Non-determinism, pass@k and pass^k**: Run each task several times. pass@k is the chance that at least one of k attempts succeeds. pass^k is the chance that all k succeed, which is closer to what users of a production agent experience.
- **Regression evals in CI**: Keep a versioned dataset, run it on every pull request that touches prompts, tools or model settings, and fail the build when the pass rate drops below a threshold you chose. Tune against a development set and keep a holdout you only score before release, and report sample sizes, since one failure in two cases is not a reliable 50%. [Deploying agent applications](#l6-deployment) builds on this gate.
- **Choosing eval tools**: Inspect AI suits agent tasks that need tools and sandboxes. promptfoo suits config-driven prompt tests and red-teaming in CI, DeepEval plugs into pytest, and LangSmith, Langfuse and Braintrust add hosted datasets and experiment tracking. OpenAI is retiring its hosted Evals platform (read-only from 31 October 2026 and shut down on 30 November 2026), so don't start new work there, and keep your dataset in a portable format such as JSONL.

## Resources

### Start here

- [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/) · Hamel Husain · Article · Free · 25 min — Makes the case that error analysis is the most valuable activity in AI development and shows how a simple custom data viewer makes it fast.
- [Demystifying evals for AI agents](https://anthropic.com/engineering/demystifying-evals-for-ai-agents) · Anthropic · Article · Free · 25 min — Defines tasks, trials, graders, transcripts and harnesses for agent evals, compares code, model and human graders, and works through pass@k versus pass^k.
- [Using LLM-as-a-Judge For Evaluation: A Complete Guide](https://hamel.dev/blog/posts/llm-judge/) · Hamel Husain · Article · Free · 30 min — A step-by-step method for building a binary judge from a domain expert's critiques and validating it with true positive and true negative rates.

### Go deeper

- [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) · Hamel Husain, Shreya Shankar · Article · Free · 2–3 h — A long, current FAQ on open and axial coding, binary versus Likert scores, judge validation, CI versus production monitoring and agentic workflows; read the sections you need.
- [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) · Hamel Husain · Article · Free · 20 min — The case study that organises evals into three levels: unit-test assertions, human and model review of traces, and A/B tests.
- [Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)](https://eugeneyan.com/writing/llm-evaluators/) · Eugene Yan · Article · Free · 50 min — Surveys judge prompting techniques, known biases such as position and verbosity bias, and what the research says about when judges can be trusted.
- [An LLM-as-Judge Won't Save the Product: Fixing Your Process Will](https://eugeneyan.com/writing/eval-process/) · Eugene Yan · Article · Free · 5 min — A short argument for eval-driven development as a loop of observing data, annotating failures and running measured experiments.
- [Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences](https://arxiv.org/abs/2404.12272) · Shankar et al. · Paper · Free · 1 h — The research behind aligning judges with human grades, including the finding that people's criteria change while they grade outputs.
- [Evaluating AI Agents](https://www.deeplearning.ai/short-courses/evaluating-ai-agents/) · DeepLearning.AI, Arize AI · Course · Free tier · 2.5 h — Hands-on video lessons on tracing an agent, evaluating its router, skills and trajectory, and running experiments when you change prompts or models.

### Reference

- [Inspect](https://inspect.aisi.org.uk/) · UK AI Security Institute · Docs · Free · reference — Open-source eval framework built from datasets, solvers and scorers, with built-in agents, tool use and sandboxed execution for agent tasks.
- [Promptfoo: Intro](https://www.promptfoo.dev/docs/intro/) · Promptfoo · Docs · Free · reference — Open-source CLI and library for config-driven evals and red-teaming that runs locally and inside CI pipelines.
- [DeepEval Quickstart](https://deepeval.com/docs/getting-started) · DeepEval · Docs · Free · reference — Apache-2.0 eval framework that runs like pytest and includes task-completion and component-level metrics for agents.
- [How to evaluate your agent with trajectory evaluations](https://docs.langchain.com/langsmith/trajectory-evals) · LangChain · Docs · Free · reference — Shows the open-source agentevals package with strict, unordered, subset and superset trajectory matching plus LLM-judged trajectories.
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) · OpenAI · Docs · Free · reference — Eval design guidance for workflows, single agents and multi-agent systems, covering tool selection, argument accuracy and judge biases.

## Practice

1. **Error analysis on 50 traces.** Run your Level 3 or Level 4 agent on 50 realistic inputs, such as support tickets or recipe questions. In a spreadsheet, write one note per trace on the first failure, then group the notes into 4 to 8 categories with counts. Done when you have a ranked failure table.
2. **Code checks for the top failures.** For each category code can detect (bad JSON, wrong tool, missing citation, too many steps), write an assertion in pytest or promptfoo. Done when the suite runs in under 2 minutes and flags the failing traces from exercise 1.
3. **Build and calibrate a judge.** Pick one subjective failure, for example "the answer ignores a constraint the user stated". Label 100 outputs pass or fail with a one-line critique, and split them roughly 20/40/40 into train, dev and test (an example split). Tune the judge on dev, then report TPR and TNR on test. Done when both are above 0.8 (an example target) or you can explain why not.
4. **Trajectory eval with repeats.** Write 10 tasks, each with an expected outcome and a reference tool sequence. Score each run on outcome, tool-set match and step count, and run each task 5 times. Done when you have a per-task table with pass@1 and pass^5.
5. **CI gate.** Add a GitHub Actions workflow that runs your suite on every pull request. Fail it when the pass rate falls more than 5 percentage points below the main branch (an example threshold). Done when a deliberately broken prompt turns the check red.

## Checklist

- [ ] [Must ship] Write a failure taxonomy from at least 50 real traces, with counts per category.
- [ ] [Must ship] Implement code-based assertions for every failure category that code can detect.
- [ ] [Must ship] Build one binary LLM judge and report its TPR and TNR on a held-out labelled set.
- [ ] [Must ship] Run the regression suite automatically on every pull request.
- [ ] [Recommended] Add trajectory checks for tool choice, arguments and step count, and report pass^k over repeated runs.
- [ ] [Stretch] Port one task to Inspect and run it inside a sandbox.

## You're ready when

- You can explain why error analysis comes before choosing metrics, and show the failure table that shaped your evals.
- Your LLM judge has a measured TPR and TNR on data it never saw during prompt tuning.
- You can explain pass@k versus pass^k and say which one your users experience.
- A pull request that breaks a known behaviour fails CI before anyone reviews it.
