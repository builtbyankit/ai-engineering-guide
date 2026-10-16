---
title: Take an agent to production
level: L6
weeks: 1.5–2
summary: Deploy your hardened agent as a streaming, durable, budget-aware service with a gateway, prompt caching, an eval-gated CI/CD pipeline and canary releases for prompt changes.
---

## The brief

You take the agent you hardened in [Harden an agent](#p5-harden-agent) and run it as a real service that other people can use. Users send a task over HTTP and watch progress stream back. Short tasks answer in place, and long ones run in the background as durable workflows that survive restarts and crashes.

Behind the API, every model call goes through a gateway that handles fallbacks, per-user budgets and caching. Every change ships through CI that runs your evals, and prompt changes reach a small slice of traffic before everyone else. You host it on a free tier or for a few dollars a month. The audience is a small group of real testers, such as classmates, friends or an online community you belong to.

## What you'll practise

- [Deploying agent applications](#l6-deployment): SSE streaming, background jobs, durable execution, containers, configuration, CI/CD and canaries.
- [Reliability, latency and cost](#l6-reliability-cost): a gateway with timeouts, fallbacks, per-user budgets, prompt caching and cost per task.
- [Evals in depth](#l5-evals-in-depth): your eval suite becomes the gate every change must pass.
- [Observability and tracing](#l5-observability): traces carry the prompt version, model and cost, so you can compare canary and baseline.
- [Security and guardrails](#l5-security): secrets live in the platform's secret store, and the public endpoint needs auth and rate limits.

## Requirements

- [ ] [Must ship] Expose a FastAPI (or equivalent) endpoint that streams typed progress events over SSE and requires an API key or login.
- [ ] [Must ship] Run any task expected to take longer than about 30 seconds as a background job that returns a job id, with a status endpoint or event stream to follow it.
- [ ] [Must ship] Execute long runs as durable workflows (Temporal, Restate, Inngest or LangGraph with a persistent checkpointer) and demonstrate recovery after killing a worker mid-run.
- [ ] [Must ship] Route all model calls through an LLM gateway with timeouts, retries, at least one cross-provider fallback and per-user budgets that return a clear error when exceeded.
- [ ] [Must ship] Enable prompt caching on your main agent prompt and report the cache hit rate and cost per completed task.
- [ ] [Must ship] Ship from a container image that takes all config and secrets from environment variables, deployed to a public URL.
- [ ] [Must ship] Run unit tests and your eval suite in CI on every pull request, block merges below your threshold, and deploy main automatically.
- [ ] [Must ship] Release prompt changes as a canary to a fixed share of users, log the prompt version on every trace, and document how to promote or roll back.

## Stretch goals

- [ ] [Recommended] Add a semantic cache for repeated questions, scoped per tenant, and measure hit rate and wrong-hit rate on 50 test queries.
- [ ] [Recommended] Move a nightly eval run or backfill to a provider batch API and record the savings.
- [ ] [Stretch] Route easy steps to a smaller or self-served open model and compare cost and quality against the baseline.
- [ ] [Stretch] Add a human approval step that pauses a durable run and resumes it from a link or button.
- [ ] [Stretch] Load test with 50 concurrent users and report p50 and p95 time to first event.

## Suggested stack

| Need | Suggested | Alternatives |
| --- | --- | --- |
| API and streaming | FastAPI with its built-in SSE support | Starlette, Litestar, a Node.js server |
| Background jobs | RQ or Celery with Redis | Arq, Cloud Run jobs, a managed cloud queue |
| Durable execution | LangGraph with a Postgres checkpointer (no extra service) or Temporal (dev server locally, Temporal Cloud or self-hosted in production) | Restate, Inngest |
| LLM gateway | LiteLLM proxy in Docker with Postgres | Cloudflare AI Gateway, OpenRouter, your cloud's gateway |
| Prompt caching | Provider-native caching (automatic on OpenAI; on Anthropic, one top-level cache setting or explicit breakpoints) | An exact-match cache in the gateway |
| Hosting | Google Cloud Run (monthly free tier) or Render (free web service that sleeps after 15 idle minutes) | Fly.io (pay as you go after a short trial), Railway (small monthly credit), a small VPS with Docker Compose |
| Database and cache | Free tiers of managed Postgres and Redis | SQLite on a volume for a single instance |
| CI/CD | GitHub Actions with promptfoo or your pytest eval harness | GitLab CI, Buildkite |
| Canary and flags | A hash of the user id plus a rollout percentage in config | A feature-flag tool such as Unleash or GrowthBook |
| Tracing and cost | Langfuse or Arize Phoenix (open source) | LangSmith, your gateway's spend logs |

Free tiers and trial terms change often, so check each platform's pricing page before you commit.

## Build it step by step

1. **Containerise what you have.** Write a Dockerfile for your Level 5 agent and move every setting and key into validated environment variables. Confirm `docker run` works with a `.env` file that is never committed.
2. **Add the streaming API.** Create a POST endpoint that starts a run and streams SSE events for status, tool calls, tokens and completion. Test it with `curl -N` and a minimal web page.
3. **Split short and long work.** Send long tasks to a queue or durable workflow and return a job id. Make each LLM call and tool call a recorded step, and give side-effecting tools idempotency keys.
4. **Put the gateway in the middle.** Run LiteLLM with a database and create a virtual key per user with a budget and rate limit. Configure a timeout, retries and a fallback to a second provider, then point the agent at the gateway URL.
5. **Turn on prompt caching and measure.** Reorder prompts so stable content comes first and enable caching. Add cached tokens and cost per task to your traces and dashboard.
6. **Wire up CI/CD.** In GitHub Actions, run unit tests and your eval suite on pull requests and fail below your threshold. On merge to main, build the image, push it and deploy to your host.
7. **Add the canary.** Store prompts as versioned files and choose the version per request from a hash of the user id and a rollout percentage in config. Tag every trace with the version, and compare eval scores, error rate and cost before promoting.
8. **Break it on purpose.** Kill a worker mid-run, revoke the primary provider key and exhaust a test user's budget. Record what happened in each case and fix anything that failed badly.

## How to evaluate it

| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Responsiveness | First SSE event within 2 s at p95 for 10 concurrent users | First event within 1 s at p95 for 50 concurrent users, with load test results in the README |
| Durability | A run resumes after a worker restart | A kill at any step resumes with zero repeated model calls or duplicate side effects, shown in traces |
| Resilience | The fallback works when the primary key is revoked | Fallbacks, timeouts and retries are exercised by a scripted failure test, with success rate reported |
| Cost control | Per-user budget enforced and cost per task reported | Cost per task cut by a measured amount (for example 30%) through caching or routing, with eval scores held |
| Release safety | CI blocks merges that fail evals | A canary with automated comparison and one-command rollback, demonstrated on a real prompt change |
| Hosting cost | Runs on a free tier or for under about $10 a month | Monthly cost per 1,000 tasks documented and split into model and infrastructure |

## Show your work

- A README with an architecture diagram, one-command setup, the endpoints, how durability and fallbacks work, and a table of cost per task, cache hit rate and p95 latency.
- A two-minute demo video that starts a long run, kills the worker, shows the run resuming, then trips a user's budget.
- A short write-up of one failure you caused on purpose, what broke and how you fixed it.
- One CV line with numbers, for example "Deployed a durable agent service with eval-gated CI; cut cost per task 35% with prompt caching and routing."

## Ideas to make it yours

- Deploy a research assistant that runs 10-minute literature searches and emails a report when it finishes.
- Turn the support triage team from [Level 4](#L4) into a service with approval links that resume paused runs.
- Build a recipe or meal-planning agent with a per-user daily budget and semantic caching for common questions.
- Run an invoice-extraction agent where uploads go to a background queue and results arrive by webhook.
- Serve part of the workload from a small open model you fine-tuned in [Open models, fine-tuning and serving](#l6-open-models).

## Helpful resources

- [temporal-ai-agent](https://github.com/temporal-community/temporal-ai-agent) · Temporal · Repo · Free · reference — A multi-turn agent running inside a Temporal workflow with native and MCP tools, using LiteLLM so you can swap providers.
- [Quickstart](https://docs.litellm.ai/docs/proxy/docker_quick_start) · LiteLLM · Docs · Free · 30 min — Start the gateway with Docker Compose and Postgres, create virtual keys with budgets, and see why budgets need a database.
- [Quickstart: Build and deploy a Python (FastAPI) web app to Cloud Run](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-fastapi-service) · Google Cloud · Tutorial · Free tier · 30 min — Deploys a FastAPI app from source with one command onto a platform that has a monthly free tier.
- [Deploy for Free](https://render.com/docs/free) · Render · Docs · Free · 10 min — What the free web service, Postgres and Key Value tiers include, and limits such as spin-down after 15 idle minutes.
- [FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/) · FastAPI · Docs · Free · 30 min — The recommended FastAPI Dockerfile, layer caching, exec-form CMD and one process per container under an orchestrator.
- [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) · FastAPI · Repo · Free · reference — A production-style template with Postgres, Docker Compose, Traefik and GitHub Actions to borrow structure from.
