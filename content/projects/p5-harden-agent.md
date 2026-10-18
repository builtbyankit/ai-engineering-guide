---
title: Harden an agent: evals, tracing and red-teaming
level: L5
weeks: 1.5–2
summary: Take your Level 3 or 4 agent and add error analysis, a calibrated judge, trajectory evals, a CI gate, tracing with cost dashboards and a prompt-injection red-team suite.
---

## The brief

You take an agent you already built, such as the research agent from Level 3 or the support triage agent from Level 4, and make it measurable, observable and harder to attack. You do not add new features. You add the engineering that lets a team change the agent with confidence: evals that catch regressions, traces that explain failures and a security suite that shows how it behaves under attack.

Imagine handing the agent to a small team who will run it for real users. They need to know what it costs per task, how often it fails and in what ways, and whether a poisoned document can make it leak data. Your deliverable is the repository, the dashboards and a short report that answers those questions with numbers.

## What you'll practise

- [Evals in depth](#l5-evals-in-depth): error analysis on real traces, a judge calibrated against your labels, trajectory evals with repeated runs and a CI gate.
- [Observability and tracing](#l5-observability): OpenTelemetry-style spans for model and tool calls, a cost and latency dashboard and feedback scores.
- [Security and guardrails](#l5-security): a lethal-trifecta threat model, an injection red-team suite, structural fixes and one guardrail layer.
- [Human in the loop](#l4-human-in-the-loop): approval gates on risky tools as a defence that holds even when the model is fooled.

## Requirements

- [ ] [Must ship] Trace every run with a root span plus child spans for each model call and tool call, including model name, tokens, latency and status.
- [ ] [Must ship] Review at least 50 traces and publish a failure taxonomy with counts per category.
- [ ] [Must ship] Write code-based assertions for each failure category code can detect, and at least one binary LLM judge with TPR and TNR reported on a held-out labelled set.
- [ ] [Must ship] Add trajectory evals for at least 10 tasks that check outcome, tool choice and step count, run 3 or more times each with pass^k reported.
- [ ] [Must ship] Run the eval suite in CI on every pull request and fail the build on a regression beyond a stated threshold.
- [ ] [Must ship] Show cost per run, cost per successful task and p95 latency on a dashboard or notebook.
- [ ] [Must ship] Build a prompt-injection suite of at least 20 cases, report attack success rate, apply at least one structural fix and report the rate again.
- [ ] [Must ship] Write a threat model naming your agent's private data, untrusted inputs and outbound channels, and which one you removed or gated.

## Stretch goals

- [ ] [Recommended] Add one guardrail model or filter and report its false positive rate on at least 30 benign inputs.
- [ ] [Recommended] Collect thumbs-up and thumbs-down feedback as trace scores and run a sampled online judge on live traces.
- [ ] [Stretch] Run an automated multi-turn attack campaign with PyRIT or promptfoo and add the successful attacks to your regression suite.
- [ ] [Stretch] Port your trajectory evals to Inspect and run tool-using tasks inside a Docker sandbox.

## Suggested stack

| Need | Suggested | Alternatives |
| --- | --- | --- |
| Agent under test | Your Level 3 or Level 4 agent | Any small tool-using agent you wrote |
| Tracing | OpenTelemetry SDK with OpenLLMetry or OpenInference | Built-in tracing in your agent SDK |
| Trace store and dashboard | Langfuse, self-hosted with Docker Compose | Arize Phoenix, LangSmith free tier, a notebook over exported spans |
| Eval runner | pytest plus promptfoo | Inspect, DeepEval |
| Judge model | A mid-sized hosted model with structured output | A local open model through Ollama |
| CI | GitHub Actions | GitLab CI |
| Red-teaming | promptfoo red-team mode and hand-written cases | garak, PyRIT |
| Guardrails | Llama Guard or Presidio for PII | NeMo Guardrails, Guardrails AI |

## Build it step by step

1. **Freeze a baseline.** Tag the current agent version and record its model, prompts and tools. Pick 3 to 5 core jobs the agent must do well.
2. **Instrument before you evaluate.** Add OTel spans for the agent loop, model calls and tool calls, and send them to Langfuse or Phoenix. Error analysis is far quicker when you can click through traces.
3. **Review 100 traces.** Run a mix of realistic and synthetic inputs, write a note on the first failure in each trace and group the notes into categories. Rank the categories by count and by impact.
4. **Write checks, then the judge.** Turn every code-checkable failure into an assertion. For one subjective failure, label at least 100 outputs, build a binary judge on a small training split and report TPR and TNR on the test split.
5. **Add trajectory evals and gate CI.** Give each of your 10 or more tasks an expected outcome and allowed tool set, run each several times and compute pass^k. Wire the suite into GitHub Actions with a threshold relative to the main branch.
6. **Red-team the agent.** Map the lethal trifecta for your tools, then write at least 20 injections hidden in documents, web pages and tool results. Add a scanner run with a capped number of tests against a test copy whose outbound and side-effecting tools are stubbed, set a spending limit first, and record attack success rate.
7. **Fix by design and re-measure.** Remove or gate one leg of the trifecta, for example with plan-then-execute, a quarantined reader or human approval. Re-run the evals and the red-team suite, and confirm normal tasks still pass.
8. **Report.** Build the dashboard view for cost and latency, then write a one-page summary with before and after numbers.

## How to evaluate it

| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Error analysis | 50 traces reviewed, 4 or more categories with counts | 100 or more traces, categories refined in a second pass, each linked to an eval |
| Judge calibration | TPR and TNR reported on 30 or more held-out examples | Both at or above 0.85 (example target) on 50 or more held-out examples, with notes on every disagreement |
| Trajectory evals | 10 tasks with outcome, tool-choice and step-count checks, run 3 times each with pass^3 reported | 20 or more tasks, tool-argument checks and pass^5 per task |
| CI gate | Suite runs on every pull request and blocks regressions | Results posted on the pull request, runtime under 10 minutes, threshold justified by run-to-run noise |
| Tracing and cost | Every model and tool call traced, cost per run visible | Cost per successful task, p50 and p95 per span type, feedback scores and redacted personal data |
| Security | 20 injection cases, attack success rate measured before and after one fix | 50 or more cases including multi-turn attacks, zero successful exfiltrations after fixes, guardrail false positive rate reported |

## Show your work

- A README with the failure taxonomy, the eval results table, judge TPR and TNR, the threat model and attack success rates before and after your fixes.
- A 2 to 3 minute video: a broken prompt turning CI red, a drill-down from a slow trace to the guilty span, and an injection attempt being blocked.
- A short write-up on what reviewing 100 traces taught you about your agent, with one surprising failure.
- A CV line such as "Built eval, tracing and red-team pipeline for an LLM agent; cut injection success rate from X% to Y% and added a CI regression gate".

## Ideas to make it yours

- Harden a recipe assistant that reads web pages users paste in, where injections hide in recipe blogs.
- Harden an email triage agent where every incoming message is untrusted input.
- Harden an invoice-processing agent that reads PDFs and can call a mock payments API.
- Compare two guardrails on the same injection suite and report the trade-off between blocked attacks and blocked benign inputs.
- Compare two models as the agent's brain using pass^k and cost per successful task.

## Helpful resources

- [Getting Started by Example](https://opentelemetry.io/docs/languages/python/getting-started/) · OpenTelemetry · Tutorial · Free · 30 min — The official Python walkthrough for adding traces to an app, the starting point for your own agent spans.
- [OpenTelemetry (OTEL) for LLM Observability](https://langfuse.com/integrations/native/opentelemetry) · Langfuse · Docs · Free · reference — How to send OTLP traces to Langfuse and how GenAI semantic convention attributes map to its model, usage, input and output fields.
- [Docker Compose Deployment](https://langfuse.com/self-hosting/deployment/docker-compose) · Langfuse · Docs · Free · 30 min — Runs a self-hosted Langfuse locally or on a small VM, with clear notes on what this setup lacks for real production use.
- [Module 7: Threat-Model the Agent, Not Just the Prompt](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-module-07-agent-security-threat-model.md) · Agentic AI Mastery · Tutorial · Free · 45 min — A worked threat register for a support agent with controls, evidence and remaining gaps, runnable security checks and release gates to copy into your own threat model.
- [Red Team Quickstart](https://promptfoo.dev/docs/red-team/quickstart/) · Promptfoo · Docs · Free · 30 min — Sets up an automated adversarial scan against an HTTP endpoint or custom target, covering injection, jailbreak and data-leak plugins.
- [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352) · Debenedetti et al. · Paper · Free · 1 h — 97 realistic agent tasks and 629 injection cases that show how to structure your own attack suite and measure utility alongside security.
