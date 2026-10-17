---
title: Open models, fine-tuning and serving
level: L6
kind: optional
hours: 10
summary: Decide when fine-tuning beats prompting or RAG, fine-tune a small open model with LoRA, and serve it behind an OpenAI-compatible API with vLLM or Ollama.
checked: 2026-10-16
---

## Why it matters

Hosted frontier models are the right default for most agents. Some situations still push you toward open models. Data that must stay on your own hardware, a narrow task called millions of times, a tight latency budget or an unusual output format can all make a small tuned model the better choice.

This module shows when that trade is worth it and how to make it. You fine-tune a small model with LoRA on a free GPU, quantize it so it fits on modest hardware, and serve it behind the same API your agent already uses. It is an optional specialisation. You need working evals first, because without them you cannot tell whether the tuned model is any better.

## What to learn

- **Prompt, RAG or fine-tune**: Prompting changes instructions, RAG supplies facts at query time, and fine-tuning changes behaviour such as format, style, tool-call syntax or a narrow skill. Exhaust prompting and retrieval first, and fine-tune only when evals show a gap they cannot close.
- **Open-weight models**: These are models whose weights you can download and run, such as the Llama, Qwen, Gemma and Mistral families. Before you pick one, check the licence, the context length and whether an instruction-tuned variant with tool calling exists.
- **Supervised fine-tuning (SFT)**: You train on example conversations so the model learns to imitate the assistant turns. Data quality matters more than size, so a small, clean, hand-checked set often beats a large noisy one.
- **LoRA and QLoRA**: LoRA freezes the base model and trains small low-rank adapter matrices, so only a tiny fraction of weights change. QLoRA does the same on a 4-bit quantized base, which lets a 7B or 8B model train on a single modest GPU.
- **Chat templates and tool-call formats**: Each model family expects its own special tokens for roles and tool calls. Train and serve with the same template, or the tuned model will emit malformed tool calls.
- **Distillation for agents**: A strong model generates successful agent trajectories (reasoning, tool calls, observations), your evals filter them, and a small model is fine-tuned on the survivors. This can make a narrow agent far cheaper to run, but the student also inherits the teacher's habits and mistakes.
- **Reinforcement fine-tuning**: When code can score an output, such as a passing test, a correct answer or a valid tool call, you can train on rewards instead of examples. GRPO samples several answers per prompt and shifts the model toward the higher-scoring ones. It needs a reliable grader and more compute than SFT, and a loose reward teaches the model to game it.
- **Quantization**: Storing weights in 8, 4 or fewer bits instead of 16 cuts memory and often speeds up inference, at some cost in quality. GGUF files suit llama.cpp and Ollama, while GPTQ, AWQ and FP8 formats suit GPU servers such as vLLM.
- **Serving**: Ollama is the easy path for local and single-user serving. vLLM is built for GPU throughput and batches many concurrent requests. Both expose OpenAI-compatible endpoints, so your gateway and agent code barely change. Size memory for the weights plus a key-value cache that grows with context length and concurrent requests ([Agent system design and capacity planning](#l6-system-design) has the formula).
- **Total cost of ownership**: A rented GPU bills by the hour whether traffic arrives or not. Compare that with per-token API pricing at your real volume, and count the engineering time to evaluate, update and monitor your own model.

## Resources

### Start here

- [Is Fine-Tuning Still Valuable?](https://hamel.dev/blog/posts/fine_tuning_valuable.html) · Hamel Husain · Article · Free · 15 min — A practitioner's view of when fine-tuning pays off, with real product cases, and why an eval system must come first.
- [Supervised Fine-Tuning](https://huggingface.co/learn/llm-course/chapter11/1) · Hugging Face · Course · Free · 2–3 h — LLM Course chapter covering chat templates, supervised fine-tuning, LoRA and evaluating the result with the Hugging Face libraries.
- [Fine-tuning LLMs Guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide) · Unsloth · Tutorial · Free · 1.5 h — Choosing a model, LoRA versus QLoRA, datasets and hyperparameters, then exporting to GGUF for Ollama or to vLLM, with free Colab notebooks.

### Go deeper

- [Practical Tips for Finetuning LLMs Using LoRA](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms) · Sebastian Raschka · Article · Free · 20 min — Experiment results on rank, alpha, which layers to adapt, QLoRA's memory and speed trade-off, and the value of a small curated dataset.
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) · Hu et al. · Paper · Free · 1 h — The original LoRA paper; read the method section and the comparison with full fine-tuning.
- [Bonus Unit 1. Fine-tuning an LLM for Function-calling](https://huggingface.co/learn/agents-course/bonus-unit1/introduction) · Hugging Face · Course · Free · self-paced — A short Agents Course unit that fine-tunes Gemma 2 2B to produce tool calls, with a Colab notebook you can run.
- [Fine Tuning LLMs for Function Calling](https://parlance-labs.com/education/fine_tuning/pawel.html) · Parlance Labs · Video · Free · 1.5 h — Pawel Garbacki's talk on tool-call syntax, training data, LoRA versus full tuning and constrained decoding for function-calling models.
- [Distilling LLM Agent into Small Models with Retrieval and Code Tools](https://arxiv.org/abs/2505.17612) · Kang et al. · Paper · Free · 1 h — Shows that distilling whole agent trajectories, tool use included, lets 0.5B to 3B models match larger models trained on reasoning traces alone.
- [A Visual Guide to Quantization](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization) · Maarten Grootendorst · Article · Free · 45 min — A diagram-heavy explanation of number formats, post-training quantization, GPTQ, GGUF and BitNet.

### Reference

- [PEFT](https://huggingface.co/docs/peft/index) · Hugging Face · Docs · Free · reference — The library that implements LoRA and other parameter-efficient methods on top of Transformers.
- [SFT Trainer](https://huggingface.co/docs/trl/sft_trainer) · Hugging Face · Docs · Free · reference — TRL's supervised fine-tuning trainer, including dataset formats for tool calling, assistant-only loss and LoRA or QLoRA through PEFT.
- [GRPO Trainer](https://huggingface.co/docs/trl/en/grpo_trainer) · Hugging Face · Docs · Free · reference — TRL's trainer for reinforcement fine-tuning with your own reward functions, with a quick start and generation through vLLM.
- [Quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart.html) · vLLM · Docs · Free · 30 min — Install vLLM, run offline batched inference and start an OpenAI-compatible server with `vllm serve`.
- [Importing a Model](https://docs.ollama.com/import) · Ollama · Docs · Free · reference — Load your own Safetensors or GGUF weights into Ollama, and quantize first with llama.cpp tools when you need to.

## Practice

1. **Make the case first.** Pick one narrow step in an agent you built, such as classifying support tickets or emitting a fixed JSON format. Measure a hosted frontier model and a prompted small open model on 50 eval examples. Done when a one-page note lists accuracy, latency and cost per 1,000 calls for each, plus a yes or no on fine-tuning.
2. **Build a training set.** Generate 300 to 1,000 examples for that step with a strong model, filter them with your eval checks, and hold out 20% for testing. Done when the data is in chat format for your target model and you have checked 30 examples by hand.
3. **Fine-tune with LoRA.** Train a 1B to 8B instruction model with QLoRA in a free Colab or Kaggle notebook, using Unsloth or TRL. Done when the tuned model beats the prompted base model on the held-out set, or you can explain why it did not.
4. **Quantize and serve.** Export the merged model to GGUF and run it in Ollama, or serve it with vLLM on a rented GPU, then add it to your gateway as one more model. Done when your agent calls it through the same OpenAI-compatible API and you have measured tokens per second. Stop or delete a rented GPU as soon as you finish, because it bills by the hour even when idle.
5. **Compare total cost.** Using your measured throughput, estimate the monthly cost of serving your expected traffic on a rented GPU versus the hosted API. Done when you can state the request volume where self-hosting breaks even, with your assumptions written down.

## Checklist

- [ ] [Must ship] Write a short decision note comparing prompting, RAG and fine-tuning for one task, backed by eval numbers.
- [ ] [Must ship] Fine-tune a small open model with LoRA or QLoRA and evaluate it on a held-out set.
- [ ] [Must ship] Serve a model with Ollama or vLLM behind an OpenAI-compatible endpoint.
- [ ] [Recommended] Route one agent step to your self-served model through the gateway.
- [ ] [Recommended] Compare a 4-bit and a 16-bit version of the same model on quality and speed.
- [ ] [Stretch] Distil agent trajectories from a strong model into a small model and measure task success.
- [ ] [Stretch] Train a small model with GRPO on a step your code can score, and compare it with your SFT model on the held-out set.

## You're ready when

- You can explain, with numbers from your own evals, why a given task should or should not be fine-tuned.
- You can describe what LoRA trains and why QLoRA fits on a single GPU.
- Your agent switches between a hosted model and your served open model by changing one config value.
- You can estimate the break-even volume between self-hosting and a per-token API.
