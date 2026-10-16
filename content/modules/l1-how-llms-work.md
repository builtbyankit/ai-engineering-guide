---
title: How LLMs work
level: L1
kind: core
hours: 8–10
summary: Explain how a large language model turns text into tokens and predicts the next one, and why that leads to limits like hallucination, context windows and knowledge cutoffs.
checked: 2026-10-16
---

## Why it matters
You will spend the rest of this guide sending text to a model and building on what comes back. Most odd behaviour you meet later has its cause here. Bills are counted in tokens. Answers change between runs because of sampling. A model states false facts with confidence because of how it was trained, and it knows nothing after its training date unless you tell it.

You do not need the maths to build agents. You need a working mental model that lets you predict failures and choose fixes. This module gives you that model through about five hours of videos and reading, plus small experiments you can run in a browser.

## What to learn
- **Tokens**: Models read and write tokens, which are chunks of text such as whole words, word pieces or punctuation. As a rough rule, one English token is about four characters, and other languages and code often use more tokens per word. Prices, limits and context sizes are all counted in tokens.
- **Next-token prediction**: A model outputs a probability for every token in its vocabulary, picks one, appends it to the text and repeats. One run of the network over the input to produce those probabilities is called a forward pass. Everything it writes, from a poem to a JSON object, comes from this loop.
- **Transformers and attention**: The transformer is the neural network design behind modern LLMs. Attention lets each token weigh which earlier tokens matter for predicting the next one, which is how meaning flows across a sentence or a whole document.
- **Pretraining, instruction tuning and RLHF**: Pretraining on huge amounts of text produces a base model that continues documents. Instruction tuning on example conversations, then reinforcement learning from human feedback (RLHF), turns it into an assistant that follows requests.
- **Context window**: The context window is the maximum number of tokens the model can consider at once, covering your input and its output. Anything outside the window does not exist for the model. Long inputs cost more, and details buried in the middle can be used less reliably.
- **Sampling**: Temperature reshapes the probabilities before a token is picked. Low values make output more predictable and high values make it more varied. Top-p sampling keeps only the smallest set of likely tokens whose probabilities add up to p.
- **Hallucination**: Models produce fluent text whether or not it is true. Training and benchmarks that reward a confident guess over "I don't know" make this worse, so you design systems that check claims against sources.
- **Reasoning models**: Some models generate "thinking" tokens before they answer, often trained with reinforcement learning on problems with checkable answers. They do better on maths, code and planning, at the cost of more tokens and slower replies.
- **Knowledge cutoff**: A model only knows what was in its training data, which stops at a date. For anything newer or private, you put the facts in the prompt or give the model a search tool.

## Resources
### Start here
- [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) · Andrej Karpathy · Video · Free · 1 h — A one-hour talk that builds the big picture: what a model file is, how pretraining and fine-tuning differ, and where the risks lie.
- [Transformers, the tech behind LLMs](https://www.youtube.com/watch?v=wjZofJX0v4M) · 3Blue1Brown · Video · Free · 27 min — The clearest animated explanation of how text flows through a transformer to become next-token probabilities.
- [Deep Dive: LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) · Andrej Karpathy · Video · Free · 3.5 h — The full pipeline from internet text and tokenization to fine-tuning, RLHF, reasoning models and hallucinations; watch it in chapters over several sittings.
### Go deeper
- [Attention in transformers, step-by-step](https://www.youtube.com/watch?v=eMlx5fFNoYc) · 3Blue1Brown · Video · Free · 26 min — Shows what queries, keys and values actually compute, so attention stops being a buzzword.
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) · Jay Alammar · Article · Free · 30 min — The classic diagram-led tour of self-attention, multi-head attention and positional encoding.
- [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) · Andrej Karpathy · Video · Free · 2–2.5 h — Builds byte-pair encoding from scratch and traces odd model behaviour, like weak spelling and arithmetic, back to tokenization.
- [Illustrating Reinforcement Learning from Human Feedback (RLHF)](https://huggingface.co/blog/rlhf) · Hugging Face · Article · Free · 30 min — Breaks RLHF into pretraining, reward model training and reinforcement learning fine-tuning, with diagrams for each step.
- [Why language models hallucinate](https://openai.com/index/why-language-models-hallucinate/) · OpenAI · Article · Free · 15 min — A 2025 explanation of how training and accuracy-only benchmarks push models to guess instead of admitting uncertainty.
- [Understanding Reasoning LLMs](https://magazine.sebastianraschka.com/p/understanding-reasoning-llms) · Sebastian Raschka · Article · Free · 45 min — What makes a reasoning model, the four main ways to build one, and when the extra cost is worth paying.
### Reference
- [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) · Georgia Tech Polo Club · Tool · Free · 30 min — Runs GPT-2 in your browser so you can type text, inspect attention and change temperature, top-k and top-p live.
- [Tiktokenizer](https://tiktokenizer.vercel.app/) · dqbd · Tool · Free · reference — Paste any text and see exactly how it splits into tokens and how many there are.
- [How to generate text: using different decoding methods for language generation with Transformers](https://huggingface.co/blog/how-to-generate) · Hugging Face · Article · Free · 30 min — Greedy search, beam search, temperature, top-k and top-p compared side by side with runnable code.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) · Vaswani et al. · Paper · Free · 1 h — The 2017 paper that introduced the transformer; skim the figures once the videos have given you the intuition.
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) · Anthropic · Docs · Free · reference — A typical provider model table, listing the context window, maximum output and knowledge cutoff for each model.

## Practice
1. **Count tokens.** Paste five texts into Tiktokenizer: an English paragraph, the same paragraph in another language, a block of Python, a JSON object and a long number. Record characters and tokens for each. Done when you can say which kinds of text cost the most tokens per character, and why.
2. **Play with sampling.** In Transformer Explainer, run one prompt at a low, a medium and a high temperature, then repeat with a small and a large top-p. Write down what changes in the probability bars and the chosen tokens. Done when you can explain temperature and top-p in two sentences each.
3. **Catch a hallucination.** Ask a chat assistant five questions about a niche topic you know well, such as your town's history or a small open-source library. Turn off web search if the app has it. Done when you have marked each answer correct, partly wrong or invented, and written a likely cause for each error.
4. **Find the cutoff.** Ask two different models about three events from the past year, again without web search. Compare what they know with the knowledge cutoff each provider publishes. Done when you have a short table of model, published cutoff, what it got right and what it made up.
5. **Explain it back.** Write a one-page explainer, in your own words, of what happens between pressing Enter and seeing a reply. Cover tokens, the forward pass, sampling and when generation stops. Done when a friend without a technical background can follow it.

## Checklist
- [ ] [Must ship] Watch the three Start here videos and write a ten-line summary of each.
- [ ] [Must ship] Complete the token counting exercise and keep the table in your notes repo.
- [ ] [Must ship] Write the one-page explainer from Practice 5.
- [ ] [Recommended] Read The Illustrated Transformer after the 3Blue1Brown videos.
- [ ] [Recommended] Collect three hallucination examples, each with a note on its likely cause.
- [ ] [Stretch] Code along with the byte-pair encoding part of Karpathy's tokenizer video.

## You're ready when
- You can explain tokens, next-token prediction and sampling without notes.
- You can say why the same prompt gives different answers and how to make output more consistent.
- You can give two reasons a model states false things and one system design fix for each.
- You can estimate the token count of a document to within a factor of two before you send it.
- You can describe what a reasoning model does differently and when its extra cost makes sense.
