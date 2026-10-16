---
title: Structured extraction service
level: L1
weeks: 1–1.5
summary: Build a service that turns messy text into validated JSON with an LLM, backed by a golden set, an accuracy report and a measured cost per document.
---

## The brief
You will build a small web service that takes messy text, such as a job posting, a pasted receipt or a customer support email, and returns clean, validated JSON. Pick one document type. The output should be something a spreadsheet, database or another program can use directly. For example, a job posting becomes title, company, location, salary range, seniority and required skills.

Imagine a small team that receives hundreds of these documents a week and copies fields out by hand. Before they trust your tool, they want to know how accurate it is, what each document costs and what happens when extraction fails. So your service ships with a golden test set, an accuracy report and cost numbers.

## What you'll practise
- [How LLMs work](#l1-how-llms-work): reasoning about tokens, temperature and why a model might invent a missing field.
- [Calling LLM APIs](#l1-llm-apis): a robust client with retries, token logging and cost per call.
- [Prompt engineering](#l1-prompt-engineering): a versioned extraction prompt with clear rules and examples.
- [Structured outputs and function calling basics](#l1-structured-outputs): Pydantic schemas, provider structured-output modes, validators and retry on validation error.
- [Your first evals](#l1-first-evals): a golden set, field-level accuracy and comparisons across prompt and model versions.

## Requirements
- [ ] [Must ship] Define a Pydantic schema for one document type with at least eight fields, including a nested list, an enum and optional fields that may be null.
- [ ] [Must ship] Extract with a provider structured-output mode or Instructor, validate with Pydantic, and retry with the validation error at most twice before returning a clear failure.
- [ ] [Must ship] Expose a `POST /extract` endpoint with FastAPI that returns the JSON plus metadata: model, prompt version, input and output tokens, cost and latency.
- [ ] [Must ship] Build a golden set of at least 25 hand-labelled documents, with at least five hard cases such as missing fields, odd formats or two items in one document.
- [ ] [Must ship] Write an eval script that reports field-level accuracy, the share of documents that are fully correct and the validation failure rate.
- [ ] [Must ship] Report average cost per document and median latency, computed from the token usage the API returns.
- [ ] [Must ship] Compare at least two prompt versions or two models in one results table, and state which you would ship and why.
- [ ] [Must ship] Keep API keys in environment variables and write a README that explains how to run the service and the eval.

## Stretch goals
- [ ] [Recommended] Add a business-rule validator, for example that receipt line items sum to the total, and measure how often it triggers a retry.
- [ ] [Recommended] Run the same golden set against a local model through Ollama and compare accuracy and cost.
- [ ] [Stretch] Port the eval to promptfoo and run it in GitHub Actions on every push.
- [ ] [Stretch] Add an LLM-graded check for one free-text field, such as a one-line summary, and measure its agreement with your labels.
- [ ] [Stretch] Accept photos of receipts as well as text, and compare accuracy and cost for images against text.

## Suggested stack
| Need | Suggested | Alternatives |
| --- | --- | --- |
| Language and packaging | Python 3.11+ with uv | venv and pip |
| Schemas and validation | Pydantic v2 | dataclasses with hand-written checks |
| Model access | A provider SDK on a free tier, such as Gemini | OpenAI or Anthropic SDKs, Instructor across providers, Ollama for local models |
| Web API | FastAPI | Flask, or a command-line tool with Typer |
| Evals | pytest with parametrized cases | promptfoo |
| Storage | JSONL files in the repo | SQLite |
| CI | GitHub Actions | GitLab CI |

## Build it step by step
1. **Pick and collect.** Choose one document type and gather 30 to 40 real examples from public sources or your own inbox. Remove personal details before you send any document to an API, not only before you commit. Free tiers, including Gemini's, may use your inputs to improve the provider's products, so use public or synthetic documents there, or a local model through Ollama for anything private.
2. **Design the schema.** Write the Pydantic model, decide which fields may be null, and use enums for any field with a fixed set of values. Add field descriptions, because they are sent to the model as part of the schema.
3. **Label the golden set.** Hand-label at least 25 documents into a JSONL file, one line per document with the input text and the expected JSON. Keep the remaining documents aside as unseen test data.
4. **Make a first extraction.** Write a prompt template, call the model in structured-output mode and validate the result. Log tokens, cost and latency for every call from the start.
5. **Score it.** Write the eval script. Use exact match for IDs, numbers and enums, use normalised match for free text, and print a per-field accuracy table.
6. **Improve and compare.** Read every failure, adjust the prompt or schema, and save the change as a new version. Rerun the eval on each version and on a second model.
7. **Wrap it in an API.** Add the FastAPI endpoint, return metadata with every response, and return a clear error body when extraction fails after retries.
8. **Write it up.** Fill in the README with the results table, cost per document, known failure cases and what you would try next.

## How to evaluate it
The numbers below are example targets. Adjust them to your document type and say why in your README.

| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Field-level accuracy on the golden set | 85% or more | 95% or more, with every remaining error explained |
| Valid output | Every response is valid JSON or a clear error | Over 98% valid on the first attempt, before retries |
| Cost per document | Measured and reported | Compared across two models, with a justified choice |
| Latency | Median reported | Median and 95th percentile reported for each model |
| Golden set | 25 documents including 5 hard cases | 50 or more documents, with hard cases tagged by type |
| Reproducibility | The eval runs with one command | The eval runs in CI on every push |

## Show your work
- A README with the schema, a sample input and output, the results table, cost per document and a short list of known failures.
- A 60 to 90 second demo video or GIF that sends a messy document to the endpoint and shows the JSON and the eval report.
- A short write-up on what moved accuracy most, such as a schema change, a new example or a model switch.
- A CV line with your real numbers, for example "Built an LLM extraction API with 94% field accuracy on a 40-document golden set at under one cent per document" (illustrative figures).

## Ideas to make it yours
- Recipes from cooking blogs into ingredients, quantities, steps and total time.
- Event announcements into calendar entries with date, time, venue and price.
- Research paper abstracts into title, task, dataset, method and headline result.
- Rental listings into rent, deposit, size, location and pet policy.
- Product reviews into rating, product aspects mentioned and sentiment for each aspect.

## Helpful resources
- [Receipt Data Extraction with GPT-4 Vision](https://python.useinstructor.com/examples/extracting_receipts/) · Instructor · Tutorial · Free · 20 min — A Pydantic receipt schema with a model validator that checks the line items add up to the total.
- [Extracting structured JSON using Claude and tool use](https://platform.claude.com/cookbook/tool-use-extracting-structured-json) · Anthropic · Tutorial · Free · 30 min — Five worked extraction and classification examples that use tool definitions as output schemas.
- [Classification with Claude](https://platform.claude.com/cookbook/capabilities-classification-guide) · Anthropic · Tutorial · Free · 1 h — A support-ticket classifier evaluated after each prompt change, including a promptfoo setup you can adapt for your report.
- [Cost Optimization on the Claude API](https://platform.claude.com/cookbook/cost-optimization-cost-optimization) · Anthropic · Tutorial · Free · 1 h — Shows how to turn the usage block of each response into cost per task and compare configurations on cost and pass rate.
- [Structured data extraction from unstructured content using LLM schemas](https://simonwillison.net/2025/Feb/28/llm-schemas/) · Simon Willison · Article · Free · 20 min — A command-line route to a quick extraction baseline before you write any service code.
