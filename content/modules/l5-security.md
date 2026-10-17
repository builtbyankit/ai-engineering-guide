---
title: Security and guardrails
level: L5
kind: core
hours: 10
summary: Explain and test prompt injection and other LLM risks, design agents that limit damage by construction, and add guardrails and red-team scans to your workflow.
checked: 2026-10-16
review-by: 2027-01-31 | The 2026 list for agentic applications
---

## Why it matters

An agent reads untrusted text and can take actions, and that pairing creates a new attack surface. A web page, email, PDF or tool result can contain instructions, and the model may follow them. This is prompt injection. No model or filter blocks it reliably today, and in recent research adaptive attacks bypassed most published defences.

Agent security is therefore mostly an architecture problem. You limit what a hijacked agent can reach and keep private data away from untrusted input and outbound channels. You require approval for risky actions, as in [Human in the loop](#l4-human-in-the-loop), and you attack your own system before anyone else does. Guardrail models and filters help as one layer. This module gives you the threat model, the design patterns and the tools.

## What to learn

- **Direct and indirect prompt injection**: Direct injection comes from a user typing instructions. Indirect injection hides instructions in content the agent reads, such as a web page, a document or a tool result. Indirect injection is the bigger risk for agents because the attacker never talks to your system directly.
- **Injection and jailbreaks**: A jailbreak tries to make the model break its own safety rules. Injection overrides your application's instructions through untrusted input. They overlap, but the defences differ.
- **The lethal trifecta**: The risky combination is access to private data, exposure to untrusted content and a way to send data out. An agent with all three can be tricked into leaking data. Meta's Agents Rule of Two generalises this to untrusted input, sensitive access and state-changing actions, and allows at most two per session without human supervision.
- **OWASP Top 10 lists**: The 2025 list for LLM applications covers risks such as prompt injection, sensitive information disclosure, improper output handling, excessive agency and unbounded consumption. The 2026 list for agentic applications adds risks specific to agents that plan and act. Use both as review checklists.
- **Least privilege and sandboxing**: Give each tool the narrowest scope it needs, such as read-only access, scoped tokens, allowlisted domains and per-user permissions. Run generated code in a container or VM with no secrets and limited network, as covered in [Coding agents](#l4-coding-agents). [Tool calling in depth](#l3-tool-calling) and [MCP](#l3-mcp) cover tool-level risks.
- **Secure design patterns**: Action-selector, plan-then-execute, map-reduce, dual LLM, code-then-execute and context minimisation all stop untrusted text from choosing the agent's next action. CaMeL goes further by tracking where each value came from and enforcing policies at every tool call.
- **Guardrails as one layer**: Input and output filters catch known-bad content, policy violations and personal data. Llama Guard is a safety classifier model, NeMo Guardrails adds programmable rails including checks on tool execution, and Guardrails AI wraps calls with validators. Treat them as risk reducers and measure their false positives.
- **PII handling**: Send the model only the personal data a task needs, mask it in traces and logs with a tool such as Presidio, and set retention limits.
- **Red-teaming**: Attack your own system on purpose. Scanners such as garak, PyRIT and promptfoo's red-team mode generate many attacks, and you add hand-written injections aimed at your tools. Re-run the suite after every change, because defences regress.

## Resources

### Start here

- [The lethal trifecta for AI agents: private data, untrusted content, and external communication](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · Simon Willison · Article · Free · 15 min — The clearest mental model for when an agent can be tricked into stealing data, and why removing one of the three ingredients is the reliable fix.
- [Design Patterns for Securing LLM Agents against Prompt Injections](https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/) · Simon Willison · Article · Free · 10 min — A readable summary of six defensive patterns from a multi-lab paper, with the trade-off each makes between capability and safety.
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) · OWASP · Docs · Free · 1.5 h — The standard risk list with examples and mitigations; read prompt injection, sensitive information disclosure, improper output handling and excessive agency closely.

### Go deeper

- [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) · OWASP · Docs · Free · 1.5 h — The peer-reviewed companion list for autonomous agents, released in December 2025, covering risks that appear when models plan and act with tools.
- [Agents Rule of Two: A Practical Approach to AI Agent Security](https://ai.meta.com/blog/practical-ai-agent-security/) · Meta AI · Article · Free · 15 min — A simple design rule with worked examples showing how dropping one risky property breaks an attack chain.
- [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/abs/2506.08837) · Beurer-Kellner et al. · Paper · Free · 1.5 h — The full paper behind the six patterns, with utility and security trade-offs and case studies of realistic agents.
- [Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) · Google DeepMind · Paper · Free · 2 h — Introduces CaMeL, which separates control flow from untrusted data and enforces capability policies at tool calls, evaluated on AgentDojo.
- [Red Teaming LLM Applications](https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/) · DeepLearning.AI, Giskard · Course · Free tier · 1.5 h — Short video course on manual and automated red-teaming of a chatbot, including prompt injection attacks and a full assessment walkthrough.
- [Presidio](https://presidio.dataprivacystack.org/) · Presidio project · Docs · Free · reference — Open-source analyzer and anonymizer for finding and masking personal data such as names, card numbers and locations before it reaches a model or a log.

### Reference

- [garak](https://github.com/NVIDIA/garak) · NVIDIA · Repo · Free · reference — LLM vulnerability scanner with probes for injection, jailbreaks, data leakage and more, runnable against hosted models or any REST endpoint.
- [PyRIT](https://github.com/microsoft/PyRIT) · Microsoft · Repo · Free · reference — Red-teaming framework with single-turn and multi-turn attack strategies, converters and scorers for automating attacks on your own system.
- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) · NVIDIA · Repo · Free · reference — Open-source toolkit for input, dialogue, retrieval, execution and output rails, with flows written in the Colang language.
- [Guardrails AI documentation](https://guardrailsai.com/docs) · Guardrails AI · Docs · Free · reference — Python framework that wraps model calls in input and output guards built from Hub validators, and also validates structured output.
- [Llama Guard 4 model card](https://dev.meta.ai/llama/docs/model-cards-and-prompt-formats/llama-guard-4) · Meta · Docs · Free · reference — A 12B safety classifier for prompts and responses with 14 hazard categories and the exact prompt format for each kind of check.

## Practice

1. **Break a toy agent.** Build or reuse an agent that reads a folder of notes and has a fake "send email" tool that only writes to a log file. Plant an instruction in one note asking it to email the other notes elsewhere. Done when you have reproduced a successful exfiltration and saved its trace.
2. **Map your trifecta.** For your Level 3 or Level 4 agent, label each tool as private data, untrusted input or outbound channel, and note the OWASP risks that apply. Done when you have a one-page threat model naming which leg you will remove or gate, and why.
3. **Fix it by design.** Apply one pattern to the toy agent, such as plan-then-execute, a quarantined reader that returns only structured fields, or human approval on outbound tools. Re-run the attack from exercise 1. Done when the attack fails and your normal tasks still pass.
4. **Scan and filter.** Set a spending cap with your provider, then run garak or promptfoo's red-team mode against a copy of your agent whose side-effecting tools are stubbed. Start narrow, with one garak probe family and fewer generations, or a capped number of promptfoo tests, because the defaults can mean thousands of agent runs. Then add one guardrail such as Llama Guard, NeMo Guardrails or a Presidio mask. Done when you report attack success rate before and after, plus the false positive rate on 30 benign inputs.

## Checklist

- [ ] [Must ship] Write a threat model that marks each tool against the lethal trifecta and lists the OWASP risks that apply.
- [ ] [Must ship] Reproduce at least one indirect prompt injection against your own agent.
- [ ] [Must ship] Apply one structural defence, such as least privilege, a design pattern or human approval, and show the attack now fails.
- [ ] [Must ship] Keep a regression suite of 10 or more injection cases that runs with your evals.
- [ ] [Recommended] Add one guardrail layer and measure its false positive rate on benign inputs.
- [ ] [Stretch] Run an automated multi-turn attack campaign with PyRIT or promptfoo and triage the results.

## You're ready when

- You can explain direct and indirect prompt injection and why filters alone cannot stop it.
- You can read an agent's tool list and say whether it has the lethal trifecta.
- Your agent has at least one defence that still holds if the model is completely fooled.
- You can report your agent's attack success rate on a fixed injection suite and track it over time.
