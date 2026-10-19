---
title: Mock interviews and scoring
hours: 4–6
summary: Run five timed mock rounds, score each one on six dimensions, retake your weakest area with new scenarios and know when you are ready.
checked: 2026-10-19
---

## Why mocks matter

Knowing an answer and giving it under time pressure, while someone changes the assumptions, are different skills. Mocks train the second one. They also show you which areas need work, so you stop spending equal time on everything.

Treat each mock like the real thing. Set a timer, speak out loud, draw on paper or a whiteboard tool and don't look anything up. Record yourself if you are practising alone, because you will hear gaps in the recording that you missed while talking.

## Five mock rounds

### Round A: system design (45 minutes)

**Prompt:** Design a permission-aware assistant that answers questions from company documents for 10,000 employees. Documents change daily, people gain and lose access, and traffic peaks at about 5 requests a second.

Follow the timeline on [Agentic system design rounds](#iv-system-design). By the end you should have:

- stated your assumptions;
- drawn ingestion and query paths with trust boundaries;
- done the storage, quota and cost numbers;
- walked through a permission change and an index rebuild;
- named your first release.

### Round B: coding and debugging (45 minutes)

**Prompt:** Pick one of the six problems on [Coding and debugging rounds](#iv-coding) that you haven't solved before. Write the contract and tests first, implement, then walk one failing case out loud.

Swap to a debugging round every other time: break your own agent in a way a friend chooses, and find the bug from the trace alone.

### Round C: incident review (30 minutes)

**Prompt:** A refund was approved and sent to the payment provider. The worker timed out before recording the result, its lease expired and a second worker picked up the job. The customer says they were refunded twice.

Draw the states from approval to confirmed refund. Explain how the second worker should have used the original idempotency key and checked the provider before doing anything. Say how you would confirm what actually happened, what you tell the customer, which alert should have fired and which regression test you would add.

**Probe to expect:** a cancellation request arrived after the refund was sent. What do you tell the user?

### Round D: evaluation review (30 minutes)

**Prompt:** Your team compares two retrievers. Keyword search scores 95% on answerable questions but refuses only 1 of 2 unanswerable ones. Hybrid search finds more right answers but refuses less often. Which do you ship, and what experiment do you run first?

Ask what the numbers are based on and how many cases each one covers. [Evaluation and debugging rounds](#iv-evals) works through the arithmetic. Point out that one of two is not a stable 50%. Separate retrieval metrics from answer quality, propose a larger labelled set with a fresh holdout and say which failure matters more for these users.

### Round E: customer conversation (30 minutes)

**Prompt:** Your partner plays the head of a finance team: "We process thousands of supplier invoices a month and it takes forever. Can AI help?" They answer your questions but volunteer nothing.

Follow the shape on [AI product and customer rounds](#iv-product). Ask questions that change the design, say which parts should not use an LLM, define outcome, quality and guardrail metrics, and propose a pilot. Finish by summarising the plan and asking what you missed.

**Probe to expect:** the customer says every invoice must be 100% correct. How do you respond?

## Score every mock

Score each mock on six dimensions from 0 to 4, right after you finish and before you look anything up.

| Dimension | What it covers |
| --- | --- |
| Requirements | Clarified the job, risk, traffic and success before designing |
| Technical mechanism | Explained how the parts actually work, not just their names |
| Failure and trust control | Kept authority in code, handled timeouts, retries, injection and unknown outcomes |
| Numbers and trade-offs | Put figures on cost, latency and limits, and named what was traded away |
| Evaluation evidence | Said how quality would be measured and what would block a release |
| Communication and ownership | Clear structure, honest about what is built versus assumed, adapted to follow-ups |

| Score | Meaning |
| --- | --- |
| 0 | Missing, or unsafe |
| 1 | Vocabulary without a workable example |
| 2 | A coherent example, but weak on failures or evidence |
| 3 | A defensible design with concrete controls and a way to validate them |
| 4 | Handles changed assumptions, limits and interacting failures, and states what is still uncertain |

## Run mocks alone or with a partner

- **Alone:** record yourself, score the recording the next day and write down the one change that would most improve the score.
- **With a partner:** give them the prompt, the follow-ups on [Agentic system design rounds](#iv-system-design) and the scoring table. Ask them to interrupt and change one assumption halfway.
- **With an AI interviewer:** an assistant can play the interviewer and ask follow-ups. Score yourself anyway, because it may be too generous, and never paste in anything confidential.

## Retake the weakest dimension

After each mock, pick your lowest-scoring dimension and practise it with a new scenario, not the same prompt with better wording. Rehearsing one answer teaches you that answer. A new scenario teaches the skill.

A reasonable target before a real loop is three mocks on different prompts, each scoring at least 18 of 24 with no dimension below 2. None of your answers should rely on the model as a security boundary or claim experience you don't have. This is a self-check, not a prediction of the outcome.

## Checklist

- [ ] [Must ship] Complete Round A under time and score it on all six dimensions.
- [ ] [Must ship] Complete Round C or Round D under time and score it.
- [ ] [Must ship] Retake your weakest dimension with a new scenario and compare the scores.
- [ ] [Recommended] Complete all five rounds at least once.
- [ ] [Recommended] Run at least one mock with a partner who changes an assumption halfway.
- [ ] [Stretch] Reach 18 of 24 on three different mocks with no dimension below 2.

## Resources

- [Interview Workbook: Explain, Defend, Build](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-interview-workbook.md) · Agentic AI Mastery · Tutorial · Free · 1 h — The original four mock rounds with minute-by-minute plans, strong and weak answers, the scoring scheme and a personal project narrative template.
- [Worked Capacity, Latency, and Cost Design](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-worked-capacity-and-cost.md) · Agentic AI Mastery · Tutorial · Free · 45 min — The assumptions and worked numbers behind Round A, so you can check your arithmetic after the mock.
- [Module 6: Human Approval and Retry-Safe Actions](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-module-06-human-approval-outbox.md) · Agentic AI Mastery · Tutorial · Free · 1 h — A runnable approval and outbox lab whose crash and retry checks mirror the Round C incident.
- [Evaluation Metrics for Search and Recommendation Systems](https://weaviate.io/blog/retrieval-evaluation-metrics) · Weaviate · Article · Free · 10 min — Short definitions of recall@k, MRR and nDCG to refresh before Round D.
