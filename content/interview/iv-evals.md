---
title: Evaluation and debugging rounds
hours: 5–6
summary: Work the numbers interviewers ask about in evaluation rounds, from judge calibration to small samples, and debug five common agent failures from their traces.
checked: 2026-10-19
---

## Why this round trips people up

Evaluation is the round where many otherwise strong candidates struggle. Saying "we'd use an LLM judge" is easy. Explaining how you know the judge is right, whether a 4-point improvement is real, and what to test before a release is harder. Debugging rounds have the same problem: they reward a calm method, not a lucky guess.

This page works through the numbers and the debugging method with concrete examples. Do the arithmetic yourself before reading each answer. Interviewers often ask you to do it out loud.

## Calibrating an LLM judge

**Setup.** You label 100 agent answers yourself: 20 fail and 80 pass. Your judge marks 14 of the 20 failures as failures, and 76 of the 80 passes as passes. Treat "fail" as the positive class, because catching failures is the judge's job.

- **True positive rate (TPR):** 14 / 20 = 70%. The judge catches 70% of real failures.
- **True negative rate (TNR):** 76 / 80 = 95%. It rarely flags a good answer.
- **Raw agreement:** (14 + 76) / 100 = 90%. This sounds good but hides the fact that the judge misses almost a third of failures.

**Correcting the production rate.** In production the judge flags 12% of 1,000 traces. That is not the true failure rate, because the judge is imperfect. A standard correction estimates the true rate as (flagged + TNR − 1) / (TPR + TNR − 1) = (0.12 + 0.95 − 1) / (0.70 + 0.95 − 1) = 0.07 / 0.65 ≈ 10.8%.

**What to say.** Report TPR and TNR on a held-out labelled set the judge was never tuned on, not raw agreement. Improve the judge by narrowing it to one criterion, asking for pass or fail, and adding labelled examples with written critiques. Re-check it when the model, prompt or data changes.

## Is the improvement real?

**One pass rate.** Your agent passes 42 of 50 eval cases (84%). The standard error is √(0.84 × 0.16 / 50) ≈ 0.052, so a 95% interval is roughly 84% ± 10 points, about 74% to 94%. A new prompt scoring 88% on the same 50 cases is well inside that range.

**Compare on the same cases.** Look at the cases that changed. Suppose the new prompt fixes 6 cases and breaks 2. Only those 8 changed cases carry information, and a 6-to-2 split happens by chance about 29% of the time even when the prompts are equally good. Say you would add cases or run more trials before shipping.

**How many cases you need.** Detecting a 5-point change around 80% with two separate samples needs on the order of a thousand cases per version. Comparing the same cases, as above, needs fewer. That is why teams grow eval sets from production failures and run each case several times.

**Repeated runs.** If each attempt succeeds 90% of the time independently, the chance that three attempts all succeed (pass^3) is 0.9³ ≈ 73%. Users who rely on the agent every day experience something closer to that number than to 90%.

## Designing an eval for a new feature

A common prompt: "We're adding a refund tool to the support agent. How would you evaluate it before launch?" A strong answer covers:

- **Slices.** Eligible and ineligible refunds, amounts near the limit, missing order numbers, two issues in one message, other customers' orders and requests in other languages.
- **Adversarial cases.** Instructions hidden in a ticket or a help article that try to trigger a refund, and repeated requests for the same order.
- **Graders.** Code checks for tool choice, arguments and limits; outcome checks on the final database state; an LLM judge only for tone and completeness, calibrated as above.
- **Release blockers.** Any refund without approval, any refund to the wrong customer, any duplicate refund. A high average score can't outweigh these.
- **Data hygiene.** Keep a holdout set you never tune on, and add every production failure to the dev set.
- **Rollout.** Shadow mode first, then proposals only, then approved refunds for a small share of traffic.

## A method for debugging rounds

1. **Restate the symptom** with numbers: what changed, since when, and for whom.
2. **Find a good trace and a bad trace** for similar inputs and compare them step by step.
3. **Locate the first divergence,** not the last symptom. The final answer is usually wrong because of something earlier.
4. **Classify the cause:** retrieval, tool, model, prompt, state or infrastructure.
5. **Confirm with one test** that fails before the fix and passes after it.
6. **Prevent recurrence:** add the case to the eval set, add a check or alert, and say what you would monitor.

