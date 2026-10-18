---
title: Deploying agent applications
level: L6
kind: core
hours: 10–12
summary: Serve an agent behind a streaming API, run long jobs durably in the background, and ship changes safely with containers, CI eval gates and canary releases.
checked: 2026-10-16
review-by: 2027-04-30 | version 0.135.0 and later
---

## Why it matters

An agent that works in a notebook is one process on your laptop. Real traffic is harsher. Runs take ten minutes, browsers close mid-answer, servers restart during deploys, and a provider times out on step 14 of 20. If the run lives only in memory, each of those events loses work and money.

This module turns your agent into a service. You stream progress so users see something within a second. You move long runs off the request path into workers and durable workflows that resume after a crash. Then you package the service in a container, deploy it, and put an eval gate and a canary between every prompt change and your users.

## What to learn

- **Streaming with SSE**: Server-sent events (SSE) keep one HTTP response open and push small text events as they happen. Use them for tokens, tool-call notices and status updates; they pass through most proxies and browsers support them natively.
- **Keep long work off the request**: A web request should finish in seconds. Hand longer work to a worker through a queue (Redis with RQ or Celery, or a cloud queue), return a job id, and let the client poll or subscribe for progress.
- **Durable execution**: A durable workflow engine records each step's result in a log. After a crash it replays the log, skips finished steps and carries on, so you never pay twice for an LLM call or repeat a side effect. If you already use LangGraph, its checkpointer is the smallest step; Temporal, Restate and Inngest suit long runs that span services.
- **Determinism and idempotency**: Replay only works if workflow code makes the same decisions on every run. Put LLM calls, tool calls, clocks and random numbers inside recorded steps (activities or tasks), and give side-effecting tools idempotency keys.
- **Containers**: A Docker image bundles code, dependencies and the start command, so the same artifact runs on your laptop, in CI and in production. Copy dependency files before source code so rebuilds stay fast.
- **Serverless or Kubernetes**: Managed platforms such as Cloud Run, Render, Fly.io and Railway run your container for you, and some scale to zero. They limit request length, memory or always-on workers. Kubernetes gives full control over workers, GPUs and networking at the cost of running a cluster, so start managed and move when a limit bites.
- **Configuration and secrets**: Keep anything that differs between environments in environment variables, validated at startup. Store API keys in the platform's secret manager, never in the image or the repo.
- **CI/CD with an eval gate**: On every pull request, run unit tests plus the eval suite from [Evals in depth](#l5-evals-in-depth), and fail the build below a pass-rate threshold. Deploy automatically from the main branch only after the gate passes.
- **Run states, leases and unknown outcomes**: Give each run explicit states (queued, running, awaiting approval, complete, failed, cancelled). Let one worker own a run at a time through an expiring lease with a fencing token, so a stalled worker cannot write after another takes over. If a call with side effects times out after it was sent, mark it as outcome unknown and reconcile using the same idempotency key, never a new one.
- **Canary releases for prompts and models**: Treat a prompt or model change like a code deploy. Send a small share of traffic (for example 5%) to the new version, compare quality, cost and errors against the current one, then promote or roll back. Pausing runs for approval is covered in [Human in the loop](#l4-human-in-the-loop).

## Resources

### Start here

- [Deployments Concepts](https://fastapi.tiangolo.com/deployment/concepts/) · FastAPI · Docs · Free · 30 min — Covers HTTPS, startup, restarts, worker processes, memory per worker and one-time pre-start steps, the questions every deployment must answer.
- [Server-Sent Events (SSE)](https://fastapi.tiangolo.com/tutorial/server-sent-events/) · FastAPI · Docs · Free · 20 min — FastAPI's built-in SSE support (version 0.135.0 and later), with keep-alive pings, event ids and resuming from the Last-Event-ID header.
- [How To Build a Durable AI Agent with Temporal and Python](https://learn.temporal.io/tutorials/ai/durable-ai-agent/) · Temporal · Tutorial · Free · 2–3 h — Builds a tool-using chat agent with a FastAPI backend where every LLM and tool call is a recorded, retried step that survives crashes (needs under $1 of OpenAI credit).

### Go deeper

- [Durable execution](https://docs.langchain.com/oss/python/durable-execution) · LangChain · Docs · Free · 30 min — How LangGraph resumes a run from its last checkpoint, the exit, async and sync durability modes, and why side effects belong in tasks.
- [Durable Agents](https://docs.restate.dev/tour/ai-agents) · Restate · Tutorial · Free · 1 h — Journals LLM and tool calls so agents built with the OpenAI Agents SDK, Pydantic AI, LangChain or plain code resume from their first unfinished step.
- [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting) · Anthropic · Docs · Free · 30 min — Ephemeral, long-running and hybrid session patterns, where agent state lives on disk, how to size hosts and how to isolate tenants.
- [Building Durable, Production-Ready Agents with OpenAI SDK and Temporal](https://ai.engineer/talks/building-durable-production-ready-agents-with-openai-sdk-and-temporal) · AI Engineer · Video · Free · 1.5 h — Workshop by Temporal's Cornelia Davis showing an agent loop that survives a killed worker without spending tokens again.
- [Learn Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) · Kubernetes · Tutorial · Free · 2–3 h — Six short modules on deployments, services, scaling and rolling updates, enough to read a manifest and judge when you need a cluster.
- [Canarying Releases](https://sre.google/workbook/canarying-releases/) · Google SRE · Book · Free · 45 min — SRE Workbook chapter on choosing canary population, duration and metrics so only a small slice of users ever meets a bad release.

### Reference

- [Understanding Temporal](https://docs.temporal.io/evaluate/understanding-temporal) · Temporal · Docs · Free · 30 min — Defines workflows, activities, workers, task queues and the event history that makes recovery possible, the vocabulary every durable engine shares.
- [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) · FastAPI · Docs · Free · 15 min — Run small jobs after the response is sent, and see where the docs recommend moving to a real queue such as Celery.
- [Module 5: Durable Runs, Retries, and Recovery](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-module-05-durable-runs-and-recovery.md) · Agentic AI Mastery · Tutorial · Free · 1 h — A runnable SQLite run journal with expiring leases, fencing tokens and thirteen crash, race and restart checks, plus the recovery rules for unknown outcomes.
- [CI/CD Integration for LLM Evaluation and Security](https://www.promptfoo.dev/docs/integrations/ci-cd/) · promptfoo · Docs · Free · reference — A GitHub Actions example with a quality-gate step that fails the build when evals fail, plus caching and output formats.
- [Deploying with GitHub Actions](https://docs.github.com/en/actions/concepts/use-cases/deploying-with-github-actions) · GitHub · Docs · Free · reference — Environments, required reviewers and concurrency groups so production deploys wait for approval and never overlap.

## Practice

1. **Stream an agent run.** Wrap an agent from an earlier level (for example your research agent) in a FastAPI endpoint that streams SSE events named `status`, `tool_call`, `token` and `done`. Done when `curl -N` shows events arriving live and the first one lands within 1 second.
2. **Move a slow task to a worker.** Add `POST /jobs`, which enqueues a long agent run with RQ or Celery and returns a job id, and `GET /jobs/{id}` for status. Done when you can restart the web server mid-run and the job still finishes.
3. **Survive a crash.** Port the same run to a durable workflow (Temporal, Restate, or LangGraph with a SQLite or Postgres checkpointer). Kill the worker after step 3 and start it again. Done when the run completes and your logs show steps 1 to 3 did not call the model again.
4. **Containerise and deploy.** Write a Dockerfile, load settings from validated environment variables, and deploy to a free or low-cost platform. Done when a fresh clone plus one documented command builds the image, and the public URL streams a response.
5. **Gate and canary a prompt change.** Add a GitHub Actions workflow that runs your evals on pull requests and fails below a pass rate you choose. Then send 10% of users to a new prompt version by hashing the user id, and log the version on every trace. Done when you can show one blocked pull request and a side-by-side comparison of both versions.

## Checklist

- [ ] [Must ship] Stream agent progress to the client over SSE with typed events.
- [ ] [Must ship] Run long agent tasks in a worker or durable workflow, outside the request handler.
- [ ] [Must ship] Show a run resuming after you kill its worker, without repeating completed LLM calls.
- [ ] [Must ship] Build a Docker image whose config and secrets come only from environment variables.
- [ ] [Recommended] Block merges with a CI eval gate that fails below a set pass rate.
- [ ] [Recommended] Release a prompt change to a small traffic slice and compare it with the current version.
- [ ] [Stretch] Deploy the same image to a managed platform and to a local Kubernetes cluster (kind or minikube).

## You're ready when

- You can explain what happens to an in-flight agent run when the server restarts, and how your design recovers it.
- Your API sends its first event within about 1 second, and long runs return a job id immediately.
- You can point to each recorded step in your workflow and say why every side-effecting tool is safe to retry.
- Your pipeline refuses to deploy a prompt change that lowers your eval score.
- You can argue for a managed platform or Kubernetes for a given workload using run length, memory and traffic shape.
