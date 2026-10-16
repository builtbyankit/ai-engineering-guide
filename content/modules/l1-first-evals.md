---
title: Your first evals
level: L1
kind: core
hours: 5–6
summary: Build a small golden dataset and an automated eval that scores LLM outputs, then use it to compare prompt and model versions with numbers.
checked: 2026-10-16
---

## Why it matters
Without measurement, prompt work is guesswork. You change a word, try two inputs, like the result and ship it, and you never see the five cases it broke. LLM output also varies between runs, so "it worked when I tried it" proves very little.

An eval is a repeatable test with fixed inputs, expected results and a scoring rule. Even 20 to 50 well-chosen examples turn arguments about quality into numbers you can track across prompt versions and models. This module gets a first harness running. [Evals in depth](#l5-evals-in-depth) in Level 5 covers error analysis, calibrated LLM judges and agent evals.

## What to learn
- **Why evals**: Evals let you change prompts, models and code with confidence and catch regressions before users do. Experienced practitioners such as Hamel Husain argue that weak evaluation is the most common reason LLM products stall.
- **Golden dataset**: A set of inputs with known-good outputs, written or checked by a person. Mix typical cases with edge cases, and draw from real inputs whenever you can.
- **Assertion-based checks**: Simple code checks such as "output parses as JSON", "contains the order number" or "is under 100 words". They are fast, free and deterministic, so write them first.
- **Exact match**: Compare a field to the expected value after normalising case and whitespace. This suits labels, numbers, dates and IDs.
- **Fuzzy match**: For text where wording varies, use string similarity, keyword overlap or embedding similarity. Pick a threshold and check a sample by hand to confirm it behaves sensibly.
- **LLM-graded checks**: A second model grades the output against a rubric, which suits qualities like tone or completeness. Prefer pass or fail over a 1 to 10 scale, and spot-check the grader against your own judgement.
- **Tracking across versions**: Record prompt version, model, score, cost and date for every run. A results table over time shows whether a change actually helped.
- **Tools**: promptfoo runs evals from a YAML config and shows results side by side in a local viewer. A pytest file with parametrized cases does the same job in plain Python. Choose promptfoo for quick model comparisons and pytest if you want everything in your codebase.

## Resources
### Start here
- [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) · Hamel Husain · Article · Free · 20 min — The practitioner's case for evals, with three levels of testing and a real case study built on simple assertions.
- [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) · Anthropic · Docs · Free · 45 min — How to set measurable success criteria and write exact-match, similarity and LLM-graded evals, with a short code example for each.
- [Getting started](https://www.promptfoo.dev/docs/getting-started/) · promptfoo · Tutorial · Free · 1 h — Set up an open-source eval config, test prompts across models with assertions, and review the results in a local web viewer.
### Go deeper
- [Building evals](https://platform.claude.com/cookbook/misc-building-evals) · Anthropic · Tutorial · Free · 45 min — A notebook that builds code-graded, human-graded and model-graded evals on the same small task so you can compare them.
- [Prompt evaluations](https://github.com/anthropics/courses/blob/master/prompt_evaluations/README.md) · Anthropic · Course · Free · self-paced — Nine lessons from code-graded classification evals to custom model-graded evals in promptfoo; the repo is archived, so update model names.
- [Task-Specific LLM Evals that Do & Don't Work](https://eugeneyan.com/writing/evals/) · Eugene Yan · Article · Free · 45 min — Which metrics hold up for classification, extraction, summarisation and translation, and which mislead.
- [Automated Testing for LLMOps](https://www.deeplearning.ai/short-courses/automated-testing-llmops/) · DeepLearning.AI · Course · Free tier · 1–1.5 h — Rules-based and model-graded evals wired into a CI pipeline so every change gets tested.
- [What We've Learned From A Year of Building with LLMs](https://applied-llms.org/) · Yan, Husain, Shankar et al. · Article · Free · 1.5–2 h — Read the evaluation section for assertion-based unit tests built from real inputs and outputs.
- [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/) · Hamel Husain · Article · Free · 30 min — Why reading real outputs and doing error analysis beats generic metrics, with advice on binary judgements and synthetic test data.
### Reference
- [Assertions & metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/) · promptfoo · Docs · Free · reference — Every assertion type, from `equals` and `is-json` to `llm-rubric`, with weights and thresholds.
- [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html) · pytest · Docs · Free · reference — Run one test function over every case in your golden set with `@pytest.mark.parametrize`.
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) · OpenAI · Docs · Free · 30 min — A step-by-step eval design process and the trade-offs between metric-based, human and LLM-judge graders.
- [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) · Hamel Husain and Shreya Shankar · Article · Free · reference — A long FAQ to dip into when a specific question comes up; Level 5 works through it properly.

## Practice
1. **Build a golden set.** First add an optional `order_number` field to your classifier's schema from the previous module. Collect 25 support emails, written by you or adapted from public examples, and label each with category, urgency and the order number if present. Include at least five hard cases, such as two issues in one email or no order number. Done when the set lives in a versioned JSONL file.
2. **Assert first.** Write a pytest file that runs your classifier from the previous module on every golden example. Check that the JSON parses, labels are valid and order numbers match exactly. Done when one command reports how many cases pass.
3. **Compare two prompts.** Run two prompt versions on two models through the same harness, in pytest or promptfoo. Done when a results table shows accuracy, cost and latency for all four combinations.
4. **Try an LLM grader.** Have a model draft a reply to each email, then have a second model grade each reply pass or fail for politeness and for addressing every issue. Grade 15 replies yourself. Done when you know how often the grader agrees with you.
5. **Keep a scoreboard.** Append each run's prompt version, model, date, score and cost to a CSV file. Done when you can see at a glance whether your last three changes helped.

## Checklist
- [ ] [Must ship] Create a golden set of at least 25 labelled examples, including hard cases.
- [ ] [Must ship] Write deterministic assertions that run on every example with one command.
- [ ] [Must ship] Compare two prompt versions on the golden set and record the scores.
- [ ] [Recommended] Set up the same eval in promptfoo and view the results side by side.
- [ ] [Recommended] Add one LLM-graded check and measure its agreement with your own labels.
- [ ] [Stretch] Run the eval automatically in GitHub Actions on every push.

## You're ready when
- You can explain why trying a few inputs by hand cannot tell you whether a change helped.
- Your project has a golden set and a script that scores it in one command.
- You can say when to use exact match, fuzzy match and an LLM grader.
- You can show a score history across at least two prompt or model versions.
