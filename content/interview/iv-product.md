---
title: AI product and customer rounds
hours: 4–5
summary: Handle the round where a customer or product manager describes a fuzzy problem, and you scope it, decide whether AI fits, define success and propose a first release.
checked: 2026-10-19
---

## What this round tests

Many applied AI loops now include a conversation with a pretend customer or product manager. They describe a problem in business terms, such as "our support team is drowning", and you lead the discussion. There is usually no diagram to draw at first. Candidates who do well in the coding rounds often fail this one, because they jump straight to an architecture before they understand the problem.

The interviewer is checking four things. Do you ask questions that change the design? Can you say plainly whether an LLM is the right tool? Do you define success in numbers the customer cares about? Do you propose something small that can ship and be measured? Treat it like a real first meeting with a client.

## The shape of a strong conversation

1. **Understand the job.** Who has the problem, how often, what they do today and what it costs them. Ask for an example of a good and a bad outcome.
2. **Find the constraints.** Data you can use, privacy rules, the price of a wrong answer, how fast it must respond, budget, and who must approve actions.
3. **Decide whether AI fits.** Say what an LLM adds, and what a rule, a search box or a form would do instead. It is fine to recommend no AI for part of the problem.
4. **Define success.** One outcome metric the customer cares about, one quality metric you can measure offline, and one guardrail metric that must not get worse.
5. **Propose a first release.** The smallest version that delivers value and can be measured, such as drafts for a person to approve rather than full automation.
6. **Plan how you'd learn.** How you'd collect examples, build an eval set, run a pilot and decide whether to expand.
7. **Summarise and check.** Restate the problem, the plan and the open questions, and ask the customer whether you missed anything.

## Questions that change the design

Good questions are the ones whose answer would change what you build. Keep a few ready in each area.

| Area | Questions |
| --- | --- |
| Users and job | Who uses it, and what do they do today? What does a great result look like? How many requests a day? |
| Cost of mistakes | What happens if the answer is wrong? Who notices, and how quickly? Is anything irreversible? |
| Data | Where does the knowledge live, and how often does it change? Are there access rules? Can we use past examples? |
| Actions | Should it only answer, or also act? Who approves actions, and what are the limits? |
| Constraints | Response time? Budget per request or per month? Any rules about where data may go? |
| Success | How do you measure this today? What number would make this a success in three months? |

## Deciding whether an LLM fits

An LLM tends to fit when:

- inputs are messy natural language;
- the right answer depends on reading and judgement;
- mistakes can be caught, or are cheap;
- there is enough volume to be worth automating.

It tends not to fit when:

- the logic is a clear rule;
- every answer must be exactly right with no review;
- there is no way to check quality;
- a search box or a form would solve it.

Say this out loud with the customer's own examples. For instance: "Tracking questions follow a rule, so a lookup handles them without a model. Complaints mixing several issues need reading and judgement, so that's where a model helps."

## Defining success

| Kind of metric | Example for a support assistant |
| --- | --- |
| Outcome the customer cares about | Median time to first response, share of tickets resolved without escalation |
| Quality you measure offline | Draft accuracy on a labelled set, share of answers grounded in a help article |
| Guardrail that must not get worse | Customer satisfaction, rate of wrong refunds, privacy incidents |
| Cost | Cost per resolved ticket, including review time |

Agree on a baseline before you build, so you can show the change. If the customer has no measurement today, say that collecting a baseline is the first task.

## Worked example: a support team that is drowning

**Customer:** "Our support team can't keep up. Customers wait two days for a reply. Can AI fix this?"

**You ask:** How many tickets a day, and what are the main types? What do agents do for each type? How long does a reply take? Do replies follow help articles, or need judgement? Can the system issue refunds, or only reply? What happens today when a reply is wrong?

**Customer answers (example):** About 2,000 tickets a day. Roughly half are order status, a third are returns and refunds, and the rest is a mix. Agents use about 40 help articles. Refunds over a set amount need a manager.

**You propose:**

- Answer order status automatically with a lookup and a template. No model is needed, and it removes about half the queue.
- For returns and the mixed tickets, have a model classify the ticket, retrieve the relevant help article and draft a reply with citations. An agent approves or edits the draft before it is sent. The model never issues refunds.
- Measure time to first response and the share of drafts sent without edits. Guard customer satisfaction and wrong-refund rate.
- Pilot on one ticket type for two weeks with a labelled set of 200 past tickets. Expand only if drafts are accepted without edits at a rate the team agrees on in advance.

**You check:** "Have I got the ticket mix right? Is there anything agents do that wouldn't show up in the ticket text, such as checking another system?"

## Common traps

- Designing the architecture before asking a single question.
- Promising full automation of a task where mistakes are expensive.
- Naming a model or framework as the answer to a business question.
- Success metrics that only measure the model, such as accuracy, with nothing the customer cares about.
- Ignoring the people in the loop, such as reviewers, their workload and their trust in the system.
- Never saying "I don't know yet; here's how we'd find out."

## Checklist

- [ ] [Must ship] Write your own list of six questions that would change the design, one per area in the table.
- [ ] [Must ship] Run the worked example as a 30-minute role-play with a friend playing the customer, without reading the answer first.
- [ ] [Must ship] For one project you built, write success metrics in all four rows of the metrics table.
- [ ] [Recommended] Practise two more scenarios: an internal document assistant for a legal team, and invoice processing for a finance team.
- [ ] [Recommended] For each scenario, say clearly which part should not use an LLM and why.
- [ ] [Stretch] Record a role-play and score it on whether every question you asked changed the plan.

## Resources

- [Errors + Graceful Failure](https://pair.withgoogle.com/chapter/errors-failing/) · Google PAIR · Article · Free · 30 min — A chapter of the People + AI Guidebook on deciding what users will see as an error and giving them a way forward when the AI falls short.
- [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/) · Microsoft Research · Paper · Free · 45 min — Eighteen tested guidelines for how AI products should behave at the start, during use, when wrong and over time, a useful checklist for scoping.
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) · OpenAI · Article · Free · 1 h — Opens with how to decide whether a use case needs an agent at all, the core question in a customer round.
- [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) · Hamel Husain · Article · Free · 20 min — A real product case study tying evals to product decisions, good material for the "how would you measure success" part.
- [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/) · Eugene Yan and Jason Liu · Article · Free · 25 min — What hiring managers look for in AI engineers, including comfort with ambiguity and judgement, seen from the interviewer's side.