## Five common failures, worked

### The agent calls the same tool over and over

**Trace:** `search_orders` is called 12 times with identical arguments, and the run hits the step limit.

**Likely causes:** the tool returns an error the model can't act on, such as "failed"; the result is too long and gets cut off; or the result was sent without its call ID, so the model never saw it.

**Fix:** return specific, actionable errors; cap and summarise results; detect repeated identical calls and stop with a reason; add the case to the eval set.

### Answers got worse after the index was rebuilt

**Trace:** the right document exists, but retrieval now returns archived versions, and recall@5 dropped from 0.88 to 0.71.

**Likely causes:** the rebuild used a new embedding model while some old vectors remained; a metadata filter for version or status was dropped; or chunking changed and split the key passage.

**Fix:** build each index version separately and switch only when retrieval checks pass; run recall@k in CI on every rebuild; keep the version filter covered by a test.

### Failures rose after a model upgrade

**Trace:** structured outputs now fail validation 6% of the time, up from 0.5%, mostly on date fields.

**Likely causes:** the new model formats some values differently, the prompt relied on the old model's habits, or strict schema mode was off.

**Fix:** pin model versions; turn on strict schemas where supported; add validators with a capped retry; gate model changes on the eval suite and release them as a canary.

### Cost per task tripled

**Trace:** input tokens per task jumped from about 6,000 to 19,000.

**Likely causes:** a tool started returning raw HTML; the conversation history is being sent twice; or a timestamp at the top of the system prompt is breaking the prompt cache on every call.

**Fix:** cap tool results; use one source of history; keep the stable prompt prefix first; alert on tokens per task, not just total spend.

### The right document was retrieved, but the answer is wrong

**Trace:** the cited chunk says returns are accepted within 30 days, but the answer says 14 days.

**Likely causes:** an older version of the same policy was also retrieved; the key chunk sat in a long context among many others; or the prompt doesn't require answers to come only from the cited text.

**Fix:** deduplicate by source and keep only the current version; send fewer, better-ranked chunks; check that each cited passage supports the claim; add a faithfulness check to the eval set.

## Checklist

- [ ] [Must ship] Redo the judge calibration and the confidence interval with your own numbers, out loud, without notes.
- [ ] [Must ship] Answer the refund-tool eval prompt in 15 minutes, covering slices, graders, blockers and rollout.
- [ ] [Must ship] Debug two of the five failures out loud using the six-step method before reading the worked answer.
- [ ] [Recommended] Calibrate a real judge on 50 or more of your own labelled outputs and report TPR and TNR.
- [ ] [Recommended] Break your own agent in one of the five ways and find it from the trace alone.
- [ ] [Stretch] Compare two prompts on your eval set using only the changed cases, and say whether the difference is real.

## Resources

- [Using LLM-as-a-Judge For Evaluation: A Complete Guide](https://hamel.dev/blog/posts/llm-judge/) · Hamel Husain · Article · Free · 30 min — The step-by-step method for building a binary judge from expert critiques and validating it with true positive and true negative rates.
- [A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals) · Anthropic · Article · Free · 10 min — Five recommendations for reporting eval results, including standard errors, paired comparisons and power analysis.
- [Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations](https://arxiv.org/abs/2411.00640) · Evan Miller · Paper · Free · 1 h — The paper behind those recommendations, with the formulas for standard errors, clustered errors and paired differences.
- [Demystifying evals for AI agents](https://anthropic.com/engineering/demystifying-evals-for-ai-agents) · Anthropic · Article · Free · 25 min — Tasks, trials, graders and harnesses for agent evals, with a clear treatment of pass@k and pass^k.
- [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) · Hamel Husain and Shreya Shankar · Article · Free · 2–3 h — A long FAQ covering error analysis, judge bias, correcting judge-estimated rates and evaluating agents, ideal for follow-up questions.
