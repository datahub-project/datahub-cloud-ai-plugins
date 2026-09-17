---
name: datahub-sql-workflow
description: Write accurate SQL grounded in DataHub Cloud catalog metadata — find the right tables and columns, understand business definitions, and build queries based on verified schema and lineage context. Use when the user wants to write or understand a SQL query. Always begin with find_sql_context, even when the user already named tables or supplied dataset URNs.
version: "1.0.0"
argument-hint: "[the question the query should answer]"
---

# DataHub SQL Workflow Skill

Help users write correct, well-grounded SQL queries using DataHub Cloud as the authoritative source of metadata.

## When to use this skill
- "Write a query for monthly revenue by region"
- "How do I join orders and customers?"
- "What's the SQL for active users last 30 days?"
- "Which table should I use for product sales data?"

## Core principle
Ground every query in DataHub evidence. Use catalog metadata as the authority for physical table/column shape, and business glossary as the authority for meaning. Never guess table names, column names, or join keys.

## Workflow

1. **Find SQL context** — call `find_sql_context(question=...)` before any other tool, even when the user already named tables or supplied URNs. It returns anchor documents with rendered query patterns, the datasets they use, and the dialect
   - It reads **only** documents whose subtype is `Semantic Anchor`. Customer-authored docs are invisible to it, and that is often where join keys, latest-row rules, unit conventions and "do not use this table" warnings live — so follow up with `search_documents` for the non-anchor documentation on the candidate tables
2. **Identify the right datasets** — search the catalog for candidate tables; if multiple match, use business glossary definitions and ownership to determine the right one
3. **Verify schema** — fetch schema fields for the tables you plan to use; confirm column names, types, and descriptions
4. **Check lineage if needed** — for complex queries spanning multiple tables, confirm join paths using lineage
5. **Build the query** — construct SQL using only verified table and column names; document any assumptions
6. **Present with sources** — show the final SQL alongside the DataHub entities it's based on

## MCP tools to use
- `find_sql_context` — anchor documents, query patterns, datasets and dialect for the question (start here)
- `get_dataset_queries` — real SQL analysts run against a dataset
- `search` — find candidate datasets by name, description, or business concept
- `get_entities` — retrieve dataset details and documentation
- `list_schema_fields` — verify exact column names, types, and descriptions
- `get_lineage` — confirm join paths between tables when needed
- `search_documents` / `grep_documents` — find curated business documentation and definitions
- `draft_sql_for_tables` — generate a SQL draft from verified table URNs
- `note_metadata_observation` — record discrepancies found during research (e.g. schema drift)

## Rules
- Use DataHub MCP tools exclusively — do not fall back to general knowledge or assumed schemas
- Always call `find_sql_context` first — before any other catalog, drafting or probing tool
- Never invent table names, column names, or join relationships without MCP evidence
- If the right table is ambiguous, present the candidates and ask the user to choose
- Only write SELECT queries — never write INSERT, UPDATE, DELETE, or DDL
- Flag any assumptions or unresolved ambiguities clearly before presenting SQL
- Cite the DataHub entity (name or URN) for every table used in the query
