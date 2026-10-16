---
title: "Better retrieval: hybrid search and reranking"
level: L2
kind: core
hours: 8–10
summary: Improve retrieval with BM25 hybrid search, reciprocal rank fusion, rerankers, query rewriting and contextual chunks, and measure which changes actually help.
checked: 2026-10-16
---

## Why it matters

Plain vector search fails in predictable ways. It misses exact terms such as error codes, product names and function names. It ranks a loosely related chunk above the one that holds the answer. It struggles when a question needs facts from two places. If the right chunk never reaches the prompt, the model cannot answer, however good the prompt is.

This module covers the standard fixes in the order most teams add them. You start with keyword search and hybrid fusion, then add reranking, then smarter queries and chunks. Each step costs latency, money or complexity, so you will measure every change against a baseline and keep only what helps.

## What to learn

- **Keyword search and BM25**: BM25 scores a document by how often the query terms appear in it, how rare those terms are across the corpus, and how long the document is. It is strong on exact matches and needs no model.
- **Hybrid search**: Run keyword and vector search side by side and merge the results. This catches both exact terms and paraphrases, and it is often the cheapest large gain you can make.
- **Reciprocal rank fusion (RRF)**: Give each document a score of 1 / (k + rank) in each result list and add the scores up. RRF uses ranks only, so you never have to compare BM25 scores with cosine scores. A common default for k is 60.
- **Rerankers**: A cross-encoder reads the query and one candidate together and scores their relevance. This is more accurate than comparing two separate embeddings but much slower, so retrieve a wide set cheaply (for example 50), rerank it, and keep the top few.
- **Choosing a reranker**: Options include hosted APIs such as Cohere Rerank and open cross-encoder models you run with Sentence Transformers. Compare them on accuracy with your data, latency, cost and whether your data may leave your servers.
- **Query rewriting and HyDE**: An LLM can clean up a vague question, split it into sub-questions or write several variants to search with. HyDE asks the model for a hypothetical answer and embeds that, because an answer looks more like a document than a question does.
- **Contextual retrieval**: Before indexing, have an LLM prepend a short note to each chunk saying where it sits in its document. Anthropic reported that contextual embeddings plus contextual BM25 cut retrieval failures by 49%, and adding reranking raised that to 67%.
- **Parent/child chunks**: Index small chunks for precise matching, then hand the model their larger parent section. Retrieval stays sharp and the model still gets enough surrounding context.
- **Multi-hop questions**: Some questions need facts from two places ("Which team owns the service that failed last week?"). Decompose the question, retrieve for each step, or let an agent search repeatedly, which Level 3 covers in [The agent loop](#l3-agent-loop).

## Resources

### Start here

- [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) · Anthropic · Article · Free · 25 min — Shows hybrid search, reranking and chunk context working together, with measured failure rates for each added step.
- [Hybrid Search Explained](https://weaviate.io/blog/hybrid-search-explained) · Weaviate · Article · Free · 10 min — A short explanation of sparse versus dense vectors and how RRF and score-based fusion merge them, with a worked example.
- [Rerankers and Two-Stage Retrieval](https://www.pinecone.io/learn/series/rag/rerankers/) · Pinecone · Article · Free · 30 min — Explains bi-encoders versus cross-encoders and shows results before and after adding an open reranker.

### Go deeper

- [Practical BM25, Part 2: The BM25 Algorithm and its Variables](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) · Elastic · Article · Free · 30 min — Walks through each part of the BM25 formula and shows what the k1 and b parameters do to scores.
- [Advanced Retrieval for AI with Chroma](https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/) · DeepLearning.AI · Course · Free tier · 1 h — Notebooks on query expansion, cross-encoder reranking and embedding adapters, plus spotting queries that retrieve poorly.
- [Retrieve & Re-Rank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) · Sentence Transformers · Docs · Free · 20 min — The two-stage pattern with lexical or dense retrieval followed by an open cross-encoder you can run locally.
- [Precise Zero-Shot Dense Retrieval without Relevance Labels](https://arxiv.org/abs/2212.10496) · Gao et al. · Paper · Free · 1 h — The HyDE paper; the method section explains why embedding a generated answer can beat embedding the question.
- [Auto Merging Retriever](https://developers.llamaindex.ai/python/examples/retrievers/auto_merging_retriever/) · LlamaIndex · Tutorial · Free · 30 min — A worked parent/child example whose own evaluation finds little gain on its test set, a useful reminder to measure.

### Reference

- [Reciprocal rank fusion](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion) · Elastic · Docs · Free · reference — The RRF formula and its rank constant, stated precisely.
- [Hybrid Queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) · Qdrant · Docs · Free · reference — How to run dense and sparse searches in one request and fuse them with RRF or score-based fusion.
- [An Overview of Cohere's Rerank Model](https://docs.cohere.com/docs/rerank-overview) · Cohere · Docs · Free · reference — Request and response format for a hosted reranker, plus advice on reranking structured documents.
- [Cross Encoder Usage](https://sbert.net/docs/cross_encoder/usage/usage.html) · Sentence Transformers · Docs · Free · reference — How to load an open cross-encoder, score query-passage pairs, rank passages and interpret raw scores.
- [bm25s](https://github.com/xhluca/bm25s) · xhluca · Repo · Free · reference — A fast, lightweight BM25 library for Python, handy when your vector store has no keyword search.

## Practice

1. **BM25 baseline**: Index your RAG corpus with bm25s or Postgres full-text search. On 20 labelled questions, compare how often the right chunk appears in the top 5 for BM25 alone and for vector search alone. Done when you can name questions that each method wins.
2. **Hybrid with RRF**: Write a short RRF function that merges the two lists. Done when the hybrid top-5 hit rate matches or beats the better single method, or you can explain why it does not.
3. **Add a reranker**: Retrieve 30 to 50 candidates with hybrid search and rerank them with an open cross-encoder. Record the top-5 hit rate and the added latency per query. Done when you can decide, with numbers, whether the reranker earns its cost.
4. **Rewrite or contextualise**: Try one of HyDE, multi-query rewriting or contextual chunk notes. Done when you report its effect on the same 20 questions, including the extra LLM calls it needs.

## Checklist

- [ ] [Must ship] Add BM25 or full-text search next to vector search for your corpus.
- [ ] [Must ship] Merge both result lists with reciprocal rank fusion.
- [ ] [Must ship] Add a reranking step and measure its effect on hit rate and latency.
- [ ] [Recommended] Test one query-side technique (rewriting, multi-query or HyDE) against the baseline.
- [ ] [Recommended] Try contextual chunk notes or parent/child retrieval on documents with many similar sections.
- [ ] [Stretch] Build a small multi-hop question set and handle it with question decomposition.

## You're ready when

- You can explain BM25, RRF and cross-encoder reranking, and say when each one helps.
- Your retriever combines keyword and vector search, then reranks, behind one function.
- You have a table showing what each technique did to top-5 hit rate and latency on your questions.
- You can describe contextual retrieval and parent/child chunks and decide whether your corpus needs them.
