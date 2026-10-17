---
title: Tool calling in depth
level: L3
kind: core
hours: 8
summary: Design, call and debug tools across major LLM APIs, with clear schemas, parallel calls, useful errors, bounded results and safe handling of side effects.
checked: 2026-10-16
---

## Why it matters
Tools are how a model reads live data and changes things in the world, such as searching the web, querying a database or sending an email. In [Structured outputs and function calling basics](#l1-structured-outputs) you saw that a tool call is structured output your code acts on. This module covers what goes wrong once tools carry real weight.

Most agent failures trace back to tools. A vague description makes the model pick the wrong tool. A huge result (say, 50,000 tokens of raw HTML) floods the context window. A retried "send invoice" call bills a customer twice. A web page tells the model to call a tool with an attacker's arguments. Good tool design prevents all four, and it is usually cheaper than moving to a bigger model.

## What to learn
- **The round trip**: You send tool definitions with your request. The model replies with a tool call (a name plus JSON arguments), your code runs it, and you send the result back so the model can continue. The model never executes anything itself.
- **Provider differences**: Anthropic, OpenAI and Gemini all define a tool with a name, a description and a JSON Schema for its parameters. They differ in field names, in how results are linked to calls by ID, and in which server-side tools they run for you, such as web search.
- **Names and descriptions**: The description is the tool's prompt. Say what the tool does, when to use it and when not to, what each parameter means and what it returns. Namespace related tools (for example `notes_search` and `notes_create`) so the model can tell them apart.
- **Schemas that constrain**: Use enums, required fields, formats and unambiguous names such as `user_id` instead of `user`. Strict or validated modes keep arguments on schema, and Pydantic validation in your code catches the rest.
- **Tool choice and parallel calls**: Most APIs let you allow, force or forbid tool calls, with support varying by model. Models can also request several independent calls in one turn. Run safe ones concurrently, then return every result together, each matched to its call ID.
- **Errors as feedback**: When a tool fails, return an error result with a message the model can act on, such as "date must be YYYY-MM-DD" or "rate limited, retry in 60 s". Models often correct themselves from a good error. A stack trace or a bare "failed" wastes a turn.
- **Result size**: Everything a tool returns enters the context window and costs tokens. Paginate, filter, truncate with a note saying so, and return stable IDs the model can use to fetch details later.
- **Idempotency**: A tool with side effects may run twice after a network retry or a confused model. Give writes an idempotency key, check whether the action already happened, and prefer designs where repeating a call is harmless. If a write times out after it was sent, its outcome is unknown, so check its status with the same key before you try again.
- **Security of tool inputs**: Arguments come from a model that may have read malicious text. Validate them like user input, allowlist paths and domains, use parameterised queries, never build shell commands from strings, and give each tool the least privilege it needs. [Security and guardrails](#l5-security) goes further.

## Resources
### Start here
- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · Anthropic · Docs · Free · 30 min — A clear walkthrough of the tool_use and tool_result round trip, plus the split between client tools you run and server tools Anthropic runs.
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling) · OpenAI · Docs · Free · 45 min — The same loop in OpenAI's API, with strict schemas, several calls per response and practical advice on keeping tool sets small.
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) · Anthropic · Article · Free · 30 min — The best single guide to tool naming, namespacing, response size and evaluating tools with realistic multi-step tasks.
### Go deeper
- [Function calling with the Gemini API](https://ai.google.dev/gemini-api/docs/function-calling) · Google · Docs · Free · 45 min — Covers parallel and compositional (chained) calls and the calling modes, so you can see which ideas are universal and which are provider-specific.
- [Tool use course](https://github.com/anthropics/courses/blob/master/tool_use/README.md) · Anthropic · Course · Free · 3–4 h — Six notebooks that build from one simple tool to a multi-tool chatbot, including tool choice and forcing JSON output.
- [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) · Anthropic · Article · Free · 20 min — Explains why large tool sets eat context and how tool search, code-driven tool calls and input examples help, with measured gains.
- [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · Simon Willison · Article · Free · 15 min — Names the mix of private data, untrusted content and an outbound channel that turns tool calling into a data-leak risk.
### Reference
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) · Anthropic · Docs · Free · reference — Exact rules for formatting results, signalling failures with is_error and ordering results so the API accepts them.
- [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use) · Anthropic · Docs · Free · reference — How to run several calls from one turn and return their results, including what to send for calls you skipped.
- [JSON Schema reference](https://json-schema.org/understanding-json-schema) · JSON Schema · Docs · Free · reference — The keywords (types, enums, required fields, composition) that every provider's parameter schema is built from.
- [Idempotent requests](https://docs.stripe.com/api/idempotent_requests) · Stripe · Docs · Free · reference — A well-documented real-world idempotency key design you can copy for tools with side effects.
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard) · UC Berkeley · Tool · Free · reference — Compares how accurately models call functions, including multi-turn and agentic tasks, alongside cost and latency.

## Practice
1. **Same tool, two providers.** Define a `convert_currency` or `get_weather` tool over a free public API and wire it up with two providers' SDKs (or one SDK plus a local model in Ollama). Done when both answer the same question correctly using the tool and you have listed three differences in request and response shapes.
2. **Description A/B test.** Build a small recipe box with three similar tools (`search_recipes`, `get_recipe`, `list_recipes_by_tag`). Write 15 requests and the tool you expect for each. Done when you have measured tool-selection accuracy with terse descriptions and again with rewritten ones.
3. **Errors the model can use.** Make a tool that validates its input, for example a date range for a public holidays API, and returns specific error messages. Send five bad requests. Done when the model fixes its own call in at least four of them and your log shows each retry.
4. **Tame a big result.** Write a `search_tickets` tool over a CSV of 1,000 fake support tickets. Add pagination, a `fields` parameter and a cap of about 2,000 tokens per result (example figure) with a note when output is truncated. Done when token usage per call stays under the cap.
5. **Safe side effects.** Build a `create_invoice` tool that writes to SQLite and accepts an idempotency key. Send the same call twice to simulate a retry. Done when only one invoice exists and the second call returns the original result.

## Checklist
- [ ] [Must ship] Implement the tool round trip by hand, without SDK helpers, in two provider APIs.
- [ ] [Must ship] Write tool descriptions that state purpose, when to use, parameters and return shape, and validate arguments with Pydantic.
- [ ] [Must ship] Return actionable error results and handle several tool calls in one response.
- [ ] [Recommended] Cap and paginate tool results, and log tokens per tool call.
- [ ] [Recommended] Add idempotency keys to every tool that writes data.
- [ ] [Stretch] Measure tool-selection accuracy on a 15-request test set before and after rewriting descriptions.

## You're ready when
- You can explain the tool call round trip and name what differs between two providers.
- Your tools reject bad arguments with messages the model uses to fix its next call.
- Your code handles a response with several tool calls and returns all results correctly.
- You can say which of your tools have side effects and how a repeated call is made harmless.
