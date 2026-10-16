---
title: Knowledge graphs and GraphRAG
level: L2
kind: optional
hours: 5–6
summary: Decide when graph-based retrieval beats chunk search, run Microsoft GraphRAG or LightRAG on a small corpus, and query a graph with Neo4j and Cypher.
checked: 2026-10-16
---

## Why it matters

Chunk-based RAG answers local questions well, such as "what is the refund window?" It struggles with global questions that need the whole corpus, such as "what are the main themes across these 200 interview notes?" It also struggles with questions about how entities connect. No single chunk holds those answers.

GraphRAG approaches use an LLM to extract entities and relationships into a knowledge graph, group related entities into communities and summarise each group. Queries can then read the summaries or walk the graph. The price is indexing cost, because building the graph takes many LLM calls and can cost far more than embedding chunks. This optional module helps you judge when that cost pays off.

## What to learn

- **Local versus global questions**: Local questions name specific things and suit vector RAG. Global questions ask about patterns across everything, which is where graph summaries help.
- **Knowledge graphs**: Nodes are entities (people, products, services) and edges are typed relationships between them; both can carry properties. A graph stores multi-hop connections as explicit edges you can follow.
- **GraphRAG indexing**: Microsoft GraphRAG splits text into units, uses an LLM to extract entities, relationships and claims, clusters the graph into a hierarchy of communities and writes a summary for each community.
- **GraphRAG query modes**: Global search answers whole-corpus questions from community summaries. Local search starts from entities named in the question and gathers their neighbours. DRIFT search mixes the two, and basic search is ordinary vector RAG.
- **LightRAG-style approaches**: Lighter systems keep both a graph and vector embeddings and retrieve at two levels, specific entities and broader themes. They aim for much of the benefit at a lower indexing cost.
- **Neo4j and Cypher**: Neo4j is a widely used graph database. Cypher queries match patterns of nodes and relationships, and Neo4j also has vector indexes, so one store can serve both kinds of retrieval.
- **Cost trade-offs**: Full GraphRAG indexing is LLM-heavy, so index a small sample first and estimate cost before running everything. Microsoft's LazyGraphRAG defers LLM work to query time and reports indexing cost of about 0.1% of full GraphRAG.
- **When to skip it**: If most questions are local lookups, hybrid search plus reranking from [Better retrieval](#l2-advanced-retrieval) is cheaper and simpler to run. Test with your real questions before you commit.

## Resources

### Start here

- [Welcome to GraphRAG](https://microsoft.github.io/graphrag/) · Microsoft · Docs · Free · 20 min — The official overview of GraphRAG indexing and its global, local, DRIFT and basic search modes.
- [LazyGraphRAG: Setting a new standard for quality and cost](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/) · Microsoft Research · Article · Free · 20 min — Lays out the indexing and query costs of full GraphRAG against a cheaper variant, on both local and global questions.
- [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/) · Neo4j GraphAcademy · Course · Free · 1 h — Graph thinking, nodes, relationships and first Cypher queries in seven short lessons.

### Go deeper

- [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130) · Edge et al. · Paper · Free · 1.5 h — The GraphRAG paper, showing why community summaries beat chunk RAG on whole-corpus sensemaking questions.
- [Knowledge Graphs for RAG](https://www.deeplearning.ai/short-courses/knowledge-graphs-rag/) · DeepLearning.AI · Course · Free tier · 2 h — Builds a knowledge graph from SEC filings in Neo4j, adds a vector index and writes Cypher that feeds context to an LLM.
- [Neo4j & GenerativeAI Fundamentals](https://graphacademy.neo4j.com/courses/genai-fundamentals/) · Neo4j GraphAcademy · Course · Free · 2 h — Compares vector RAG with GraphRAG and builds Python retrievers against Neo4j, including a text-to-Cypher retriever.
- [GraphRAG Pattern Catalog](https://graphrag.com/) · Neo4j · Docs · Free · self-paced — A catalog of graph models and retriever patterns with concept pages, how-to guides and a glossary.

### Reference

- [microsoft/graphrag](https://github.com/microsoft/graphrag) · Microsoft · Repo · Free · reference — The open-source pipeline; its README warns that indexing can be expensive and advises starting small.
- [GraphRAG Indexing](https://microsoft.github.io/graphrag/index/overview/) · Microsoft · Docs · Free · reference — What the indexing pipeline extracts and the output tables it writes.
- [LightRAG](https://github.com/HKUDS/LightRAG) · HKUDS · Repo · Free · reference — A lighter graph-plus-vector RAG framework with local, global, hybrid and mix query modes and Neo4j or Postgres backends.
- [LightRAG: Simple and Fast Retrieval-Augmented Generation](https://arxiv.org/abs/2410.05779) · Guo et al. · Paper · Free · 1 h — The paper behind LightRAG's dual-level retrieval over entities and broader themes.
- [GraphRAG for Python](https://neo4j.com/docs/neo4j-graphrag-python/current/) · Neo4j · Docs · Free · reference — The official Neo4j package for building knowledge graphs and retrievers from Python.

## Practice

1. **Question audit**: Write 10 questions about a corpus you know (for example 30 meeting notes or the chapters of a novel) and label each local or global. Done when you can say which ones your Level 2 hybrid pipeline answered poorly.
2. **Small GraphRAG run**: Index 10 to 20 documents with Microsoft GraphRAG or LightRAG using a low-cost model, and record tokens used. Done when you have answers to your global questions and a cost-per-document figure.
3. **Compare**: Ask the same 10 questions through your hybrid RAG and the graph system. Done when you have a side-by-side table with your verdict on each answer and the reason.
4. **Cypher by hand**: Load a small graph (for example people, teams and the services they own) into Neo4j and write three Cypher queries, including one that follows two relationships. Done when every query returns what you expect.

## Checklist

- [ ] [Must ship] Classify a question set into local and global questions.
- [ ] [Must ship] Index a small corpus with GraphRAG or LightRAG and record the indexing cost.
- [ ] [Must ship] Compare graph answers with your hybrid RAG answers on the same questions.
- [ ] [Recommended] Write and run Cypher queries, including a multi-hop pattern, on a small Neo4j graph.
- [ ] [Stretch] Estimate the cost of indexing your full corpus and write a one-paragraph go or no-go decision.

## You're ready when

- You can explain the difference between local and global questions and why chunk RAG struggles with global ones.
- You can describe how GraphRAG builds community summaries and uses them at query time.
- You have measured what a graph index cost you and what it improved.
- You can decide, with evidence, whether a project needs graph retrieval.
