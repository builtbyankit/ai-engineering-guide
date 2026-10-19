---
title: Enterprise and regulated settings
hours: 3–4
summary: Answer the governance, privacy, audit and model-risk questions that banks, insurers and other regulated companies ask AI engineers, with model answers and follow-ups.
checked: 2026-10-19
review-by: 2027-04-30 | which replaced SR 11-7 in April 2026
review-by: 2027-04-30 | is being revised
---

## Why these questions come up

Banks, payment companies, insurers, healthcare and government teams build AI under rules that most tutorials ignore. Their interviewers want to know that you won't put customer data, money or the company's licence at risk. Expect questions on approval processes, personal data, audit trails, explainability, fairness, vendor models and human oversight, alongside the usual design questions.

You don't need to be a lawyer. You need to show that you design for these constraints from the start, know the main frameworks by name and can say what each requires of the engineering team. If you have worked in a regulated company, your own stories about controls and approvals are some of your strongest material.

## Frameworks worth knowing by name

- **NIST AI Risk Management Framework (AI RMF 1.0).** A voluntary US framework from January 2023, organised around four functions: govern, map, measure and manage. NIST says it is being revised. Its **Generative AI Profile (NIST AI 600-1)**, from July 2024, applies it to generative AI risks.
- **US model risk management guidance (SR 26-2).** Revised supervisory guidance from the Federal Reserve, OCC and FDIC, which replaced SR 11-7 in April 2026. It covers model development, validation, monitoring, vendor models and governance. It explicitly leaves generative and agentic AI models out of scope and asks each bank's own risk practices to set their controls. Expect banks to apply similar ideas anyway: an inventory, independent validation and ongoing monitoring.
- **RBI FREE-AI framework.** A report from India's central bank, published in August 2025, setting out 7 principles (sutras) and 26 recommendations for responsible AI in the financial sector. Its six pillars are infrastructure, policy, capacity, governance, protection and assurance.
- **OWASP Top 10 for LLM and agentic applications.** The security checklists covered in [Security and guardrails](#l5-security).

Check which rules apply to the company and country you are interviewing for, and say so if you are unsure.

## Questions and model answers

### How would you get an LLM feature approved for launch in a bank?

Classify the use case by risk first: who it affects, what decisions it influences and what could go wrong. Document the purpose, data, model, prompts, limits and the evaluation results, including slices and adversarial tests. Have the evaluation reviewed by people independent of the build team. Launch with human oversight and monitoring, register it in the model inventory, and agree what change, such as a new model version, requires review again.

**Follow-up:** The risk team asks you to prove the model is "accurate". What do you show them?

### How do you handle customer personal data with a hosted model?

Send the model only the fields the task needs. Mask or tokenise identifiers before the call, and map them back afterwards in your own code. Use a provider agreement that rules out training on your data and sets retention and region. Redact personal data in logs and traces, limit who can read them, and set retention periods. Never put secrets or credentials in prompts.

**Follow-up:** Masking breaks the task because the model needs the customer's name. What now?

### How do you make an LLM-assisted decision auditable?

Record everything needed to reconstruct it. That means the input, the retrieved evidence with versions, the model and prompt versions, every tool call and result, the output, and any human approval with the reviewer's identity. Store this in an append-only log with a retention policy. Be honest that rerunning the model may not give the same text. The record of what happened is the audit evidence, not a later replay.

**Follow-up:** An auditor asks for every decision the agent made for one customer last March. How long does that take you?

### Can you explain why the model gave that answer?

Not reliably from the model's own account, because its stated reasoning may not reflect what actually drove the output. Instead, design for evidence: cite the documents and rules used, show the data the answer relied on, and keep the steps in traceable tool calls. For decisions that need clear reasons, keep the final decision in a rule or an interpretable model, and use the LLM to gather and summarise information.

**Follow-up:** A product manager wants the LLM to decide credit limit increases directly. How do you respond?

### How do you test an LLM system for bias?

Define which groups and outcomes matter for the use case, with the legal and risk teams. Build eval slices for those groups, and run counterfactual tests that change only a name, a dialect or another attribute and check whether the outcome changes. Monitor outcomes in production by slice where it is lawful to do so, and route borderline cases to people.

**Follow-up:** You can't collect protected attributes. How do you still test for bias?

### The model provider updates the model behind your API. What controls do you have?

Pin a specific model version rather than an alias that changes. Get notice of deprecations in the contract and track the provider's deprecation schedule. Rerun the full eval suite on the new version, release it as a canary with the old version still available, and keep an approved fallback. Treat a model change like any other change that needs review.

**Follow-up:** The pinned version will be retired in 60 days and the new one fails two of your eval slices. What do you do?

### Data must stay in the country. How does that change the design?

Use the provider's in-region endpoints if they meet the requirement, or self-host an open model inside the boundary. Make sure prompts, logs, traces, caches and vector stores all stay in the region, not only the model call. Route through a gateway that enforces the rule and fails closed. Re-evaluate quality, because the in-region or self-hosted model may perform differently.

**Follow-up:** The best model isn't available in-region. How do you make the case for or against using it?

### How do you let an agent act on accounts safely?

Give it the least privilege it needs, with per-action limits and per-customer scope enforced in code. Require approval for actions above a threshold, and use separation of duties so the person who requests an action can't approve it. Make every action idempotent and reversible where possible, log every proposal and decision, and keep a kill switch for action delivery that is separate from the chat itself. See [Human in the loop](#l4-human-in-the-loop).

**Follow-up:** Reviewers approve almost everything. Is that a problem?

### How do you monitor an LLM system for risk after launch?

Track quality on a sample of live traces with code checks and a calibrated judge, by slice. Watch input drift, refusal and escalation rates, complaints, cost and latency, and any security or privacy alerts. Define incident severity and a response process with named owners, and turn each incident into new eval cases. Report these to the risk owner on a regular schedule.

**Follow-up:** Quality drops on one customer segment, but the overall number looks fine. How would you catch that?

### What do you check before adopting a third-party model or AI vendor?

Check how the vendor handles and retains data, where it is processed and which security certifications it holds. Check what notice it gives before model changes, its uptime and limits, and the contract terms on training and liability. Plan an exit: keep prompts and evals portable and have a tested fallback. Run your own evals on your data, because a vendor's benchmark scores don't show how it will perform on your task.

**Follow-up:** Your team wants to use a new open model from an unknown publisher. What checks do you add?

## Checklist

- [ ] [Must ship] Answer five of the ten questions out loud in two minutes each, then answer their follow-ups.
- [ ] [Must ship] Explain in one minute each what the NIST AI RMF and your target company's main regulator expect from an AI team.
- [ ] [Must ship] Write one story from your own work about a control, an approval process or an audit, using STAR plus reflection.
- [ ] [Recommended] For one project you built, list what an auditor would need to reconstruct a decision and check that your logs capture it.
- [ ] [Recommended] Design counterfactual bias tests for one use case and run them on your own agent.
- [ ] [Stretch] Read the RBI FREE-AI report or SR 26-2 and note three recommendations that would change how you build.

## Resources

- [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) · NIST · Docs · Free · reference — The voluntary US framework for managing AI risk, with links to the framework, its playbook and the current revision work.
- [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) · NIST · Docs · Free · 1–2 h — NIST AI 600-1, which applies the framework to generative AI risks such as confabulation, data privacy and information security.
- [Revised Guidance on Model Risk Management (SR 26-2)](https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm) · Federal Reserve · Docs · Free · 1 h — The 2026 supervisory guidance for US banks that replaced SR 11-7, covering validation, monitoring and vendor models, and placing generative and agentic AI outside its scope.
- [Framework for Responsible and Ethical Enablement of Artificial Intelligence (FREE-AI)](https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?UrlPage=&ID=1306) · Reserve Bank of India · Docs · Free · self-paced — The RBI committee report setting out 7 principles and 26 recommendations for AI in India's financial sector.
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) · OWASP · Docs · Free · 1.5 h — The standard risk list for LLM applications, which regulated companies often use as a security review checklist.
- [Presidio](https://presidio.dataprivacystack.org/) · Presidio project · Docs · Free · reference — An open-source tool for finding and masking personal data before it reaches a model or a log.
