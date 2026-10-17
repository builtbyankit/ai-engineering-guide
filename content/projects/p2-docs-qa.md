---
title: Docs Q&A with citations
level: L2
weeks: 1.5–2
summary: Build question answering over public docs or PDFs with hybrid search, reranking, cited answers that refuse when unsupported, and a retrieval and answer evaluation report.
---

## The brief

You will build a question-answering assistant for a set of documents. Pick a public documentation site, such as an open-source library's user guide, or a folder of PDFs, such as product manuals or research papers. A user asks a question in plain language and gets a short answer with numbered citations that lead to the exact page or section. When the documents do not support an answer, the assistant says so and does not guess.

The users are people who would otherwise search the docs by hand, such as a new user of a library or someone hunting through manuals. Alongside the app you write a short evaluation report showing how well retrieval and answers work, what fails and what you changed. That report turns a demo into evidence you can show an employer.

## What you'll practise

- [Embeddings and vector search](#l2-embeddings-vector-search): picking an embedding model with a quick test and storing chunks with metadata.
- [Building a RAG pipeline](#l2-rag-pipeline): parsing, chunking, prompt assembly, citations and refusals.
- [Better retrieval: hybrid search and reranking](#l2-advanced-retrieval): BM25 plus vectors, reciprocal rank fusion and a reranker.
- [Evaluating RAG](#l2-rag-evaluation): a labelled question set, retrieval and answer metrics, and error analysis.
- [Structured outputs and function calling basics](#l1-structured-outputs): returning answers and citations as validated JSON.

## Requirements

- [ ] [Must ship] Ingest at least 50 pages of public documentation or PDFs, keeping source, title, section and page or URL for every chunk.
- [ ] [Must ship] Retrieve with hybrid search (BM25 or full-text search plus vectors) merged with reciprocal rank fusion.
- [ ] [Must ship] Rerank the merged candidates with a cross-encoder or hosted reranker before building the prompt.
- [ ] [Must ship] Return answers as structured output whose citations map to real chunk ids, and show them as links or page references.
- [ ] [Must ship] Refuse clearly when the retrieved context does not support an answer.
- [ ] [Must ship] Provide a CLI, web page or API endpoint where someone can ask a question and see the answer with its sources.
- [ ] [Must ship] Include an eval set of at least 40 questions, 8 or more of them unanswerable, and a script that reports recall@5, MRR, faithfulness, answer relevance and refusal accuracy.
- [ ] [Must ship] Write an evaluation report with a baseline, at least one improvement, before and after numbers, and an error analysis.

## Stretch goals

- [ ] [Recommended] Add contextual chunk notes or parent/child retrieval and measure the change.
- [ ] [Recommended] Check each citation after generation by confirming the cited chunk contains the supporting text, and drop or retry claims that fail.
- [ ] [Stretch] Add query decomposition for multi-part questions and test it on a multi-hop subset of your eval set.
- [ ] [Stretch] Support incremental re-indexing so changed files are re-embedded without rebuilding everything.
- [ ] [Stretch] Run the eval in GitHub Actions on every push and fail the build if recall@5 drops.

## Suggested stack

| Need | Suggested | Alternatives |
| --- | --- | --- |
| Parsing | Docling or PyMuPDF4LLM for PDFs; Markdown files as they are | Unstructured; BeautifulSoup for HTML |
| Embeddings | An open model run with Sentence Transformers, shortlisted from MTEB | OpenAI or Gemini embedding APIs |
| Storage and keyword search | Postgres with pgvector and built-in full-text search | Qdrant with dense and sparse vectors; Chroma plus bm25s |
| Reranking | An open cross-encoder run with Sentence Transformers | Cohere Rerank or another hosted reranker |
| Generation | Any API model from Level 1, using structured output | A local model through Ollama |
| Evaluation | A plain Python or pytest script plus Ragas | DeepEval; ranx for ranking metrics |
| Interface | A CLI or a FastAPI endpoint | Streamlit or Gradio for a quick web page |

## Build it step by step

1. **Pick and fetch the corpus**: Choose 50 to 300 pages whose licence lets you use them in a public demo. Save the raw files with their source URLs so citations can link back.
2. **Parse and chunk**: Convert everything to Markdown, split by headings into chunks of a few hundred tokens, and store each chunk with an id and its metadata. Spot-check ten chunks, including one that contains a table.
3. **Write the eval set early**: Before tuning anything, write and label 40 or more questions, including unanswerable ones. This set is how you will judge every later change.
4. **Baseline retrieval and answers**: Embed the chunks, run vector search and generate answers with chunk ids in the prompt. Record recall@5 and MRR so you have numbers to beat.
5. **Add hybrid search and reranking**: Add BM25 or full-text search, merge with RRF, then rerank the top 30 to 50 candidates. Rerun the eval after each change and keep the results table.
6. **Citations and refusals**: Ask for structured output with the answer, the cited chunk ids and an `answerable` flag. Check that every cited id exists, then show citations as links or page numbers.
7. **Score answers and analyse errors**: Run faithfulness and answer relevance, hand-check a sample of judge scores and tag every failure by cause. Fix the largest group and measure again.
8. **Package it**: Add the interface, a README and the evaluation report, and make the whole thing run from one setup command.

## How to evaluate it

The thresholds below are example targets. Adjust them to your corpus and explain any change in your report.

| Criterion | Good enough | Excellent |
| --- | --- | --- |
| Retrieval | Recall@5 of at least 0.75 on answerable questions | Recall@5 of at least 0.9, with MRR reported and improved over the baseline |
| Citations | Every cited id exists and points to the right document | Each cited passage is checked automatically to contain the supporting text |
| Refusals | Refuses at least 7 of 8 unanswerable questions | Refuses all of them while still answering at least 90% of answerable ones |
| Faithfulness | Average score of at least 0.8, with 10 judge scores hand-checked | 0.9 or higher, with judge agreement against your own labels reported |
| Latency | Answers in under 10 s on a laptop | Median under 3 s, with timings reported per stage |
| Report | Baseline, one improvement and before and after numbers | Several measured changes, failure counts by type and a clear next step |

## Show your work

- A README with the corpus and its licence, a short architecture description, setup steps, example questions and known limits.
- A 2-minute demo video or GIF showing a cited answer, a click through to the source and a refusal.
- The evaluation report as a Markdown file or blog post, with the before and after table and three example failures.
- A CV line with real numbers, for example "Built hybrid RAG over 300 pages of docs; raised recall@5 from 0.68 to 0.91 with BM25 fusion and reranking."

## Ideas to make it yours

- Your city council's meeting minutes, answering "what was decided about X, and when?"
- The documentation of a programming library you use, keeping code samples intact inside chunks.
- A folder of research papers in one field, with citations down to page numbers.
- Public repair manuals for bikes or home appliances, where refusing matters because wrong advice is costly.
- A government guidance site with yearly versions, using date filters so answers match the right year.

## Helpful resources

- [Enhancing RAG with Contextual Retrieval](https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/contextual-embeddings/guide.ipynb) · Anthropic · Tutorial · Free · 2 h — A full notebook that adds contextual embeddings, BM25 hybrid search and reranking to a baseline and measures each step.
- [pgvector-python](https://github.com/pgvector/pgvector-python) · pgvector · Repo · Free · reference — Has short examples of hybrid search with reciprocal rank fusion and with a cross-encoder, plus a small RAG example.
- [kotaemon](https://github.com/Cinnamon/kotaemon) · Cinnamon · Repo · Free · reference — An open-source document chat app with hybrid retrieval, reranking and in-browser PDF citations, worth studying for design ideas.
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations) · Anthropic · Docs · Free · 20 min — If you use Claude, the API can cite passages from your own chunks so you do not have to parse citation markers yourself.
- [Testset Generation for RAG](https://docs.ragas.io/en/stable/getstarted/rag_testset_generation/) · Ragas · Docs · Free · 30 min — Generates draft single-hop and multi-hop questions from your documents to seed the eval set before you review them.
- [Advanced Labs: Build Evidence for Mastery](https://github.com/builtbyankit/agentic-ai-learning-guide/blob/main/agentic-ai-advanced-labs.md) · Agentic AI Mastery · Tutorial · Free · self-paced — Eight labs, including separate answer and retrieval evaluation, calibrated abstention and index lifecycle with security metadata, each with a report template.
