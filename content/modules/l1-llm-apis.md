---
title: Calling LLM APIs
level: L1
kind: core
hours: 8–10
summary: Call cloud and local LLMs from Python, stream replies, count tokens and cost, handle rate limits, and pick a model on capability, cost and latency.
checked: 2026-10-16
---

## Why it matters
Chat apps hide the moving parts. An agent is code that calls a model API many times, so you need to be fluent with the API itself. That means knowing how a request is shaped, what comes back, what it costs, and what to do when the provider tells you to slow down.

This module makes you comfortable with the three big cloud providers and one local option. They differ in naming and small details, but the core ideas carry over. Once you have built one small wrapper with streaming, retries and cost logging, every later project in this guide can reuse it.

## What to learn
- **Provider SDKs**: OpenAI, Anthropic and Google each publish official Python and TypeScript SDKs that handle authentication, retries and typed responses. Use them instead of raw HTTP unless you have a specific reason.
- **The messages format**: A request carries a list of messages with roles, usually user and assistant, plus a system prompt with standing instructions. Most chat APIs are stateless, so you resend the whole conversation on every call. OpenAI's Responses API can also keep history for you on the server, but earlier turns are still billed as input tokens. Where the system prompt goes differs slightly by provider.
- **Key parameters**: Model name, maximum output tokens and temperature are the settings you change most. The response also tells you why generation stopped, for example a natural end or hitting the token limit.
- **Streaming**: With streaming on, the server sends the reply in small pieces as server-sent events (SSE). Users see text sooner, and long generations avoid HTTP timeouts.
- **Tokens and cost**: Every response reports input and output tokens. Cost is tokens multiplied by the per-million-token price, and output tokens usually cost several times more than input. Log both for every call.
- **Rate limits and retries**: Providers cap requests and tokens per minute and return HTTP 429 when you exceed them. Retry with exponential backoff and jitter, respect the Retry-After header, and check what your SDK already retries by default.
- **Choosing a model**: Larger models are more capable but slower and pricier. Prove the task works on a strong model first, then test whether a smaller, cheaper one still passes your checks.
- **Local models**: Ollama runs open-weight models on your own machine, with no per-token bill and no data leaving it. It also offers an OpenAI-compatible endpoint, so the same client code can talk to it.
- **Multimodal input**: Many current models accept images and PDFs alongside text. Images are converted to tokens based on their size, so resize them before sending.
- **API key safety**: Keep keys in environment variables or a secrets manager, never in code or Git. Never ship a key to a browser or mobile app; call the model from your own backend.

## Resources
### Start here
- [Developer quickstart](https://developers.openai.com/api/docs/quickstart) · OpenAI · Tutorial · Free · 30 min — Create a key, install the SDK and make a first Responses API call, then try images, files and tools.
- [Get started with Claude](https://platform.claude.com/docs/en/get-started) · Anthropic · Tutorial · Free · 30 min — Set your key as an environment variable and send a first Messages API request from Python or one of eight other languages.
- [Quickstart](https://docs.ollama.com/quickstart) · Ollama · Docs · Free · 30 min — Install Ollama, run an open model on your own laptop and send it a first request with no per-token cost.
### Go deeper
- [Gemini API: Getting started](https://ai.google.dev/gemini-api/docs/quickstart) · Google · Tutorial · Free · 30 min — Covers keys, streaming, multi-turn chat, images and JSON output; the Gemini API also has a free tier that suits learning.
- [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) · Anthropic · Docs · Free · 20 min — Multi-turn conversations, system prompts and image inputs, with a clear statement that you resend history on every call.
- [Streaming API responses](https://developers.openai.com/api/docs/guides/streaming-responses) · OpenAI · Docs · Free · 20 min — How to turn on streaming and handle the typed events that arrive, with examples in several languages.
- [Anthropic API fundamentals](https://github.com/anthropics/courses/blob/master/anthropic_api_fundamentals/README.md) · Anthropic · Course · Free · self-paced — Six notebooks on keys, the messages format, model parameters, streaming and vision; the repo is archived, so swap in a current model name.
- [Choosing the right model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) · Anthropic · Docs · Free · 15 min — A short framework for trading capability against speed and cost, then confirming the choice with your own tests.
- [Best practices for API key safety](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) · OpenAI · Article · Free · 10 min — Concrete rules for storing, rotating and limiting keys that apply to every provider.
### Reference
- [Rate limits](https://developers.openai.com/api/docs/guides/rate-limits) · OpenAI · Docs · Free · reference — Usage tiers, rate-limit headers and Python examples of retrying with exponential backoff.
- [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) · Anthropic · Docs · Free · reference — A free endpoint for counting input tokens before you send a request.
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) · Anthropic · Docs · Free · reference — Per-million-token prices plus batch and caching discounts; a good template for reading any provider's price sheet.
- [Vision](https://platform.claude.com/docs/en/build-with-claude/vision) · Anthropic · Docs · Free · reference — Image formats, size limits and the formula for how many tokens an image costs.
- [Artificial Analysis](https://artificialanalysis.ai/) · Artificial Analysis · Tool · Free · reference — Independent comparisons of models and API providers on quality, speed and price.

## Practice
1. **Hello, two ways.** Send the same question to one cloud model and one local Ollama model from a single Python script. Print the reply, input tokens, output tokens and time taken. Done when one command runs both and prints a side-by-side comparison.
2. **A tiny chat loop.** Build a terminal chat that keeps the message history in a list and streams each reply as it arrives. Add a system prompt such as "You are a patient cooking tutor". Done when the bot remembers your name three turns later and text appears word by word.
3. **Cost logger.** Wrap your API calls in one function that records model, tokens, latency and cost to a JSONL file, using prices copied from the provider's pricing page. Done when a short script answers "what did today's experiments cost?".
4. **Survive a 429.** Add retries with exponential backoff and jitter, capped at a few attempts. Test it by faking a 429 response in a unit test. Done when your code recovers, logs every retry and gives up cleanly after the cap.
5. **Model bake-off.** Summarise 10 support tickets into one line each on a large model, a small model and a local model. Done when you have a table of quality (your own 1 to 5 rating), latency and cost per ticket, plus a one-line recommendation.

## Checklist
- [ ] [Must ship] Make a working API call to at least one cloud provider and one local model.
- [ ] [Must ship] Store your API key in an environment variable and add `.env` to `.gitignore`.
- [ ] [Must ship] Build a reusable call wrapper that streams, retries on 429 and logs tokens and cost.
- [ ] [Recommended] Send an image, such as a receipt photo or a chart, and check the model's description.
- [ ] [Recommended] Run the model bake-off and write down which model you would pick and why.
- [ ] [Stretch] Point the OpenAI SDK at Ollama's OpenAI-compatible endpoint and run the same code unchanged.

## You're ready when
- You can explain why the model needs the full conversation on every request, and how it gets there.
- Your wrapper reports tokens, latency and cost for every call.
- Your code recovers from a rate-limit error without crashing.
- You can justify a model choice for a task with capability, cost and latency numbers you measured.
