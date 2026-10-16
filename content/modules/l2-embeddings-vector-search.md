---
title: Embeddings and vector search
level: L2
kind: core
hours: 8–10
summary: Turn text into embeddings, search them by meaning, and choose and run a vector store with metadata filters for a real document collection.
checked: 2026-10-16
---

## Why it matters

An agent that answers from your documents first has to find the right passage. Keyword search misses paraphrases. A user asks "how do I get my money back" and the page says "refund policy". Embeddings fix much of this by turning text into vectors where similar meanings sit close together, so you can search by meaning.

This module gives you the search layer that later RAG and memory features sit on. You will learn what an embedding model does, how to compare models with evidence, how vector indexes trade accuracy for speed, and how to choose between a Postgres extension, an embedded store, a dedicated vector database and a plain index library. Get this layer right and the rest of the level is tuning. Get it wrong and no prompt will rescue the answers.

## What to learn

- **Embeddings**: An embedding model maps a piece of text to a fixed-length list of numbers (for example 1,536 of them). Texts with similar meaning get vectors that point in similar directions.
- **Choosing an embedding model**: Models differ in quality, languages, maximum input length, vector size and price. The MTEB leaderboard scores many models on retrieval and other tasks, so use it to build a shortlist, then test the shortlist on your own data.
- **Queries versus documents**: A short question and a long passage are different kinds of text. Some models expect a different prefix, task type or method for each, so read the model card before you embed anything.
- **Cosine similarity**: The standard score for how close two vectors are, based on the angle between them. On normalized vectors it equals the dot product, which is why many stores offer both.
- **Exact versus approximate search**: Comparing a query with every stored vector (flat or brute-force search) is exact but slow at scale. Approximate nearest neighbour (ANN) indexes give up a little recall (they sometimes miss a few of the true nearest vectors) for a large speed gain.
- **HNSW and IVF**: HNSW builds a layered graph that a search walks towards the nearest vectors; it is fast and accurate but uses a lot of memory. IVF groups vectors into clusters and searches only the closest few; it builds faster and uses less memory. Both have a query-time setting that trades recall for speed.
- **Vector stores**: pgvector adds vector columns and indexes to Postgres. Chroma is an easy store for local prototypes. Qdrant is a dedicated vector database with rich filtering. FAISS is a library of indexes that you manage yourself.
- **Picking a store**: Start with what you already run. If you have Postgres, pgvector keeps vectors next to the rest of your data. For a quick local prototype, Chroma is enough. Move to a dedicated database when you need scale or features your current store lacks.
- **Metadata filtering**: Store fields such as source, date, language or owner with each vector. Filters restrict a search ("only version 3 docs", "only this user's files"), which also matters for access control.

## Resources

### Start here

- [Embeddings: What they are and why they matter](https://simonwillison.net/2023/Oct/23/embeddings/) · Simon Willison · Article · Free · 1 h — A clear, example-led tour of embeddings, related-content search and RAG, with a 38-minute talk video on the same page.
- [Vector embeddings](https://developers.openai.com/api/docs/guides/embeddings) · OpenAI · Docs · Free · 30 min — Shows how to call an embedding API, rank results with cosine similarity and shorten vectors with the dimensions parameter.
- [What is a Vector Database & How Does it Work?](https://www.pinecone.io/learn/vector-database/) · Pinecone · Article · Free · 30 min — Explains indexing, similarity measures and pre- versus post-filtering in plain terms; skim past the product calls to action.

### Go deeper

- [Vector Databases: from Embeddings to Applications](https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/) · DeepLearning.AI · Course · Free tier · 1 h — A short video course with notebooks on ANN algorithms, sparse versus dense search and vector databases for RAG.
- [Nearest Neighbor Indexes for Similarity Search](https://www.pinecone.io/learn/series/faiss/vector-indexes/) · Pinecone · Article · Free · 45 min — Compares flat, LSH, HNSW and IVF indexes in FAISS, ending with a table of memory, speed and recall.
- [Hierarchical Navigable Small Worlds (HNSW)](https://www.pinecone.io/learn/series/faiss/hnsw/) · Pinecone · Article · Free · 45 min — Builds HNSW up from skip lists and small-world graphs, then measures how its settings change recall, speed and memory.
- [Semantic Search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) · Sentence Transformers · Docs · Free · 20 min — Explains symmetric versus asymmetric search and how to embed queries and documents with an open model on your own machine.
- [Embeddings](https://ai.google.dev/gemini-api/docs/embeddings) · Google · Docs · Free · 20 min — A second provider's view of task types and output sizes, and a clear warning that switching models means re-embedding everything.

### Reference

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) · Hugging Face · Tool · Free · reference — Filter embedding models by task, language and size to build a shortlist before you test on your own data.
- [pgvector](https://github.com/pgvector/pgvector) · pgvector · Repo · Free · reference — The README covers distance operators, HNSW and IVFFlat options, filtered queries and hybrid search inside Postgres.
- [Filtering](https://qdrant.tech/documentation/concepts/filtering/) · Qdrant · Docs · Free · reference — Boolean filter clauses, range and full-text conditions, and why you should index the payload fields you filter on.
- [Getting Started](https://docs.trychroma.com/docs/overview/getting-started) · Chroma · Docs · Free · 15 min — A short quickstart for a local collection that embeds and queries documents for you.
- [Guidelines to choose an index](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index) · FAISS · Docs · Free · reference — A decision guide for picking a FAISS index from dataset size, memory budget and whether you need exact results.

## Practice

1. **Similarity by hand**: Embed 20 short recipe titles (for example "quick vegan pasta" and "slow-cooked beef stew") with one model. Print the top 3 neighbours for five queries using cosine similarity in NumPy. Done when you can explain one surprising match.
2. **Compare two models**: Write 15 questions about a small corpus (for example 100 support tickets or 50 paper abstracts) and mark the correct document for each. Compare two models from your MTEB shortlist by how often the right document lands in the top 5. Done when you have a two-row results table.
3. **Exact versus approximate**: Load at least 50,000 vectors into FAISS (embed a public dataset or use random vectors). Compare a flat index with HNSW on query time and on how many of the flat top-10 results HNSW also returns, at two search settings. Done when you can state the trade-off in numbers.
4. **Store with filters**: Put the corpus from exercise 2 into pgvector, Chroma or Qdrant with `source` and `date` metadata. Run the same query with and without a filter such as "only 2025 documents". Done when the filtered query never returns an out-of-range document.

## Checklist

- [ ] [Must ship] Write a script that embeds a folder of text files and answers similarity queries from the command line.
- [ ] [Must ship] Measure top-5 hit rate for at least two embedding models on 15 or more labelled questions.
- [ ] [Must ship] Store vectors with metadata in pgvector, Chroma or Qdrant and run a filtered query.
- [ ] [Recommended] Benchmark flat versus HNSW search on speed and recall at a size where the difference shows.
- [ ] [Recommended] Write a half-page note on which store you would pick for a 10,000-document project and why.
- [ ] [Stretch] Try a shorter vector size (for example 256 dimensions) and report the change in hit rate and storage.

## You're ready when

- You can explain embeddings, cosine similarity and approximate search to a friend without notes.
- You can pick an embedding model with evidence from your own small test, using the leaderboard only to shortlist.
- You can describe the trade-offs between HNSW and IVF, and between pgvector, Chroma, Qdrant and FAISS.
- Your code filters search results by metadata, and you can say why that matters for access control.
