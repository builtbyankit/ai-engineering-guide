---
title: Evaluating RAG
level: L2
kind: core
hours: 6–8
summary: Measure retrieval and answer quality separately with recall@k, MRR, nDCG, faithfulness and answer relevance, using a question set built from your own corpus.
checked: 2026-10-16
---

## Why it matters

A RAG system can fail in two places. Retrieval can miss the right passage, or generation can ignore, misread or embellish a passage it was given. If you only score the final answer, you cannot tell which half to fix, and you may spend days rewriting prompts when the real problem is chunking.

This module teaches you to measure each half on its own. Retrieval metrics come from decades of search research and are cheap and exact once you have labelled questions. Answer metrics such as faithfulness usually need an LLM judge, so you will learn what they measure and how far to trust them. It builds on [Your first evals](#l1-first-evals); [Evals in depth](#l5-evals-in-depth) returns to judge calibration and CI later.

## What to learn

- **Two halves**: Score retrieval (did the right chunks come back?) and generation (did the answer use them correctly?) separately. Then check end-to-end correctness on a smaller set.
- **Recall@k**: The share of questions whose relevant chunk appears in the top k results. Track it first, because the model cannot use a chunk it never sees.
- **MRR**: Mean reciprocal rank averages 1 / (rank of the first relevant result) across questions. It rewards putting the right chunk near the top.
- **nDCG**: Normalized discounted cumulative gain supports graded relevance (very relevant, somewhat relevant) and counts results lower in the list for less. Use it when several chunks matter for one question.
- **Faithfulness or groundedness**: Whether every claim in the answer is supported by the retrieved context. Tools usually measure it with an LLM that splits the answer into claims and checks each one.
- **Answer relevance**: Whether the answer addresses the question that was asked. A perfectly faithful answer can still miss the point.
- **Building a question set**: Write questions from real or likely user needs and label the chunk or page that answers each. Generate extra candidates with an LLM, one per sampled chunk, then review and edit them by hand. Add questions the corpus cannot answer, to test refusals.
- **Tools**: Ragas, DeepEval and TruLens offer ready-made RAG metrics, and ranx computes classic ranking metrics. A plain Python script is enough to start; adopt a tool when it saves you effort.
- **Error analysis**: Read failing cases one by one, tag why each failed (retrieval miss, wrong ranking, unfaithful answer, should have refused, bad question) and count the tags. Fix the largest group first, then measure again.

## Resources

### Start here

- [Evaluation Metrics for Search and Recommendation Systems](https://weaviate.io/blog/retrieval-evaluation-metrics) · Weaviate · Article · Free · 10 min — Short, clear definitions of precision@k, recall@k, MRR, MAP and nDCG with Python examples.
- [Systematically Improving Your RAG](https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/) · Jason Liu · Article · Free · 30 min — Practical advice on synthetic questions per chunk, tracking retrieval precision and recall, and clustering queries to find weak spots.
- [Evaluate a simple RAG system](https://docs.ragas.io/en/stable/getstarted/rag_eval/) · Ragas · Tutorial · Free · 45 min — Builds a tiny RAG app and scores it on context recall, faithfulness and factual correctness.

### Go deeper

- [Evaluation Measures in Information Retrieval](https://www.pinecone.io/learn/offline-evaluation/) · Pinecone · Article · Free · 45 min — Longer worked examples of each ranking metric, with the pros and cons of order-aware and order-unaware measures.
- [Building and Evaluating Advanced RAG](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/) · DeepLearning.AI · Course · Free tier · 2 h — Introduces the RAG triad (context relevance, groundedness, answer relevance) and improves a pipeline using it.
- [Retrieval Augmented Generation](https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/retrieval_augmented_generation/guide.ipynb) · Anthropic · Tutorial · Free · 2 h — A notebook that builds RAG in plain code and tracks precision, recall, MRR and end-to-end accuracy as it adds summaries and reranking.
- [RAG Evaluation](https://deepeval.com/guides/guides-rag-evaluation) · DeepEval · Docs · Free · 30 min — Maps each retriever and generator metric to the pipeline setting it helps you tune, and shows them running as tests.
- [RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/) · TruLens · Docs · Free · 10 min — A one-page explanation of three checks that together catch most RAG hallucinations.
- [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) · Hamel Husain and Shreya Shankar · Article · Free · self-paced — A long FAQ on error analysis and judge design, including test sets built from answerable and unanswerable questions.

### Reference

- [List of available metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) · Ragas · Docs · Free · reference — Definitions of context precision, context recall, faithfulness, response relevancy and related metrics.
- [Testset Generation for RAG](https://docs.ragas.io/en/stable/getstarted/rag_testset_generation/) · Ragas · Docs · Free · reference — Generates single-hop and multi-hop questions from your documents as a draft set to review.
- [Ragas: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217) · Es et al. · Paper · Free · 45 min — The paper behind reference-free faithfulness and relevance scoring, useful for knowing what the scores assume.
- [ranx](https://github.com/AmenRa/ranx) · AmenRa · Repo · Free · reference — Fast ranking metrics (recall, MRR, MAP, nDCG) checked against TREC Eval, plus fusion methods such as RRF.

## Practice

1. **Label a question set**: For your Level 2 corpus, write 20 questions by hand and generate 20 more with an LLM, one per random chunk. Review them, keep the best 30 with their correct chunk or page, and add 5 unanswerable questions. Done when the set is saved as JSON or CSV.
2. **Retrieval metrics script**: Compute recall@5, recall@10 and MRR for your retriever. Done when one command prints the numbers and lists the questions that missed.
3. **Answer metrics**: Score faithfulness and answer relevance with Ragas or DeepEval on the same set, then hand-check 10 of the judgements. Done when you can say how often the judge agreed with you.
4. **Error analysis**: Read every failure and tag its cause. Done when you have counts per tag and have chosen the one change to make first.
5. **Before and after**: Apply that change (for example adding a reranker) and rerun everything. Done when you have a before/after table for retrieval and answer metrics.

## Checklist

- [ ] [Must ship] Build a labelled set of at least 30 questions with source chunks, plus at least 5 unanswerable ones.
- [ ] [Must ship] Report recall@k and MRR for your retriever from a single script.
- [ ] [Must ship] Score faithfulness and answer relevance on the same questions and spot-check the judge by hand.
- [ ] [Recommended] Tag every failure by cause and fix the largest group first.
- [ ] [Recommended] Save results per run to a file so you can compare versions.
- [ ] [Stretch] Add nDCG with graded labels for questions that have several relevant chunks.

## You're ready when

- You can explain recall@k, MRR, nDCG, faithfulness and answer relevance, and which half of the system each one measures.
- Your eval script prints retrieval and answer metrics for a labelled question set in one run.
- You can point to a failure group and show the metric change after you fixed it.
- You can say where an LLM judge disagreed with you and how you handled it.
