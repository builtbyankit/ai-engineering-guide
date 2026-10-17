---
title: Observability and tracing
level: L5
kind: core
hours: 8
summary: Instrument an agent with OpenTelemetry-style traces, inspect every model and tool call, and track tokens, cost, latency and user feedback on a dashboard.
checked: 2026-10-16
review-by: 2027-01-31 | They are still evolving and now live in their own repository
---

## Why it matters

When an agent gives a bad answer in production, the final output rarely tells you why. Maybe retrieval came back empty, or a tool timed out and the model guessed. Maybe the loop ran 14 steps and burned your budget. Without traces you re-run the request and hope it fails the same way, which agents often do not.

Tracing records each run as a tree of timed steps: the request, each model call with its tokens, and each tool call with its arguments and result. The same data serves three jobs. You debug single failures, you watch cost and latency across thousands of runs, and you sample real traffic for the error analysis from [Evals in depth](#l5-evals-in-depth).

## What to learn

- **Traces and spans**: A trace is one end-to-end run. It holds spans, and each span is a timed operation with a parent, attributes and a status. For agents the usual tree is an agent span containing model-call spans and tool-call spans.
- **OpenTelemetry (OTel)**: The vendor-neutral standard for traces, metrics and logs. Instrument once with OTel and you can send the same data over OTLP, its wire protocol, to Langfuse, Phoenix, LangSmith, Jaeger or a cloud backend.
- **GenAI semantic conventions**: Shared names for LLM spans and attributes, such as `gen_ai.request.model`, `gen_ai.usage.*` for tokens, and operations like `chat`, `invoke_agent` and `execute_tool`. They are still evolving and now live in their own repository, so check it before you rely on a field.
- **Automatic and manual instrumentation**: Libraries such as OpenLLMetry and OpenInference patch provider SDKs and frameworks for you. Add manual spans around your own logic, such as planning steps, retries and guardrail checks, so the tree mirrors your design.
- **Content capture and privacy**: Prompts and tool results can contain personal data. Many instrumentations leave content capture off by default. Decide what to record, redact sensitive fields before export and set a retention period.
- **Cost and latency**: Record input, output, cached and reasoning tokens per call, then compute cost from a price table. Track p50 and p95 latency (the times within which half and 95% of requests finish) per span type, steps per run, and cost per successful task alongside cost per call. [Reliability, latency and cost](#l6-reliability-cost) uses these numbers to cut spend.
- **Online quality signals**: Collect explicit feedback (thumbs, ratings, comments) and implicit signals (retries, copying the answer, abandoned sessions). Store them as scores on the trace so you can filter to the worst runs.
- **Online evaluation**: Run cheap code checks on every live trace and an LLM judge on a sample. Promote interesting failures into your offline eval dataset.
- **Choosing a tool**: Langfuse and Arize Phoenix are open source and self-hostable. LangSmith is a hosted platform with a free developer tier and close LangChain integration. OpenLLMetry is instrumentation that exports to any OTel backend. Choose by hosting needs, your framework and how well each ingests standard OTel data.

## Resources

### Start here

- [Inside the LLM Call: GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/) · OpenTelemetry · Article · Free · 10 min — Shows a real coding agent emitting `invoke_agent`, `chat` and `execute_tool` spans to a local dashboard and explains why content capture is off by default.
- [LLM Observability & Application Tracing](https://langfuse.com/docs/observability/overview) · Langfuse · Docs · Free · 20 min — A clear overview of what a trace captures for an LLM app (prompts, responses, tokens, latency, tool and retrieval steps) and how to start.
- [Tracing](https://openai.github.io/openai-agents-python/tracing/) · OpenAI · Docs · Free · 15 min — A concrete agent span model with agent, generation, function, guardrail and handoff spans, plus the setting that keeps sensitive data out of traces.

### Go deeper

- [AI Agent Observability: Evolving Standards and Best Practices](https://opentelemetry.io/blog/2025/ai-agent-observability/) · OpenTelemetry · Article · Free · 10 min — Explains the GenAI SIG's work on agent conventions and compares instrumentation baked into frameworks with separate OTel libraries.
- [Token & Cost Tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking) · Langfuse · Docs · Free · 15 min — How ingested and inferred costs differ, how model price tables work, and why reasoning tokens need explicit usage data to be priced correctly.
- [User Feedback](https://langfuse.com/docs/observability/features/user-feedback) · Langfuse · Docs · Free · 15 min — Compares explicit and implicit feedback and shows how to link a thumbs-up or thumbs-down in your UI to the trace that produced the answer.
- [Tracing quickstart](https://docs.langchain.com/langsmith/observability-quickstart) · LangChain · Tutorial · Free tier · 20 min — Adds tracing to a small tool-using app in a few lines, so you can compare a hosted tracer with a self-hosted one.

### Reference

- [OpenTelemetry semantic conventions for GenAI](https://github.com/open-telemetry/semantic-conventions-genai) · OpenTelemetry · Repo · Free · reference — The current home of the GenAI span, metric and attribute definitions, including agent and tool operations.
- [What is Arize Phoenix?](https://arize.com/docs/phoenix) · Arize AI · Docs · Free · reference — Open-source tracing and evaluation built on OpenTelemetry and OpenInference, with datasets and experiments for re-running traces.
- [OpenLLMetry](https://github.com/traceloop/openllmetry) · Traceloop · Repo · Free · reference — Apache-2.0 OTel instrumentation for many model providers, vector databases, agent frameworks and MCP, exportable to any OTel backend.

## Practice

1. **Trace one run by hand.** Use the OTel Python SDK with a console exporter. Wrap your agent loop in a root span and add child spans for each model call and tool call, with model name, token counts and tool name as attributes. Done when one run prints a correctly nested tree.
2. **Send traces to a backend.** Run Langfuse or Phoenix locally with Docker, point your exporter or their SDK at it, and run 20 tasks. Done when you can click from a slow run to the exact span that took the time.
3. **Cost and latency dashboard.** Build a view, in the tool or a notebook, of cost per run, p50 and p95 latency per span type, and steps per run. Done when you can name your most expensive prompt or tool and the share of total cost it causes.
4. **Feedback and online checks.** Add thumbs-up and thumbs-down to a minimal UI or CLI and store each click as a score on the trace. Add one code check that runs on every live trace. Done when you can filter to runs that failed either signal.
5. **Redaction.** Add a hook or span processor that masks email addresses and phone numbers before export. Done when a test trace with fake personal data shows only masked values in the backend.

## Checklist

- [ ] [Must ship] Instrument your agent so every model call and tool call appears as a span under one trace per run.
- [ ] [Must ship] Record model name, input and output tokens, latency and status on every model span.
- [ ] [Must ship] Show cost per run and p95 latency on a dashboard or in a notebook.
- [ ] [Recommended] Attach user feedback and at least one automated check to traces as scores.
- [ ] [Recommended] Redact personal data before traces leave your process.
- [ ] [Stretch] Export the same traces to two backends through an OpenTelemetry Collector to show you are not locked in.

## You're ready when

- You can open the trace for any failed run and point to the span where it went wrong.
- You can explain what the GenAI semantic conventions standardise and why you should check them before relying on a field.
- Your dashboard answers "what does one successful task cost?" and "what is our p95 latency?".
- You can show how a production trace becomes a new case in your offline eval set.
