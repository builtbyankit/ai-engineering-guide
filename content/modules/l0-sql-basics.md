---
title: Just enough SQL
level: L0
kind: core
hours: 5–6
summary: Create tables, query and join them, write data safely with placeholders and transactions, and add the indexes and full-text search that agent memory and retrieval rely on.
checked: 2026-10-17
---

## Why it matters

Agents keep a lot of state, and most of it ends up in a database. Long-term memory, run checkpoints, audit logs, idempotency keys and the chunks behind retrieval all live in tables. Later levels use SQLite and Postgres for each of these, so you need to read and write SQL without looking up every keyword.

SQL is also a security boundary. When a tool turns a model's arguments into a query, a value pasted into the SQL string can change what the query does. This module covers the small part of SQL you will use every week, from the first `SELECT` to indexes and full-text search. It uses SQLite, which ships with Python and needs no server. [Embeddings and vector search](#l2-embeddings-vector-search) and [Memory and context engineering](#l3-memory-context) build on it.

## What to learn

- **Tables, rows and types**: A table holds rows that share the same columns, and each column has a type such as `INTEGER`, `TEXT` or `REAL`. A primary key gives every row a unique id that other tables can point to.
- **Querying**: `SELECT` picks columns, `WHERE` filters rows, `ORDER BY` sorts and `LIMIT` caps how many come back. Most questions you ask a database combine these four.
- **Changing data**: `INSERT` adds rows, `UPDATE` changes them and `DELETE` removes them. Before you run an `UPDATE` or `DELETE`, run a `SELECT` with the same `WHERE` to see which rows it will touch.
- **Joins**: A join combines rows from two tables that share a key, such as recipes and their ingredients. An inner join keeps only rows that match, and a left join keeps every row from the first table.
- **Aggregates**: `COUNT`, `SUM` and `AVG` summarise rows, and `GROUP BY` gives one summary per group, such as the number of tickets per category.
- **Constraints and upserts**: `UNIQUE` and `NOT NULL` let the database reject bad data. `INSERT ... ON CONFLICT DO NOTHING` turns a repeated write into a harmless no-op, which is how idempotency keys work in [Tool calling in depth](#l3-tool-calling).
- **Transactions**: A transaction groups several changes so that either all of them are saved or none are. In Python's `sqlite3`, your changes are not saved until you commit.
- **Placeholders**: Pass values with `?` or `:name` placeholders, never by formatting them into the SQL string. Placeholders keep data as data, so input such as `' OR 1=1 --` cannot change the query.
- **Indexes**: An index lets the database find matching rows without reading the whole table. `EXPLAIN QUERY PLAN` shows whether a query scans every row or searches an index.
- **Full-text search**: SQLite's FTS5 and Postgres's built-in text search index the words in a column and rank matches by relevance. Level 2 combines this keyword search with vector search.

## Resources

### Start here

- [Introduction to SQL](https://sqlbolt.com/) · SQLBolt · Tutorial · Free · 2–3 h — Nineteen short interactive lessons from `SELECT` through joins, aggregates, `INSERT`, `UPDATE` and `CREATE TABLE`, each ending in an exercise you solve in the browser.
- [sqlite3: DB-API 2.0 interface for SQLite databases](https://docs.python.org/3/library/sqlite3.html) · Python Software Foundation · Docs · Free · 45 min — Read the tutorial and the how-to on placeholders to connect, create a table, commit and bind values safely from Python.

### Go deeper

- [CS50's Introduction to Databases with SQL](https://cs50.harvard.edu/sql) · Harvard University · Course · Free · self-paced — Seven weeks of lectures and problem sets on querying, schema design, indexes, transactions and scaling, starting in SQLite and ending with PostgreSQL and MySQL.
- [Select Star SQL](https://selectstarsql.com/) · Zi Chong Kao · Book · Free · 2 h — A free interactive book that teaches filtering, aggregation, grouping and joins on one real dataset, in four chapters of about 30 minutes each.
- [Use The Index, Luke](https://use-the-index-luke.com/) · Markus Winand · Book · Free · self-paced — The free web edition of an indexing book; the chapters on index anatomy and the WHERE clause explain why one index can make a slow query fast.
- [Tutorial](https://www.postgresql.org/docs/current/tutorial.html) · PostgreSQL · Docs · Free · 2 h — The official tutorial on tables, joins, aggregates, foreign keys and transactions, a good bridge to pgvector and Postgres full-text search in Level 2.
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) · OWASP · Docs · Free · 20 min — Ranks the defences against SQL injection with parameterised queries first, the rule every database tool you give an agent must follow.

### Reference

- [SQLite FTS5 Extension](https://sqlite.org/fts5.html) · SQLite · Docs · Free · reference — Creating full-text tables, the `MATCH` query syntax and the `bm25()` ranking function behind keyword search over notes and memories.
- [UPSERT](https://sqlite.org/lang_upsert.html) · SQLite · Docs · Free · reference — `INSERT ... ON CONFLICT DO NOTHING` and `DO UPDATE` with examples, the building block for idempotent writes.
- [EXPLAIN QUERY PLAN](https://sqlite.org/eqp.html) · SQLite · Docs · Free · reference — How to read `SCAN` versus `SEARCH ... USING INDEX` in a query plan, so you can confirm that an index is used.

## Practice

1. **Work through SQLBolt.** Complete lessons 1 to 16, from `SELECT` to `CREATE TABLE`. Done when you can write a query that joins two tables, filters rows and groups the result without looking at the lesson.
2. **Recipes in SQLite.** With Python's `sqlite3`, create `recipes` and `ingredients` tables linked by a recipe id, with a `UNIQUE` recipe title. Load the recipes from [Python for AI engineering](#l0-python-for-ai) with placeholders inside one transaction. Write three queries: recipes with at least four servings, recipes that use a chosen ingredient (a join) and the number of ingredients per recipe (a group). Done when all three print correct results and running the load script twice adds no duplicate rows.
3. **Prove placeholders matter.** Write `find_recipe(title)` twice, once with an f-string and once with a placeholder, and call both with `' OR 1=1 --`. Done when the f-string version returns every recipe and the placeholder version returns none.
4. **Make a write idempotent.** Add an `orders` table with a `UNIQUE` idempotency key and insert the same order twice with `ON CONFLICT DO NOTHING`. Done when the table holds one row and your code reports that the second insert was a repeat.
5. **Index and search.** Generate 100,000 rows, time a filtered query and read its `EXPLAIN QUERY PLAN`, then add an index and repeat. Then build an FTS5 table over a few dozen notes and rank matches with `bm25()`. Done when you can show the plan change from `SCAN` to `SEARCH` and a ranked keyword search.

## Checklist

- [ ] [Must ship] Complete the SQLBolt lessons up to `CREATE TABLE`.
- [ ] [Must ship] Create two related tables in SQLite from Python and query them with a join and a `GROUP BY`.
- [ ] [Must ship] Use placeholders for every query in your scripts, and show an injection succeeding against an f-string version.
- [ ] [Recommended] Make a repeated insert harmless with a `UNIQUE` key and `ON CONFLICT DO NOTHING`.
- [ ] [Recommended] Add an index and show the query plan change with `EXPLAIN QUERY PLAN`.
- [ ] [Stretch] Build an FTS5 table over a folder of notes and rank keyword matches with `bm25()`.

## You're ready when

- You can write a query that joins two tables, filters rows and groups the result without looking anything up.
- You can explain why placeholders stop SQL injection and why string formatting does not.
- You can say what a transaction guarantees and where your script commits.
- You can explain how a `UNIQUE` constraint makes a repeated write harmless, and how to check whether a query uses an index.
