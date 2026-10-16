---
title: Python for AI engineering
level: L0
kind: core
hours: 12–15
summary: Set up a modern Python project, write typed code with Pydantic models, make concurrent API calls with asyncio and httpx, and test it all with pytest.
checked: 2026-10-16
---

## Why it matters

Almost every LLM SDK, agent framework and evaluation tool in this guide is Python first. Agent code is mostly glue. It reads files, calls web APIs, checks the shape of the data that comes back and recovers when something fails. The Python features in this module are the ones that make that glue reliable.

Two habits matter most. Type hints and Pydantic models describe the data you expect, so bad input or bad model output fails loudly at the boundary. Async code lets one program wait on many slow network calls at once, which is how agents call models and tools in parallel. The goal is a clean setup, readable code and tests you trust. That takes far less than mastering the whole language, and [Structured outputs](#l1-structured-outputs) in Level 1 builds directly on it.

## What to learn

- **Project setup with uv**: uv creates a project, a virtual environment and a lockfile, then runs your code with the right packages. A virtual environment keeps each project's packages separate; `venv` plus `pip` does the same job with more manual steps.
- **Everyday syntax**: f-strings build text, list and dict comprehensions transform collections, and keyword arguments make calls readable. Most agent code combines these three.
- **Type hints**: annotations such as `def score(text: str) -> float` say what a function takes and returns. Editors and checkers such as mypy use them to catch mistakes before you run anything.
- **Dataclasses and Pydantic models**: a dataclass is a lightweight class for holding data. A Pydantic model also validates and converts incoming data and turns it to and from JSON, which is why FastAPI and most LLM SDKs use it.
- **Exceptions**: raise specific errors, catch only the ones you can handle and let the rest surface. Agents fail in many small ways, so precise error handling saves hours of debugging.
- **Context managers**: the `with` statement opens a resource and guarantees it is closed, even after an error. Files, HTTP clients and database connections all work this way.
- **Files and JSON**: use `pathlib` to read and write files and the `json` module to convert between dicts and JSON text. JSON is the format that models, APIs and tools exchange.
- **async and await**: an `async def` function can pause while it waits on the network and let other work run. With `asyncio.gather` and an async client such as httpx, ten requests take about as long as the slowest one.
- **pytest basics**: tests are plain functions named `test_...` that use `assert`. Fixtures such as `tmp_path` provide setup, and `pytest.raises` checks that bad input fails the way you expect.

## Resources

### Start here

- [The Python Tutorial](https://docs.python.org/3/tutorial/) · Python Software Foundation · Docs · Free · 5–6 h — The official walkthrough of the language; chapters 3 to 9 cover comprehensions, f-strings, files and JSON, exceptions and classes, and chapter 12 explains virtual environments.
- [Working on projects](https://docs.astral.sh/uv/guides/projects/) · Astral · Docs · Free · 20 min — Shows `uv init`, `uv add` and `uv run`, and explains what `pyproject.toml`, `.venv` and `uv.lock` are for.
- [Models](https://pydantic.dev/docs/validation/latest/concepts/models/) · Pydantic · Docs · Free · 1 h — The core Pydantic v2 page on defining models, validation errors, nested models and converting to and from JSON.

### Go deeper

- [Python's asyncio: A Hands-On Walkthrough](https://realpython.com/async-io-python/) · Real Python · Article · Free · 40 min — Explains coroutines, the event loop and running tasks concurrently with runnable examples (a free Real Python account is needed to read it in full).
- [Get Started](https://docs.pytest.org/en/stable/getting-started.html) · pytest · Docs · Free · 20 min — Install pytest, write a first test, assert that an exception is raised and use a temporary directory fixture.
- [Python's with Statement: Manage External Resources Safely](https://realpython.com/python-with-statement/) · Real Python · Article · Free · 40 min — Covers how context managers work, `async with`, and how to write your own with a class or a generator function.
- [Working With JSON Data in Python](https://realpython.com/python-json/) · Real Python · Article · Free · 40 min — Reading and writing JSON files, converting Python types, and validating or pretty-printing JSON from the terminal.
- [Data Classes in Python](https://realpython.com/python-data-classes/) · Real Python · Article · Free · 25 min — An older but still accurate guide to defaults, immutability and comparison, useful before you reach for Pydantic.
- [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) · Harvard University · Course · Free · self-paced — Video lectures and problem sets on exceptions, unit tests, file I/O and classes; take it if the official tutorial feels too terse.

### Reference

- [Type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) · mypy · Docs · Free · reference — One page of annotation examples for collections, optional values, callables, classes and async functions.
- [Async Support](https://www.python-httpx.org/async/) · HTTPX · Docs · Free · reference — How to use `httpx.AsyncClient` with `async with` and `await`, the pattern behind concurrent API calls.
- [asyncio: Asynchronous I/O](https://docs.python.org/3/library/asyncio.html) · Python Software Foundation · Docs · Free · reference — The standard library docs for tasks, timeouts, queues and synchronization when tutorials stop short.

## Practice

1. **Set up a project.** Install uv, run `uv init recipes`, add `pydantic`, `httpx` and `pytest`, and commit `pyproject.toml` and `uv.lock`. Done when `uv run pytest` works in a fresh clone of the folder.
2. **Model a recipe.** Write a Pydantic `Recipe` model with a title, a list of ingredients, servings as a positive integer and an optional source URL. Load ten recipes from a JSON file, one deliberately broken, and save the valid ones to a new file. Done when the broken entry prints a readable validation error and the program carries on.
3. **Fetch concurrently.** Write an async function that requests 10 URLs from a free public API (for example 10 cities from a weather API) with `httpx.AsyncClient`. Time a sequential loop against `asyncio.gather`. Done when you print both timings and one failing URL does not crash the batch.
4. **Add a context manager.** Write a `Timer` context manager, as a class or with `contextlib.contextmanager`, and use it to time exercise 3. Done when `with Timer("fetch"):` prints elapsed milliseconds even if the block raises.
5. **Test it.** Write at least six pytest tests covering a valid recipe, invalid recipes, a JSON round trip using `tmp_path` and a `pytest.raises` check. Done when `uv run pytest` passes and breaking the model makes a test fail.

## Checklist

- [ ] [Must ship] Create a uv project with a committed lockfile that runs with `uv run`.
- [ ] [Must ship] Define a Pydantic model and handle its validation errors without crashing.
- [ ] [Must ship] Read and write JSON files using `pathlib` together with `json` or Pydantic's JSON methods.
- [ ] [Must ship] Write an async function that runs several httpx requests concurrently.
- [ ] [Must ship] Write at least six passing pytest tests.
- [ ] [Recommended] Add type hints to every function and run mypy or your editor's checker with no errors.
- [ ] [Stretch] Cap concurrent requests with `asyncio.Semaphore` and add a per-request timeout.

## You're ready when

- You can start a project with uv and explain what `pyproject.toml`, `uv.lock` and `.venv` each do.
- You can explain when you would use a dataclass and when a Pydantic model.
- Your async script fetches several URLs concurrently and survives one of them failing.
- Your tests run with one command and fail when you introduce a bug.
