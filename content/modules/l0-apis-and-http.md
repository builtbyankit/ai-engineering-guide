---
title: Web APIs, HTTP and JSON
level: L0
kind: core
hours: 8–10
summary: Read API docs, call web APIs safely from Python with timeouts, retries and pagination, and build a small self-documenting API with FastAPI.
checked: 2026-10-16
---

## Why it matters

An agent is a program that talks to other programs over HTTP. Every model call is an HTTP request to a provider's API. Every tool that searches the web, reads a calendar or files a ticket is another API call. When an agent breaks, the cause often sits in this layer: a missing auth header, a 429 that nobody retried, or a list that stopped after the first page.

You will also serve APIs. Agents usually run behind an endpoint that a front end or another service calls. This module teaches enough HTTP to read any API's docs, call it correctly from Python and build a small, documented API with FastAPI. [Calling LLM APIs](#l1-llm-apis) applies the same ideas to model providers, and [Reliability, latency and cost](#l6-reliability-cost) takes them to production scale.

## What to learn

- **Requests and responses**: a client sends a method, a URL, headers and sometimes a body. The server answers with a status code, headers and a body, usually JSON.
- **Methods and REST conventions**: GET reads, POST creates, PUT and PATCH update, DELETE removes. REST APIs name resources with nouns in the URL, such as `/tickets/42`, and use the method to say what to do.
- **Status codes**: 2xx means success, 4xx means the client sent something wrong and 5xx means the server failed. Learn 200, 201, 400, 401, 403, 404, 422, 429, 500 and 503 by heart.
- **Headers and auth**: headers carry metadata such as `Content-Type` and `Authorization`. Most APIs expect a key as `Authorization: Bearer <key>` or in a custom header such as `x-api-key`.
- **Secrets in environment variables**: keep keys out of your code. Read them from environment variables, keep a local `.env` file out of git, and stop with a clear message when a key is missing.
- **Timeouts**: always set one, so a hung server cannot hang your program. Pick a value that fits the API instead of relying on a library default.
- **Rate limits and retries**: APIs cap how often you can call them and answer 429 when you exceed it. Retry only 429s, 5xx errors and network failures, waiting longer each time (exponential backoff) with some randomness (jitter), and respect a `Retry-After` header.
- **Pagination**: large lists arrive in pages. You follow a `next` link, a cursor or a page number until no results remain.
- **Building an API with FastAPI**: you declare routes with decorators and describe request and response bodies with Pydantic models. FastAPI validates input, returns 422 for bad data and generates interactive docs at `/docs` from an OpenAPI schema.

## Resources

### Start here

- [Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) · MDN · Docs · Free · 30 min — A clear picture of clients, servers, requests, responses and headers, with real message examples.
- [QuickStart](https://www.python-httpx.org/quickstart/) · HTTPX · Docs · Free · 45 min — Covers query parameters, JSON bodies, custom headers, status codes, `raise_for_status`, timeouts and exceptions in one page.
- [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/) · FastAPI · Tutorial · Free · 3–4 h — Work from First Steps through Response Model, Response Status Code and Handling Errors to build a validated, self-documenting API.

### Go deeper

- [Python and REST APIs: Interacting With Web Services](https://realpython.com/api-integration-in-python/) · Real Python · Article · Free · 30–45 min — Walks through REST constraints, methods, status codes and endpoint design, then consuming and building APIs in Python.
- [APIs for Beginners](https://www.freecodecamp.org/news/apis-for-beginners-full-course/) · freeCodeCamp · Video · Free · 2 h — A friendly video course that explores real APIs with Postman and code before building a small app on top of one.
- [Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) · AWS Architecture Blog · Article · Free · 15 min — Marc Brooker's classic simulation of why retries need random jitter as well as growing waits.
- [Using pagination in the REST API](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api) · GitHub · Docs · Free · 15 min — A concrete example of link-header pagination and how to loop through every page in a script.
- [Store config in the environment](https://12factor.net/config) · The Twelve-Factor App · Article · Free · 10 min — The short argument for keeping credentials and per-deploy settings in environment variables, with a useful litmus test.
- [HTTP authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Authentication) · MDN · Docs · Free · 20 min — Explains the `Authorization` header and the 401 challenge flow that API keys and bearer tokens build on.

### Reference

- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) · MDN · Docs · Free · reference — Every status code grouped by class with a one-line meaning, including 429 Too Many Requests.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) · IETF · Docs · Free · reference — The standard that defines methods, status codes and headers, for when two sources disagree.
- [Tenacity](https://tenacity.readthedocs.io/en/latest/) · Tenacity · Docs · Free · reference — A retry library with exponential backoff, jitter, stop conditions and asyncio support.
- [Settings Management](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/) · Pydantic · Docs · Free · reference — Load typed settings and API keys from environment variables and `.env` files with `BaseSettings`.

## Practice

1. **Read an API by hand.** Pick a free public API, such as a weather API or GitHub's public REST API. Call two endpoints with `curl -i` and note the status code, three response headers and the shape of the JSON. Done when you can explain every field you plan to use.
2. **Write a careful client.** Write a Python function that calls one endpoint with httpx, sets a timeout, raises on 4xx and 5xx, and returns a Pydantic model instead of a raw dict. Done when a wrong parameter produces a clear, specific error message.
3. **Retry with backoff.** Add retries for 429, 5xx and timeouts using exponential backoff with jitter, by hand or with Tenacity. Test it against a mocked response that fails twice and then succeeds. Done when the test passes and your logs show the waits growing.
4. **Follow pagination.** Fetch every page of a paginated endpoint, for example the issues of a small public GitHub repository, and stop cleanly at the end. Load a token from an environment variable if you hit the anonymous rate limit. Done when your count matches the total shown on the website.
5. **Build a small API.** With FastAPI, create a notes service with `POST /notes`, `GET /notes/{note_id}` and `GET /notes`, using Pydantic request and response models and in-memory storage. Done when every route works from `/docs`, unknown ids return 404 and invalid input returns 422.

## Checklist

- [ ] [Must ship] Call a public API from Python with a timeout and explicit status-code handling.
- [ ] [Must ship] Load an API key from an environment variable and keep `.env` out of git.
- [ ] [Must ship] Retry 429 and 5xx responses with exponential backoff and jitter.
- [ ] [Must ship] Build a FastAPI app with at least three routes and Pydantic request and response models.
- [ ] [Recommended] Follow pagination to fetch a complete list and handle the last page correctly.
- [ ] [Recommended] Respect the `Retry-After` header when the server sends one.
- [ ] [Stretch] Add a simple per-client rate limit to your FastAPI app that returns 429.

## You're ready when

- You can read an unfamiliar API's docs and name the method, URL, headers and body a call needs.
- You can explain what 401, 404, 422, 429 and 503 mean and which of them are worth retrying.
- Your client code contains no secrets and never waits forever on a slow server.
- Your FastAPI app validates input, returns correct status codes and documents itself at `/docs`.
