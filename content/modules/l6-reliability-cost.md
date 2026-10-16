---
title: Reliability, latency and cost
level: L6
kind: core
hours: 8–10
summary: Put an LLM gateway in front of your agent with fallbacks, budgets and caching, then measure and cut latency and cost per task without losing quality.
checked: 2026-10-16
---

## Why it matters

Agents multiply every weakness of a single LLM call. A run that makes 20 model calls has 20 chances to hit a timeout, and it costs 20 times as much. Provider outages, rate limits and one user looping your agent all night are normal events in production. Each one shows up as an angry user or a surprise bill.

This module gives you the controls. A gateway routes calls across providers, retries sensibly and enforces per-user budgets. Prompt caching, batching, routing to smaller models and semantic caching cut cost and latency. Measuring cost per completed task tells you whether any of it worked.

## What to learn

- **LLM gateway**: A proxy between your app and model providers that exposes one API, usually OpenAI-compatible. It centralises keys, logging, retries, fallbacks, rate limits and spend tracking. LiteLLM is the common self-hosted choice, and Cloudflare AI Gateway, OpenRouter and the major clouds offer hosted ones; choose by whether you must self-host and which providers you need.
- **Timeouts, retries and backoff**: Set a timeout on every model and tool call. Retry only transient errors (429, 5xx, timeouts) with capped exponential backoff and jitter, and retry at one layer only so retries do not multiply.
- **Fallbacks**: When a model still fails after retries, send the request to a backup model or provider. Test fallbacks on purpose, because the backup may format tool calls differently or have a smaller context window.
- **Rate limits and per-user budgets**: Cap requests and tokens per minute for each user or API key, and set a daily spend limit per user. This protects you from abuse, runaway agent loops and one customer starving everyone else.
- **Prompt caching**: Providers can reuse the processed prefix of a prompt across calls, charging a fraction of the normal price for cached input tokens and responding faster. Put stable content (system prompt, tool definitions, reference documents) first and anything that changes per request last.
- **Semantic caching**: Store answers keyed by the embedding of the question, and return a stored answer when a new question is similar enough. It suits FAQ-style traffic. A loose threshold returns wrong answers, so scope the cache per user or tenant and tune the threshold on real queries.
- **Batching**: Work that can wait up to 24 hours, such as nightly evals, backfills and bulk classification, can go through provider batch APIs at half the normal price.
- **Model routing and cascades**: Send easy requests to a small, cheap model and hard ones to a strong model. You can route with simple rules, a trained router, or a cascade that escalates when the cheap answer fails a check.
- **Cost per task**: Track tokens and dollars per completed task rather than per call, split by step. It tells you whether a change saved money or only moved cost elsewhere. Your traces from [Observability and tracing](#l5-observability) already hold the raw data.

## Resources

### Start here

- [Building A Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html) · Chip Huyen · Article · Free · 45 min — Shows where a gateway, router, caches and guardrails sit in a real LLM application and what each component buys you.
- [LiteLLM AI Gateway](https://docs.litellm.ai/docs/simple_proxy) · LiteLLM · Docs · Free · 1 h — Overview of the self-hosted, OpenAI-compatible proxy with virtual keys, per-key budgets, spend tracking, load balancing, fallbacks and retries.
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) · Anthropic · Docs · Free · 30 min — How cache breakpoints, cache lifetimes and write and read pricing work, and how to confirm cache hits from the usage fields.

### Go deeper

- [Timeouts, retries, and backoff with jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter) · Marc Brooker, AWS · Article · Free · 25 min — Why naive retries turn small failures into outages, and how timeouts, capped backoff, jitter and single-layer retries prevent it.
- [Latency optimization](https://developers.openai.com/api/docs/guides/latency-optimization) · OpenAI · Docs · Free · 30 min — Seven provider-neutral principles for faster LLM apps, from generating fewer tokens to parallelising calls or skipping the LLM entirely.
- [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) · Eugene Yan · Article · Free · 1–1.5 h — A long survey of production patterns; read the caching, guardrails and defensive UX sections for this module.
- [FrugalGPT](https://arxiv.org/abs/2305.05176) · Chen, Zaharia and Zou · Paper · Free · 1 h — Introduces LLM cascades that try cheaper models first and escalate only when needed, with large reported cost savings.
- [RouteLLM](https://github.com/lm-sys/RouteLLM) · LMSYS · Repo · Free · 1 h — Open-source routers that send each query to a strong or a weak model by predicted difficulty, usable as an OpenAI-compatible server.
- [LangCache concepts](https://redis.io/docs/latest/develop/ai/context-engine/langcache/concepts/) · Redis · Docs · Free · 20 min — A plain explanation of semantic caching, the similarity-threshold trade-off and why false cache hits happen.

### Reference

- [Fallbacks (Provider Failover)](https://docs.litellm.ai/docs/proxy/reliability) · LiteLLM · Docs · Free · reference — Configure retries, timeouts, cooldowns and general, context-window and content-policy fallbacks in the gateway.
- [Budgets, Rate Limits](https://docs.litellm.ai/docs/proxy/users) · LiteLLM · Docs · Free · reference — Budgets per user, key and team with scheduled resets, plus TPM, RPM and parallel-request limits.
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) · OpenAI · Docs · Free · reference — OpenAI's automatic prefix caching and its advice on prompt order and cache keys, useful to compare with Anthropic's choice of one top-level cache setting or explicit breakpoints.
- [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) · Anthropic · Docs · Free · reference — Submit large jobs at half the standard price with results within 24 hours; OpenAI's Batch API offers the same discount.
- [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) · Cloudflare · Docs · Free · reference — A hosted gateway with caching, rate limiting, retries, model fallback and cost analytics, if you prefer not to run LiteLLM yourself.

## Practice

1. **Put a gateway in front of your agent.** Run LiteLLM in Docker, add two models from different providers (or one hosted model and one local Ollama model), and point your agent at it. Done when switching models is a config change and every call appears in the gateway's spend log.
2. **Break the primary on purpose.** Configure retries, a timeout and a fallback, then give the primary an invalid key or a 1-second timeout. Done when 20 requests in a row still succeed and your logs show which model answered each one.
3. **Enforce a per-user budget.** Issue a virtual key per test user with a small daily budget (for example $0.50) and a requests-per-minute limit, then write a loop that blows through it. Done when the gateway refuses further calls and your API returns a clear 429 message the user can understand.
4. **Measure prompt caching.** Restructure one agent prompt so the system prompt and tool definitions form a stable prefix, enable caching where the provider needs it, and run the same 10-step task 10 times. Done when you have a before-and-after table of cached input tokens, total cost and time to first token.
5. **Compute cost per task and cut it.** For 30 tasks from your eval set, record tokens and dollars per completed task. Try one cheaper option, such as routing easy steps to a smaller model, batching an offline step or adding a semantic cache. Done when you can show the new cost per task and an eval score within a margin you set in advance.

## Checklist

- [ ] [Must ship] Route all model calls through a gateway or one client wrapper, with a timeout on every call.
- [ ] [Must ship] Configure at least one cross-provider fallback and prove it works by breaking the primary.
- [ ] [Must ship] Enforce a per-user spend or token budget that returns a clear error when exceeded.
- [ ] [Must ship] Enable prompt caching and record the cache hit rate and savings on a repeated task.
- [ ] [Recommended] Report cost per completed task, split by step, on a dashboard.
- [ ] [Recommended] Move one offline workload to a batch API and record the savings.
- [ ] [Stretch] Add a model router or cascade and chart its cost against quality on your eval set.

## You're ready when

- You can explain what your system does when the primary provider returns 429 errors for 10 minutes.
- Your logs show cached input tokens on repeated calls, and you can say which prompt changes break the cache.
- You can state your cost per completed task and its single biggest contributor.
- A test proves that one user cannot spend more than the cap you set.
