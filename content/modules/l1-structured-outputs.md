---
title: Structured outputs and function calling basics
level: L1
kind: core
hours: 6–8
summary: Get reliable, validated JSON from any LLM using JSON Schema, provider structured-output modes, Pydantic and Instructor, and use it for extraction and classification.
checked: 2026-10-16
---

## Why it matters
Code cannot use a paragraph. When your program needs a name, a date and a list of line items, text that is usually JSON will eventually break your pipeline. Agents depend on this too, because every tool call is the model producing structured arguments that your code must parse.

Providers now offer modes that constrain output to a schema you supply, and libraries like Instructor add validation and automatic retries. With Pydantic models on top, you get typed Python objects you can trust, or a clear error you can handle. This module teaches that toolkit and the two jobs it powers most often: extraction and classification. [Tool calling in depth](#l3-tool-calling) builds on it in Level 3.

## What to learn
- **JSON Schema**: A standard way to describe the shape of JSON, including types, required fields, enums, arrays and nested objects. Providers accept it to define what the model must return.
- **Pydantic models**: Python classes with typed fields that validate data and can generate JSON Schema for you. One model serves as both the schema you send and the validator you run on the reply.
- **Structured-output modes**: OpenAI, Anthropic, Gemini and Ollama can constrain generation so the reply matches your schema. This is stronger than the older JSON mode, which guaranteed valid JSON but not your fields.
- **Validation beyond shape**: A schema guarantees structure, and says nothing about truth. Add validators for business rules, such as line items summing to the total or a date not being in the future.
- **Retry on validation error**: When validation fails, send the error message back to the model and ask it to fix the output. Always cap the number of retries and log what failed.
- **Instructor**: A library that wraps many providers and returns Pydantic objects, with validation, automatic re-asking and streaming of partial results. Use a provider's native mode when you work with one provider, and Instructor when you want one interface across several.
- **Function calling as structured output**: Tool calling is the model filling in a JSON argument object for a function you described. You can define a tool only to get structured data, without ever running a function.
- **Extraction and classification**: Extraction pulls fields out of messy text, and classification picks labels from a fixed set. Use enums for labels, allow null for missing fields, and never force the model to invent a value.
- **Failure modes**: Refusals, output cut off at the token limit, and schemas beyond a provider's supported subset still happen. Check the stop reason and handle each case explicitly.

## Resources
### Start here
- [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs) · OpenAI · Docs · Free · 45 min — Defines output schemas with Pydantic, explains how Structured Outputs differs from JSON mode, and shows how to detect refusals.
- [Instructor](https://python.useinstructor.com/) · Jason Liu · Docs · Free · 1 h — A widely used library for structured extraction: define a Pydantic model and get validated objects back from 15+ providers.
- [Getting Structured LLM Output](https://www.deeplearning.ai/short-courses/getting-structured-llm-output/) · DeepLearning.AI · Course · Free tier · 1.5 h — Compares provider APIs, re-prompting with Instructor and constrained decoding with Outlines across seven short lessons with code.
### Go deeper
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) · Anthropic · Docs · Free · 30 min — Claude's JSON outputs and strict tool use, with a Pydantic parse helper and a clear list of schema limitations.
- [Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output) · Google · Docs · Free · 30 min — Gemini's schema-constrained JSON with Pydantic examples for extraction and classification, plus the supported schema subset.
- [Validation and Reasking](https://python.useinstructor.com/concepts/reask_validation/) · Instructor · Docs · Free · 30 min — How Pydantic validators and automatic re-asking turn a failed parse into a corrected answer.
- [Pydantic for LLM Workflows](https://www.deeplearning.ai/short-courses/pydantic-for-llm-workflows/) · DeepLearning.AI · Course · Free tier · 2 h — Validating model responses and user input with Pydantic, then combining structured output with tool calling.
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling) · OpenAI · Docs · Free · 45 min — How tools are described with JSON Schema and how strict mode makes the model's arguments match it.
- [Structured data extraction from unstructured content using LLM schemas](https://simonwillison.net/2025/Feb/28/llm-schemas/) · Simon Willison · Article · Free · 20 min — Schema-based extraction from the command line with results stored in SQLite, a fast way to prototype.
### Reference
- [Creating your first schema](https://json-schema.org/learn/getting-started-step-by-step) · JSON Schema · Tutorial · Free · 30 min — The official step-by-step introduction to types, required fields, arrays and nested objects.
- [Models](https://pydantic.dev/docs/validation/latest/concepts/models/) · Pydantic · Docs · Free · reference — Defining models and nested models, and validating straight from JSON strings.
- [Validators](https://pydantic.dev/docs/validation/latest/concepts/validators/) · Pydantic · Docs · Free · reference — Field and model validators for business rules that a schema alone cannot express.
- [Structured Outputs](https://docs.ollama.com/capabilities/structured-outputs) · Ollama · Docs · Free · reference — Schema-constrained JSON from local models, with Pydantic examples in Python.
- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · Anthropic · Docs · Free · reference — How tool definitions, tool calls and tool results fit together, as a bridge to Level 3.

## Practice
1. **Schema first.** Write a Pydantic model for a recipe with title, servings, total time in minutes, difficulty (easy, medium or hard), a list of ingredients (name, quantity, unit) and a list of steps. Print its JSON Schema. Done when the schema has nested objects, an optional field and an enum.
2. **Three ways to JSON.** Extract that recipe from five messy blog posts using a prompt that only asks for JSON, then a provider structured-output mode, then Instructor. Done when you have a table of parse failures and validation failures for each method.
3. **Validate and retry.** Add a model validator to an invoice schema that checks line items sum to the total. Feed it invoices with deliberate typos. Done when your code retries with the error message, stops after a fixed number of attempts and logs every failure.
4. **Classify with enums.** Label 30 support emails by category (billing, bug, how-to, account, other) and urgency (low, medium, high) using enum fields. Done when every output parses and you have measured accuracy against your own labels.
5. **Tool call as output.** Define a single `save_contact` tool and force the model to call it to extract contact details from 10 email signatures. Done when you can explain how this differs from a structured-output mode and when you would pick each.

## Checklist
- [ ] [Must ship] Write a Pydantic model with nested objects, enums and optional fields for one real document type.
- [ ] [Must ship] Extract data with a provider structured-output mode and validate it with Pydantic.
- [ ] [Must ship] Add a capped retry that feeds validation errors back to the model.
- [ ] [Recommended] Compare plain prompting, a structured-output mode and Instructor on the same inputs.
- [ ] [Recommended] Build an enum-based classifier and measure its accuracy on 30 labelled examples.
- [ ] [Stretch] Run the same extraction on a local model through Ollama and compare failure rates.

## You're ready when
- You can explain the difference between JSON mode, schema-constrained output and validation.
- Your extraction code returns a typed object or a clear, logged error, never a half-parsed dictionary.
- You can show a validation error leading to a corrected answer on retry.
- You can describe how tool calling and structured outputs relate.
