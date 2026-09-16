---
name: datahub-search
description: Search and explore the DataHub Cloud data catalog — find datasets, dashboards, pipelines, columns, and any metadata entity by name, owner, tag, domain, or description. Use this when the user wants to find or discover anything in their data catalog.
version: "1.0.0"
---

# DataHub Search Skill

Use the `datahub` MCP tools to search and explore the DataHub Cloud catalog.

## Capabilities
- Search for any entity: datasets, dashboards, charts, data jobs, data flows, ML models, glossary terms, and more
- Filter by owner, tag, domain, platform, environment
- Look up schema details and column-level metadata
- Retrieve entity URNs for use in other operations

## Workflow

1. **Clarify the query** — understand what the user is looking for (entity type, keywords, filters)
2. **Search** — use `search` or `search_across_entities` MCP tool with appropriate filters
3. **Retrieve details** — for the most relevant results, fetch entity aspects (schema, ownership, tags, glossary terms, etc.)
4. **Present results** — summarize clearly with names, URNs, platforms, and descriptions

## Rules
- Always include the entity URN in your response so users can navigate directly
- Use GraphQL projection to fetch only the aspects you need — avoid fetching everything
- For ambiguous queries, ask the user to clarify before searching
- Check the `siblings` aspect when retrieving dataset details — it links related entities across environments
- Popularity sorting is available in DataHub Cloud; use it when ranking matters
- Never fabricate entity names or URNs — only report what MCP tools return

## Examples
- "Find all Snowflake tables owned by the Data Engineering team"
- "Search for dashboards tagged with PII"
- "Show me schemas for the orders dataset"
- "What datasets are in the Finance domain?"
