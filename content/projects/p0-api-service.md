---
title: A tested API service
level: L0
weeks: 1
summary: Build a small FastAPI service that wraps a free public API, with Pydantic models, offline tests, a Docker image and a GitHub Actions workflow.
---

## The brief

You will build a small web service that wraps a free public API and gives it a cleaner, safer interface. For example, a weather service could call a free forecast API and expose `GET /forecast?latitude=52.52&longitude=13.41`, returning a short typed summary instead of the raw upstream response. The service validates input, handles upstream failures gracefully and documents itself.

The users are a front-end developer, or a future agent, who need reliable data without learning the quirks of the upstream API. This is the shape of a real agent tool: a narrow, well-tested function behind an HTTP endpoint. You will reuse this skeleton in later levels when you serve models and agents.

## What you'll practise

- [Python for AI engineering](#l0-python-for-ai): Pydantic models, async httpx calls, custom exceptions and pytest.
- [Web APIs, HTTP and JSON](#l0-apis-and-http): timeouts, retries with backoff, status codes and FastAPI routes with automatic docs.
- [Git, the command line and Docker](#l0-dev-tooling): a clean repository, a Dockerfile, a CI workflow and a README.

## Requirements

- [ ] [Must ship] Expose at least two routes, such as `GET /health` and one data route, with Pydantic response models and validated query or path parameters.
- [ ] [Must ship] Call the upstream API with an async httpx client, a timeout, and retries with exponential backoff for 429, 5xx and network errors.
- [ ] [Must ship] Map upstream failures to clear responses, for example 502 when the upstream is down and 404 when it has no data, with no stack traces sent to clients.
- [ ] [Must ship] Read all configuration, including any API key, from environment variables, and commit a `.env.example` with placeholder values.
- [ ] [Must ship] Write at least eight pytest tests that run without network access by mocking the upstream API, covering success, bad input and upstream failure.
- [ ] [Must ship] Ship a Dockerfile and a `.dockerignore` so that `docker build` and `docker run` start the service.
- [ ] [Must ship] Add a GitHub Actions workflow that runs the tests on every push and pull request.
- [ ] [Must ship] Write a README with setup, run, test and Docker instructions plus an example request and response.

## Stretch goals

- [ ] [Recommended] Cache upstream responses in memory for a few minutes and add a test proving the second call skips the network.
- [ ] [Recommended] Add a linter and formatter such as Ruff to CI and type-check the code with mypy.
- [ ] [Stretch] Add a `compose.yaml` with a second service, such as Redis for the cache.
- [ ] [Stretch] Log one structured JSON line per request with a request id, status code and upstream latency.
- [ ] [Stretch] Build the image in CI and push it to a container registry on every merge to `main`.

## Suggested stack

| Need | Suggested | Alternatives |
| --- | --- | --- |
| Project and dependencies | uv | pip with venv, Poetry |
| Web framework | FastAPI | Flask, Litestar |
| HTTP client | httpx (async) | aiohttp, requests (sync only) |
| Retries | Tenacity | A hand-written backoff loop |
| Tests and HTTP mocking | pytest with RESPX | pytest with httpx's MockTransport, pytest-httpx |
| Upstream API | [Open-Meteo](https://open-meteo.com/) (free for non-commercial use, no key) | Any keyless API from the public-apis list |
| Container | Docker | Podman |
| CI | GitHub Actions | GitLab CI |

## Build it step by step

1. **Pick the upstream API.** Choose a free API that needs no key or only a free one, and call it with `curl` to learn its parameters and response shape. Save one real response as a JSON file to use as a test fixture.
2. **Scaffold the project.** Run `uv init`, add FastAPI, httpx, Tenacity, pytest and RESPX, then create a GitHub repository with a Python `.gitignore` and push the skeleton.
3. **Model the data.** Write Pydantic models for the parts of the upstream response you use and a separate model for your own response. Keep your response small, with field names that make sense to your users.
4. **Write the client.** Wrap the upstream call in one async function with a timeout, retries with backoff and conversion to your model. Raise your own exception type when the upstream fails so routes can map it to a status code.
5. **Add the routes.** Create the FastAPI app with `/health` and your data route, and try both by hand in `/docs`. Map your exception to 502 or 404 with a short, clear error message.
6. **Test without the network.** Use RESPX to replay your saved JSON, a 500, a timeout and a 429 followed by success. Test the routes end to end with FastAPI's `TestClient`.
7. **Containerize and automate.** Write the Dockerfile and `.dockerignore` and check that the container serves `/docs` on a published port. Add the GitHub Actions workflow and confirm a green check on a pull request.
8. **Document it.** Write the README, add the CI badge and record a short demo.

## How to evaluate it

| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Tests | 8 or more tests pass with the network disabled | 15 or more tests cover every error path and run in under 5 seconds |
| Error handling | Upstream failures return a 5xx with a message | Each failure type maps to a specific status code and clients never see a stack trace |
| Resilience | Retries 429 and 5xx with backoff | Also respects `Retry-After`, caps total wait time and has a test for each case |
| Reproducibility | A fresh clone runs by following the README | `docker run` and CI both work first time from a fresh clone |
| Configuration and secrets | No secrets anywhere in the repository | `.env.example` documents every variable and the app stops with a clear message when one is missing |
| API design | Routes return Pydantic models and appear in `/docs` | Clear names, example values in the docs and correct status codes on every route |

## Show your work

- A README with a one-paragraph description, the request flow as a short list, setup steps, an example `curl` call with its response and the CI badge.
- A 60-second screen recording or GIF showing `/docs`, a successful call and a handled upstream failure.
- A short write-up of 300 to 500 words on one design decision, such as which errors you retry and why.
- A CV line such as "Built a tested FastAPI service with async retries, Docker and GitHub Actions CI", linked to the repository.

## Ideas to make it yours

- A book lookup service that returns title, authors and year from a public book catalogue.
- A currency converter that caches daily exchange rates and rejects unknown currency codes.
- A public holidays service that answers whether a given date is a holiday in a given country.
- A recipe search service that filters results by ingredient and returns a compact list.
- Any keyless API from the public-apis list, with the smallest useful interface you can design on top.

## Helpful resources

- [Testing](https://fastapi.tiangolo.com/tutorial/testing/) · FastAPI · Docs · Free · 20 min — Shows how to test routes with `TestClient` and pytest, including headers, error responses and POST bodies.
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/) · FastAPI · Docs · Free · 45 min — A ready Dockerfile for FastAPI with advice on layer caching, the exec form of `CMD` and a uv variant.
- [Using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/) · Astral · Docs · Free · 20 min — Workflow examples that install uv, cache dependencies and run your tests with `uv run pytest`.
- [RESPX](https://lundberg.github.io/respx/) · lundberg · Docs · Free · reference — Mocks httpx requests through a pytest fixture so you can replay upstream responses and failures offline.
- [uv-docker-example](https://github.com/astral-sh/uv-docker-example) · Astral · Repo · Free · 30 min — A minimal FastAPI project packaged with uv, Docker and Compose that you can copy as a starting layout.
- [Public APIs](https://github.com/public-apis/public-apis) · public-apis · Repo · Free · reference — A large community-maintained list of free APIs to choose your upstream from.
