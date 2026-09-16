---
name: datahub-search
description: Search and explore the DataHub Cloud data catalog — find datasets, dashboards, pipelines, columns, owners, tags, domains, and any metadata. Use when the user wants to find, discover, or look up anything in their data catalog.
version: "1.0.0"
---

# DataHub Search Skill

Help users find and explore their data catalog using DataHub MCP tools.

## When to use this skill
- "Find datasets about orders"
- "Who owns the revenue table?"
- "What's in the Finance domain?"
- "Show me Snowflake tables tagged PII"
- "What columns does the customer table have?"

## When NOT to use this skill
- Lineage questions ("what feeds into X?") → use `datahub-cloud:datahub-lineage`
- Data quality questions ("is this table healthy?") → use `datahub-cloud:datahub-quality`
- SQL help → use `datahub-cloud:datahub-sql-workflow`

## Workflow

1. **Understand the request** — identify what the user is looking for: an entity name, an owner, a tag, a domain, a platform, or a concept
2. **Search** — use MCP search tools with the most relevant filters
3. **Fetch details** — for top results, retrieve schema, ownership, tags, glossary terms, and descriptions
4. **Present clearly** — summarize results in plain language; include entity names, platforms, and links when available

## MCP tools to use
- `search` — find entities by keyword, type, platform, owner, tag, domain
- `get_entities` — fetch full details (schema, ownership, tags, glossary terms, descriptions) for a known URN
- `list_schema_fields` — list columns for a dataset
- `search_documents` — search curated documentation and business context
- `grep_documents` — search document content for specific terms

## Rules
- Use DataHub MCP tools exclusively — do not use the DataHub CLI
- Always include the entity URN in responses so users can navigate directly
- When the query is ambiguous, ask one clarifying question before searching
- Never fabricate entity names, owners, or URNs — only report what the MCP tools return
- If no results are found, say so clearly and suggest broadening the search
- Limit results to the most relevant 5–10; offer to show more if asked
