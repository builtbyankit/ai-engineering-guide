---
title: Just enough machine learning
level: L0
kind: core
hours: 6–8
summary: Explain in plain words what a model is, how neural networks learn, why models overfit, what embeddings are and where transformers fit.
checked: 2026-10-16
---

## Why it matters

You will rarely train a model when you build agents, yet you will use one in every request. A working picture of how models are made explains much of their behaviour. Why do they do well on familiar examples and badly on new ones? Why can a list of numbers capture what a sentence means? Why does a model predict text one piece at a time? These questions come up every week once you start building.

This module gives you that picture through visual, intuitive material with almost no math. It sets up [How LLMs work](#l1-how-llms-work) in Level 1 and [Embeddings and vector search](#l2-embeddings-vector-search) in Level 2, which both build directly on these ideas.

## What to learn

- **What a model is**: a function with many adjustable numbers, called parameters or weights, that maps an input to an output. Training sets those numbers; the code around them stays the same.
- **Training vs inference**: training adjusts the weights using many examples and costs a lot of compute, usually once. Inference runs the finished model on a new input, which is what happens on every API call you make.
- **Loss and gradient descent**: the loss is a number that measures how wrong the model is. Gradient descent nudges every weight a little in the direction that lowers the loss, then repeats many thousands of times.
- **Neural networks**: layers of simple units that each compute a weighted sum and pass it through a non-linear function. Stacking layers lets the network learn complex patterns, and backpropagation works out how to nudge each weight.
- **Supervised vs self-supervised learning**: supervised learning uses examples labelled by people, such as emails marked spam or not spam. Self-supervised learning creates labels from the data itself, such as predicting the next word, which is how language models learn from huge amounts of text.
- **Overfitting**: a model that memorises its training data scores well on it and badly on new data. You catch it by holding back a test set the model never sees in training, a habit you will reuse when you build evals.
- **Embeddings**: a list of numbers (a vector) that represents a word, sentence or image so that similar meanings land close together. Comparing vectors gives you semantic search, clustering and recommendations.
- **Transformers at a high level**: the neural network design behind modern LLMs. Its key idea, attention, lets each word look at the words before it to decide what matters for predicting the next one.
- **Pretraining and fine-tuning**: a model first learns general patterns from a large corpus, then trains further on a smaller dataset for a specific task. Most of what you build will use models that someone else pretrained and tuned.

## Resources

### Start here

- [Neural networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) · 3Blue1Brown · Video · Free · 1.5 h — Animated explanations of neurons, gradient descent and backpropagation; watch chapters 1 to 3, then chapter 5 on transformers.
- [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) · Google · Course · Free · 2–3 h — Take the neural networks and embeddings modules and the overfitting pages of the datasets module, each with interactive exercises.
- [Embeddings: What they are and why they matter](https://simonwillison.net/2023/Oct/23/embeddings/) · Simon Willison · Article · Free · 30–45 min — A practical explanation of embeddings and cosine similarity with real uses such as related content and semantic search.

### Go deeper

- [A Neural Network Playground](https://playground.tensorflow.org/) · TensorFlow · Tool · Free · 30 min — Train a tiny network in your browser and watch how layers, learning rate and noisy data change what it learns.
- [How do Transformers work?](https://huggingface.co/learn/llm-course/chapter1/4) · Hugging Face · Course · Free · 30 min — Explains self-supervised pretraining, transfer learning and encoder versus decoder models in plain language.
- [Practical Deep Learning for Coders](https://course.fast.ai/) · fast.ai · Course · Free · self-paced — A code-first course of nine lessons of about 90 minutes each; lesson 1 alone shows a model being trained and used.
- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) · Andrej Karpathy · Course · Free · self-paced — Builds a neural network and then a small GPT from scratch in Python, for when you want to see every moving part.

### Reference

- [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary) · Google · Docs · Free · reference — Short definitions of ML terms with links back to the crash course, handy when docs use unfamiliar jargon.
- [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) · Georgia Tech Polo Club · Tool · Free · reference — Runs a small GPT-2 model in your browser so you can type a prompt and watch attention and next-token probabilities.

## Practice

1. **Watch a network learn.** In the Neural Network Playground, train on the spiral dataset and record the settings that give your lowest test loss. Then add noise and extra neurons until the training loss drops while the test loss rises. Done when you can explain that gap in two sentences.
2. **Gradient descent by hand.** In plain Python with no ML libraries, fit `y = w * x + b` to 20 points you generate with known values of `w` and `b`. Nudge both values to reduce the mean squared error and print the loss every 100 steps. Done when the loss falls steadily and the learned values land close to the true ones.
3. **See overfitting.** Generate 30 noisy points from a smooth curve and split them into 20 training and 10 test points. Fit polynomials of degree 1, 3 and 12 with `numpy.polyfit` and compare training and test error. Done when you can point to the model that overfits and explain how you know.
4. **Explore embeddings.** Embed 20 short sentences about four topics (recipes, sport, programming, weather) with an open model through the sentence-transformers library or any provider's embeddings API. Compute cosine similarity and print each sentence's nearest neighbour. Done when most neighbours share a topic and you can explain the misses.
5. **Explain it back.** Write a note of about 300 words, in your own words, on training vs inference, overfitting, embeddings and what a transformer does. Done when a friend who does not code can follow it.

## Checklist

- [ ] [Must ship] Watch the first three 3Blue1Brown chapters and summarise gradient descent in three sentences.
- [ ] [Must ship] Implement gradient descent for a straight line in plain Python.
- [ ] [Must ship] Show overfitting with a held-out test set and explain what you see.
- [ ] [Must ship] Compute embedding similarities for a small set of sentences.
- [ ] [Recommended] Complete the embeddings module of Google's crash course, including its exercises.
- [ ] [Stretch] Watch the first Zero to Hero lecture and build its small autograd engine alongside it.

## You're ready when

- You can explain training vs inference and why inference is what you pay for on each API call.
- You can describe gradient descent and overfitting to a non-programmer without equations.
- Your embedding script finds similar sentences, and you can say why cosine similarity suits the job.
- You can say in two sentences what a transformer is and what attention does.
