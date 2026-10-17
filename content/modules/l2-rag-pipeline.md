---
title: Building a RAG pipeline
level: L2
kind: core
hours: 10–12
summary: Build a RAG pipeline from document parsing to cited answers that refuse when the context lacks support, and judge when RAG beats long context or fine-tuning.
checked: 2026-10-16
---

## Why it matters

Models do not know your documents, and they will confidently invent answers about them. Retrieval-augmented generation (RAG) searches your data first and puts the best passages into the prompt, so the model answers from evidence you control. It is the most common pattern in LLM applications, and agents follow the same steps whenever they call a search tool.

A RAG system is a pipeline, and each stage can quietly spoil the answer. Bad PDF parsing loses tables. Poor chunking splits an answer in half. A weak prompt lets the model ignore the context or skip the citation. This module walks the whole chain once, in plain code first, so you know where to look when answers go wrong.

## What to learn

- **The RAG loop**: Index once (load, split, embed, store). Then, for each question, retrieve the top passages, assemble a prompt and generate an answer. The 2020 paper by Lewis et al. named the idea; most systems today use this simpler retrieve-then-prompt form.
- **Loading and parsing**: HTML, Markdown and plain text are easy. PDFs are hard because columns, headers, footers and tables get scrambled. Tools such as Docling or PyMuPDF4LLM convert PDFs to Markdown that keeps headings and tables.
- **Chunking**: Split documents into passages small enough to match precisely but large enough to make sense alone. Start with structure-aware splitting (by heading, then paragraph) at a few hundred tokens with a small overlap, and tune from there with measurements.
- **Chunk metadata**: Keep the source file, title, heading path, page number and URL with every chunk. You need them for citations, filters and debugging.
- **Prompt assembly**: Wrap each retrieved chunk in clear delimiters with an id, then add the question and instructions. Models still use long inputs less reliably than short ones (see context rot in [Memory and context engineering](#l3-memory-context)), so send a few well-ranked chunks instead of dozens.
- **Citations**: Ask the model to cite chunk ids for each claim and return structured output you can validate (see [Structured outputs](#l1-structured-outputs)). Some APIs, such as Anthropic's Citations feature, return the cited passages for you.
- **Refusing**: Instruct the model to say it cannot find the answer when the context does not support one, and test that it does. A wrong answer with a confident citation does more harm than "I don't know".
- **Frameworks versus plain code**: LlamaIndex and LangChain supply loaders, splitters, retrievers and integrations. Build your first pipeline as a short plain Python script so you understand each step, then adopt a framework where it saves real work.
- **RAG, long context or fine-tuning**: If the whole corpus fits comfortably in your model's context window and the cost per call is acceptable, try sending all of it with prompt caching, where the provider reuses an unchanged prompt prefix at a discount (see [Reliability, latency and cost](#l6-reliability-cost)). Use RAG for larger or frequently changing data. Fine-tuning shapes behaviour and format and is a poor way to add facts.

## Resources

### Start here

- [Levels of Complexity: RAG Applications](https://jxnl.co/writing/2024/02/28/levels-of-complexity-rag-applications/) · Jason Liu · Article · Free · 45 min — A staged path from a basic chunk-embed-answer script to citations, observability and evals, with advice on what to master first.
- [Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval) · LangChain · Docs · Free · 20 min — Names the building blocks (loaders, splitters, embeddings, stores, retrievers) and contrasts fixed two-step RAG with agentic RAG.
- [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/) · Pinecone · Article · Free · 30 min — Compares fixed-size, recursive, structure-based and semantic chunking, plus chunk expansion at query time.

### Go deeper

- [Learn RAG from Scratch – Python AI Tutorial from a LangChain Engineer](https://www.freecodecamp.org/news/mastering-rag-from-scratch/) · freeCodeCamp · Video · Free · 2.5 h — Lance Martin builds indexing, retrieval and generation step by step, then covers query translation, routing and adaptive RAG.
- [Introduction to RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/) · LlamaIndex · Docs · Free · 15 min — Defines the five stages of a RAG app and the vocabulary (nodes, retrievers, response synthesizers) used across LlamaIndex.
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations) · Anthropic · Docs · Free · 20 min — API-level citations over plain text, PDFs and your own chunks, with a response format you can render as footnotes.
- [Optimizing LLM Accuracy](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) · OpenAI · Docs · Free · 30 min — A clear mental model for when to reach for prompting, RAG or fine-tuning, and why they fix different problems.
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) · Liu et al. · Paper · Free · 1 h — The 2023 evidence that models miss facts placed mid-context; newer models do better, so measure your own model before you tune chunk count and order around it.
- [Build a custom RAG agent with LangGraph](https://docs.langchain.com/oss/python/langgraph/agentic-rag) · LangChain · Tutorial · Free · 1.5 h — Turns retrieval into a tool an agent chooses to call, with document grading and question rewriting; a preview of Level 3.

### Reference

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) · Lewis et al. · Paper · Free · 1 h — The 2020 paper that coined the term; the introduction and method sections are enough for context.
- [Docling](https://github.com/docling-project/docling) · Docling Project · Repo · Free · reference — An open-source parser that turns PDFs, Office files and HTML into Markdown or JSON, with LlamaIndex and LangChain integrations.
- [PyMuPDF4LLM](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/) · PyMuPDF · Docs · Free · reference — A lightweight PDF-to-Markdown converter with layout analysis and OCR for scanned pages.

## Practice

1. **RAG in plain Python**: Pick 20 to 50 pages of public documentation, such as a library's user guide. Write load, chunk, embed, retrieve and answer as separate functions with no framework. Done when it answers five test questions and prints the chunk ids it used.
2. **Parse a hard PDF**: Convert a PDF with tables or two columns (a research paper or an invoice) with plain text extraction, then with Docling or PyMuPDF4LLM. Done when you can show one table that broke with the first method and survived the second.
3. **Chunk size sweep**: Run your pipeline with three chunk sizes (for example 200, 500 and 1,000 tokens) on 15 questions with known source pages. Done when you have a small table of how often the right page was retrieved.
4. **Cite or refuse**: Change the prompt so every claim cites a chunk id and the model replies "I can't find this in the documents" when unsupported. Add five questions the corpus cannot answer. Done when all five are refused and every cited id exists.
5. **Framework port**: Rebuild exercise 1 with LlamaIndex or LangChain. Done when you can list what the framework saved you and what it hid.

## Checklist

- [ ] [Must ship] Build a plain Python RAG script that loads, chunks, embeds, retrieves and answers over a real document set.
- [ ] [Must ship] Store source, title and page or URL with every chunk and show them as citations.
- [ ] [Must ship] Make the pipeline refuse questions the documents cannot answer, and keep five such questions as tests.
- [ ] [Recommended] Compare at least two chunking settings on a labelled question set.
- [ ] [Recommended] Parse at least one complex PDF into Markdown and check its tables by eye.
- [ ] [Stretch] Rebuild the pipeline in a framework and write down the trade-offs.

## You're ready when

- You can sketch the RAG pipeline from loading to answer and name one way each stage fails.
- Your pipeline returns answers with citations that point to real chunks, and refuses when the context lacks the answer.
- You can justify your chunk size with numbers from a small test.
- You can explain whether long context, RAG or fine-tuning fits a given problem, and why.
