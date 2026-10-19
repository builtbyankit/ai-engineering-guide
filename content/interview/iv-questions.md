---
title: Question bank
hours: 6–8
summary: About 40 common agentic AI interview questions with short model answers and a follow-up each, from LLM fundamentals to evaluation and operations.
checked: 2026-10-19
---

## How to use this page

Each question has a short model answer and a follow-up an interviewer might ask next. The answers show the shape of a strong reply. Don't memorise them. Answer out loud in about two minutes first, then compare, then answer the follow-up. Add an example from your own projects to every answer you can, because a real example is what makes an answer believable.

Where a question links to a module, that module covers the topic in depth.

## LLM fundamentals

### What is a token, and why does it matter?

A token is the unit a model reads and writes, often a word or part of a word. Prices, rate limits, context windows and latency are all counted in tokens. So the token count of your prompts, tool results and outputs drives cost and speed more than anything else. Code and non-English text often use more tokens per word. See [How LLMs work](#l1-how-llms-work).

**Follow-up:** Your agent's cost doubled after a change. Where do you look first?

### What do temperature and top-p do?

Temperature reshapes the probabilities before the next token is picked. Low values make output more predictable and high values make it more varied. Top-p keeps only the smallest set of likely tokens whose probabilities add up to p. For extraction or tool calls you usually want low temperature, and you still validate the output, because low temperature does not guarantee identical results.

**Follow-up:** Why can the same prompt at temperature 0 still give different answers?

### Why do models hallucinate, and what do you do about it?

Models produce fluent text whether or not it is true, and training often rewards a confident guess over "I don't know". You reduce the harm with system design: ground answers in retrieved sources, require citations, check that cited text supports the claim, allow and test refusals, and keep consequential facts in systems of record. See [Building a RAG pipeline](#l2-rag-pipeline).

**Follow-up:** How would you measure the hallucination rate of your assistant?

### What does a reasoning model do differently, and when is it worth it?

A reasoning model spends extra tokens thinking before it answers, which helps with multi-step planning, maths and code. The cost is more output tokens and slower replies, and the thinking tokens are billed. Use one where an eval shows a real quality gain, and try a lower effort setting first. In a tool loop, send its reasoning blocks back with each tool result. See [The agent loop](#l3-agent-loop).

**Follow-up:** How would you decide between a reasoning model and a smaller fast model for one step?

### What is an embedding, and how do you compare two of them?

An embedding is a vector that represents text so that similar meanings land close together. Cosine similarity compares direction, and on normalised vectors it equals the dot product. Changing the embedding model means re-embedding everything, because vectors from different models are not comparable. See [Embeddings and vector search](#l2-embeddings-vector-search).

**Follow-up:** How would you choose an embedding model for your own documents?

### When would you fine-tune instead of prompting or using RAG?

Prompting changes instructions, RAG supplies facts at query time and fine-tuning changes behaviour, such as format, style or a narrow skill. Try prompting and retrieval first. Fine-tune when evals show a gap they can't close, or when a small tuned model can replace an expensive one on a narrow, high-volume task. Fine-tuning is a poor way to add facts that change. See [Open models, fine-tuning and serving](#l6-open-models).

**Follow-up:** What would you need in place before starting a fine-tuning project?

### How does attention work, and why do long prompts cost more?

Each token builds a query, a key and a value. Attention compares a token's query with the keys of the tokens before it and uses the resulting weights to mix their values. Comparing every token with every earlier one makes processing the prompt grow faster than its length. During generation, the model stores past keys and values so each new token only attends to them. Long prompts therefore cost more compute, more memory and a slower first token.

**Follow-up:** Why can't you just send every document in a 1-million-token context instead of using retrieval?

### What is the KV cache, and why does it matter for serving?

The KV cache stores the keys and values of every token already processed, so the model doesn't recompute them for each new token. It grows with context length, the number of layers and the number of concurrent requests, and it can need more memory than the model weights. That limits how many requests a server can batch. Serving engines such as vLLM manage it in pages to waste less memory. See [Agent system design and capacity planning](#l6-system-design) for the formula.

**Follow-up:** Roughly how much KV cache memory do 8 concurrent 32,000-token requests need on a model you know?

### Why is time to first token different from total response time?

Generation has two phases. Prefill processes the whole prompt in parallel, so time to first token grows with prompt length. Decode then produces one token at a time, so total time grows with output length. Streaming makes a long answer feel faster, prompt caching shortens prefill, and shorter outputs cut decode time.

**Follow-up:** Your p95 time to first token doubled but output length didn't change. Where do you look?

### What is quantization, and what does it cost?

Quantization stores weights, and sometimes activations or the KV cache, in fewer bits, for example 8 or 4 instead of 16. It cuts memory and often speeds up serving, so a bigger model fits on smaller hardware. The cost is some quality loss that varies by model, method and task. Always rerun your own evals before and after quantizing.

**Follow-up:** A 4-bit model is half the cost and scores 2 points lower on your evals. Do you ship it?

### How do structured outputs guarantee valid JSON?

Providers that support strict schemas constrain decoding. At each step they block any token that would break the schema, so the output always parses and has the required fields. This guarantees the shape, not the truth of the values. You still validate business rules, handle refusals and truncation, and keep schemas within the subset the provider supports. See [Structured outputs](#l1-structured-outputs).

**Follow-up:** Why might forcing a strict schema make answers slightly worse, and how would you check?

### What is the difference between full fine-tuning, LoRA and preference tuning?

Full fine-tuning updates every weight, which is expensive and needs the most data and memory. LoRA freezes the model and trains small adapter matrices, which is far cheaper and easy to swap. Preference tuning, such as RLHF or DPO, trains on pairs of better and worse answers to shift style and behaviour. Reinforcement fine-tuning such as GRPO trains against a scoring function when code can check the answer.

**Follow-up:** You have 500 examples of the exact output format you want. Which method do you try first?

## Agents and tools

### What makes a system agentic, and how is it different from a workflow?

In a workflow, your code decides the sequence of steps. In an agent, the model chooses the next step based on what it has seen so far, usually in a loop of decide, call a tool, read the result. Many good systems mix the two. Code owns the lifecycle and policy, and the model handles the parts that need judgement. See [Workflows and agent design patterns](#l3-workflow-patterns).

**Follow-up:** Give an example from your own work of a step you moved from an agent to a workflow, or the reverse.

### When would you avoid using an agent?

When the steps are known in advance, mistakes are expensive or you cannot check the result. A model loop adds latency, cost, variation and a larger security surface. I would compare an agent with the simplest workflow on the same test cases and keep it only if it wins clearly on a metric that matters.

**Follow-up:** Your manager wants an agent for invoice processing. How do you respond?

### Walk me through a tool call.

You send tool definitions with the request. The model replies with a tool name and JSON arguments. Your code validates the arguments, runs the tool and sends the result back, matched to the call's ID. Then the model continues. The model never runs anything itself, so every check on identity and permissions belongs in your code. See [Tool calling in depth](#l3-tool-calling).

**Follow-up:** What do you return to the model when a tool fails?

### What makes a good tool definition?

A clear name, a description that says what it does, when to use it and when not to, and a strict schema with enums and required fields. Results should be small and useful, with stable IDs the model can use later. Errors should tell the model how to fix its call. Good tool design often helps more than a bigger model.

**Follow-up:** Your agent keeps picking the wrong one of two similar tools. What do you change?

### The model asks for three tool calls in one turn. What do you do?

Validate all three first. Run the independent read-only ones concurrently and return every result together, each matched to its call ID, including errors. Calls with side effects need more care, so run them in a safe order or ask for approval. Never drop a result, because many APIs reject a turn with a missing one.

**Follow-up:** One of the three calls writes data and fails. What happens to the others?

### How do you stop an agent from running forever or overspending?

Set limits in code: maximum steps, a token or cost budget, a wall-clock deadline and a check for repeated identical calls. Check the budget before every model call, warn the model when it is close, and record which limit stopped the run. When a limit fires, return the best partial answer instead of nothing.

**Follow-up:** How would you choose the step limit for a new agent?

### What is MCP, and what are the risks of third-party servers?

The Model Context Protocol is an open standard that lets any compatible app use a server's tools, resources and prompts, so you write an integration once. A third-party server runs with your permissions, and its tool descriptions go straight into the model's context. Risks include hidden instructions in descriptions, tools that change after you approve them and one server shadowing another's tools. See [Model Context Protocol](#l3-mcp).

**Follow-up:** How would you decide whether to allow a new MCP server in your company?

### When is a multi-agent design justified?

When one agent's context overflows, when parts of the work are truly independent and can run in parallel, or when sub-tasks need different tools or permissions. Multi-agent systems cost more tokens and can make conflicting hidden decisions. I would start with one agent, measure where it fails and add agents only where the numbers justify it. See [Multi-agent systems](#l4-multi-agent).

**Follow-up:** What do you put in the task you hand to a worker agent?

## State, durability and approvals

### What is the difference between context, run state and memory?

Context is what the model sees on this call. Run state is the durable record of this task, such as steps taken, tool results and status, which lets you resume. Memory is information kept across tasks, such as a user preference. Only run state and systems of record are authoritative. Context is a view, and memory needs rules for scope, consent and deletion. See [Memory and context engineering](#l3-memory-context).

**Follow-up:** What should never be stored as long-term memory?

### How do you make retries safe for tools that change things?

Give every write an idempotency key, so a repeated request returns the first result. If a call times out after it was sent, its outcome is unknown, so query the downstream system with the same key before deciding. Never retry an unknown write with a new key. Retry transient failures at one layer only, with capped backoff and jitter.

**Follow-up:** The downstream system has no idempotency support. What now?

### The process crashes halfway through a long run. How do you resume without repeating work?

Record each model and tool call as a durable step before moving on, then replay from the log after a restart and skip finished steps. Give runs a lease with a fencing token so only one worker owns a run, and a stale worker cannot write after takeover. Writes still need idempotency keys, because a crash can land between sending a request and recording its result. See [Deploying agent applications](#l6-deployment).

**Follow-up:** Would you use a workflow engine, a graph framework's checkpointer or your own log?

### How would you design human approval for a refund?

The model drafts a proposal, and code checks eligibility. The reviewer sees the exact action, its evidence and its effect. The approval binds to a digest of that exact proposal, so any change makes it stale. The decision and an outbox row are written in one transaction, and a worker sends the refund with a stable key. Every step goes in an audit log. See [Human in the loop](#l4-human-in-the-loop).

**Follow-up:** Reviewers are approving 95% of requests without reading them. What do you change?

## Retrieval and RAG

### Walk me through a RAG pipeline from documents to an answer.

Parse documents into clean text that keeps headings and tables. Chunk by structure, embed the chunks and store them with source, version and access metadata. At query time, run keyword and vector search, merge the results, rerank them and check access. Then build a prompt with a few labelled chunks and ask for an answer with citations, or a refusal when the context doesn't support one. See [Building a RAG pipeline](#l2-rag-pipeline).

**Follow-up:** Which step would you check first when answers get worse?

### How do you choose a chunk size?

Start with structure-aware chunks of a few hundred tokens with a small overlap, then measure. Test two or three sizes on a labelled question set and compare how often the right chunk lands in the top results. Smaller chunks match precisely but lose context, and parent-child retrieval can give you both.

**Follow-up:** Your documents are mostly tables. What changes?

### Why use hybrid search and a reranker?

Vector search finds paraphrases but misses exact terms such as error codes and product names. Keyword search such as BM25 catches those. Merging the two lists with reciprocal rank fusion is often the cheapest big gain. A cross-encoder reranker then reads each query and candidate together and reorders a wide set more accurately, at extra latency. See [Better retrieval](#l2-advanced-retrieval).

**Follow-up:** How do you decide whether the reranker is worth its latency?

### How do you evaluate a RAG system?

Measure retrieval and generation separately. For retrieval, use recall@k and MRR on questions labelled with their source chunks. For answers, measure faithfulness to the retrieved text, relevance and correct refusals on questions the documents can't answer. Then read the failures, tag their causes and fix the biggest group first. See [Evaluating RAG](#l2-rag-evaluation).

**Follow-up:** You only have 40 labelled questions. How confident can you be in a 5-point improvement?

### A document is deleted, or someone loses access to it. What happens?

The index is derived data, so deletions and permission changes must reach it, and the query path must not rely on it alone. Check current access against the source system at query time. Remove the document's chunks and any cached answers that quote it. Build new index versions beside the live one so a rebuild never restores old access.

**Follow-up:** How quickly must a permission change take effect, and how would you test it?

## Context, memory and security

### What goes into the model's context on each call?

The smallest set of useful tokens: stable instructions and tool definitions first, then trusted task metadata, the current request, the latest relevant tool results with their sources, a short summary of earlier steps and room for the output. Keep the stable part first so prompt caching works. Long contexts get less reliable, so more is not better.

**Follow-up:** How would you notice that the context is too large?

### How do you defend an agent against prompt injection?

Assume any text the agent reads can carry instructions, and no filter blocks all of them. So design for it. Check whether the agent has private data, untrusted input and a way to send data out (the lethal trifecta), and remove or gate one of the three. Use least-privilege tools, approvals for risky actions and patterns that stop untrusted text from choosing the next action. Then red-team it. See [Security and guardrails](#l5-security).

**Follow-up:** Your agent reads emails and can send emails. What do you change?

### What is prompt caching, and what breaks it?

The provider reuses the processed prefix of a prompt across calls and charges less for cached input tokens. It pays off when a long stable prefix, such as instructions, tool definitions or reference documents, repeats across many calls. Anything that changes early in the prompt, such as a timestamp, a reordered tool list or user data placed before the stable part, breaks the cache. See [Reliability, latency and cost](#l6-reliability-cost).

**Follow-up:** Your cache hit rate is 10%. How do you investigate?

### The context keeps growing during a long run. What do you do?

Clear bulky old tool results, keep recent turns intact and summarise earlier work into a short note that points to the full records. Store important facts outside the context and fetch them again when needed. Isolate sub-tasks in sub-agents with their own clean context. Before any write, re-read the authoritative data instead of trusting the summary.

**Follow-up:** How would you test that compaction didn't drop something important?

## Evaluation and operations

### How would you build an eval program for a new agent?

Start by reading 50 to 100 real traces and noting the first failure in each. Group the notes into categories and count them. Write code checks for what code can detect, and an LLM judge only for the rest. Keep a versioned dataset with a holdout set, run it on every change and block regressions in CI. See [Evals in depth](#l5-evals-in-depth).

**Follow-up:** What does a 95% offline pass rate tell you, and what doesn't it?

### How do you know an LLM judge is right?

Label a set of outputs yourself, split them into tuning and test sets, and tune the judge on the tuning set only. Report its true positive and true negative rates on the test set, because overall agreement hides problems when failures are rare. Give each judge one narrow criterion and a pass or fail answer.

**Follow-up:** Your judge agrees with you 90% of the time. Is that good enough?

### What is the difference between pass@k and pass^k?

Pass@k is the chance that at least one of k attempts succeeds, so it rises as k grows. Pass^k is the chance that all k attempts succeed, so it falls as k grows. Users of a production agent experience something closer to pass^k, because they need it to work every time.

**Follow-up:** Your agent scores 90% pass@1. Roughly what is pass^3 if attempts are independent?

### What would you trace in production?

One trace per run, with spans for each model call, tool call and retrieval step. Record model, prompt version, tokens, cost, latency, status and stop reason. Attach user feedback and automated check results to the trace. Mask personal data before export and set a retention period. Traces feed both debugging and the next round of evals. See [Observability and tracing](#l5-observability).

**Follow-up:** A user says the agent gave a wrong answer yesterday. How do you find out why?

### How would you cut cost and latency without losing quality?

Measure cost and latency per completed task first, split by step, so you know where the money goes. Then try prompt caching, routing easy steps to a smaller model, trimming tool results, batching offline work and running independent calls in parallel. Keep each change only if the eval score holds.

**Follow-up:** Which of these would you try first, and why?

### The model provider is down for an hour. What happens?

Calls time out, retries back off and the gateway fails over to a backup model if one has passed the same evals. Read-only cases a fixed workflow can handle keep working. Writes that were already sent stay in an unknown state until you reconcile them, never retried through another provider under a new key. Users get a clear message and, where needed, a human handoff.

**Follow-up:** Why can't you just switch providers for every request?

### How do you roll out a new prompt or model safely?

Version prompts and models, and tag every trace with the version. Run the eval suite in CI and block merges that lower the score. Then send a small share of traffic to the new version, compare quality, cost and errors with the current one, and promote or roll back. Keep a kill switch.

**Follow-up:** The canary looks better on cost but slightly worse on one eval slice. What do you do?

## Checklist

- [ ] [Must ship] Answer ten questions across at least four sections out loud in two minutes each, before reading the model answer.
- [ ] [Must ship] Answer the follow-up for each of those ten questions and write down what changed in your answer.
- [ ] [Must ship] Add an example from your own projects to at least five answers.
- [ ] [Recommended] Work through every section once, marking the questions you couldn't answer confidently.
- [ ] [Recommended] Re-answer your marked questions a week later without notes.
- [ ] [Stretch] Write five new questions from a job description you are targeting, with your own model answers.

## Resources

- [Agentic AI Interview Preparation](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-interview-preparation.md) · Agentic AI Mastery · Article · Free · 45 min — A second set of senior-level questions and model answers with an answer structure, an interviewer scorecard and three system design prompts.
- [Interview Workbook: Explain, Defend, Build](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-interview-workbook.md) · Agentic AI Mastery · Tutorial · Free · 1 h — A follow-up question and an expected artifact for every core answer, so you can practise defending a reply under pressure.
- [Numerical Workbook: LLMs, Retrieval and Serving](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-numerical-workbook.md) · Agentic AI Mastery · Tutorial · Free · 1 h — Worked calculations for token budgets, attention, similarity, BM25 and rank fusion, ranking metrics, LoRA and KV cache memory.
- [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) · Hamel Husain and Shreya Shankar · Article · Free · 2–3 h — A long FAQ on error analysis, judges, binary scores and agent evals, the source of many evaluation questions in interviews.
- [A Visual Guide to Quantization](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization) · Maarten Grootendorst · Article · Free · 45 min — Diagram-led explanations of number formats, post-training quantization, GPTQ and GGUF, enough for any quantization question.
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) · Rafailov et al. · Paper · Free · 1 h — The DPO paper, which tunes a model on preference pairs without a separate reward model, a common follow-up to RLHF questions.
- [Introduction to Machine Learning Interviews](https://huyenchip.com/ml-interviews-book/) · Chip Huyen · Book · Free · self-paced — A 2021 book with over 200 machine learning knowledge questions, useful when a loop includes a classic ML fundamentals round.
