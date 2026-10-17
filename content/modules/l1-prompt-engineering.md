---
title: Prompt engineering
level: L1
kind: core
hours: 8–10
summary: Write clear, structured prompts with roles, examples and delimiters, chain them for harder tasks, and manage prompts as versioned, tested code.
checked: 2026-10-16
---

## Why it matters
The prompt is the main way you program a model. A vague prompt gives vague, inconsistent output, and in an agent that inconsistency compounds over many steps. Good prompting is mostly clear writing. Say what you want, give the context a smart newcomer would need, and show an example.

Prompt engineering also has an engineering half. Prompts change as you learn, models change under you, and a small edit can fix one case and break three others. So you store prompts in files, version them, and run them against test cases before you ship. This module covers both halves, using the official guides from the three main providers.

## What to learn
- **Clear instructions**: State the task, the audience, the output format and the constraints explicitly. Explain why a rule exists, because models follow a rule more reliably when they know its purpose.
- **System prompts and roles**: The system prompt holds standing instructions and a role, such as "You are a careful bookkeeping assistant". Keep stable rules there and put the per-request data in user messages.
- **Few-shot examples**: A few worked input and output examples, often three to five, teach format and edge cases faster than paragraphs of rules. Make them varied and close to real inputs, or the model will copy their quirks.
- **Delimiters and XML tags**: Wrap documents, examples and instructions in clear markers such as `<document>` tags or Markdown headings. This stops the model mixing up your data and your instructions.
- **Letting the model think**: Asking for step-by-step reasoning before the answer (chain of thought) helps on multi-step tasks. Reasoning models do this internally, so with them you mostly describe the goal and constraints.
- **Prompt templates**: Separate the fixed prompt text from the variables you fill in per request. Keep templates in files under version control, and log the template version with every output.
- **Prompt chaining**: Split a big task into steps, such as extract, then check, then write, where each output feeds the next step. Each step is easier to get right and to debug.
- **Common mistakes**: Watch for contradictory rules, missing context, examples that all look alike, too many tasks in one prompt, and judging a prompt on one lucky output.
- **Prompts as code**: Treat a prompt change like a code change. Run it against a fixed set of test inputs and compare with the previous version before you merge it.

## Resources
### Start here
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) · Anthropic · Docs · Free · 1 h — Anthropic's living reference on clarity, context, examples, XML structure, roles, thinking and chaining; most of it transfers to other models.
- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) · OpenAI · Docs · Free · 45 min — OpenAI's guide to message roles, Markdown and XML formatting, few-shot examples, keeping prompts in code and prompting reasoning models.
- [Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) · Google · Docs · Free · 45 min — Gemini's guide to instructions, few-shot examples, breaking prompts into chains and tuning sampling parameters.
### Go deeper
- [Prompting Fundamentals and How to Apply them Effectively](https://eugeneyan.com/writing/prompting/) · Eugene Yan · Article · Free · 40 min — A practitioner's tour of roles, XML structure, n-shot examples, chain of thought and prompt splitting, plus popular tricks that barely help.
- [Best practices for prompt engineering for 2026](https://www.claude.com/blog/best-practices-for-prompt-engineering) · Anthropic · Article · Free · 20 min — A late-2025 overview of core and advanced techniques, common mistakes and how to choose which technique to reach for.
- [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) · Lilian Weng · Article · Free · 1 h — A research survey of zero-shot, few-shot, chain-of-thought and self-consistency prompting, with links to the original papers.
- [Classification with Claude](https://platform.claude.com/cookbook/capabilities-classification-guide) · Anthropic · Tutorial · Free · 1 h — Improves a support-ticket classifier step by step and measures accuracy after each prompt change, which is prompts-as-code in practice.
- [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) · DeepLearning.AI · Course · Free tier · 1.5–2 h — Isa Fulford and Andrew Ng teach two core prompting principles through summarising, inferring, transforming and chatbot examples in code; recorded in 2023, so swap in a current model name when you run it.
- [Prompt engineering interactive tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) · Anthropic · Course · Free · self-paced — Nine chapters of notebook exercises, from basic structure to avoiding hallucinations; written for older models, so pair it with the best-practices page.
### Reference
- [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) · Anthropic · Docs · Free · reference — Lists what to have before you start (success criteria, tests, a first draft) and links a prompt generator for first drafts.
- [Prompt Engineering Guide](https://www.promptingguide.ai/) · DAIR.AI · Docs · Free · reference — A broad catalogue of prompting techniques with short examples and links to the papers behind them.
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) · Wei et al. · Paper · Free · 1 h — The 2022 paper showing that worked reasoning examples improve multi-step problem solving.

## Practice
1. **Fix a bad prompt.** Start from "Summarise this support ticket." Rewrite it with a role, the audience, a length limit, an output format and one example. Run both versions on 10 real or invented tickets. Done when you can point to specific, repeatable differences in the outputs.
2. **Few-shot a classifier.** Write a prompt that labels recipe descriptions as breakfast, main, dessert or snack. Compare zero, two and five examples on 30 recipes you labelled yourself. Done when you have an accuracy number for each version.
3. **Chain it.** Turn "write a product FAQ from these 20 customer reviews" into three steps: extract questions, group duplicates, write answers. Done when each step's output is saved to a file you can inspect and the final FAQ beats a single-prompt attempt.
4. **Version your prompts.** Move the prompts from exercises 1 to 3 into template files, for example `prompts/ticket_summary_v2.txt`, load them in code and log the version with each output. Done when changing a prompt never requires editing Python.
5. **Cross-model check.** Run your best classifier prompt on two providers. Done when you have noted at least one place where the same prompt behaves differently and what you changed to fix it.

## Checklist
- [ ] [Must ship] Read the three Start here guides and list five techniques they agree on and one place where they differ.
- [ ] [Must ship] Rewrite one vague prompt with role, context, format and examples, and compare outputs.
- [ ] [Must ship] Store prompts as versioned template files that your code loads.
- [ ] [Recommended] Measure the accuracy of a few-shot classifier on at least 30 labelled examples.
- [ ] [Recommended] Build one three-step prompt chain with inspectable intermediate outputs.
- [ ] [Stretch] Run the same prompt on two providers and document the differences.

## You're ready when
- You can explain when to use few-shot examples, XML tags, chain of thought and prompt chaining.
- Your prompts live in versioned files, and each output records which version produced it.
- You can show a before and after accuracy number for a prompt change.
- You can review someone else's prompt and name its two biggest problems.
