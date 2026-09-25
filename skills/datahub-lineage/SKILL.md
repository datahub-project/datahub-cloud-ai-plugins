---
name: datahub-lineage
description: Explore data lineage in DataHub Cloud — trace where data comes from (upstream) and where it flows (downstream), understand pipeline dependencies, and assess the impact of changes. Use when the user asks about data origins, dependencies, or flow.
---

# DataHub Lineage Skill

Help users understand data flow and dependencies using DataHub MCP tools.

## When to use this skill
- "Where does the orders table come from?"
- "What depends on the customer_dim dataset?"
- "What would break if we changed this table?"
- "Show me the pipeline for revenue metrics"
- "Trace lineage from Kafka to the dashboard"

## When NOT to use this skill
- General catalog search → use `datahub-cloud:datahub-search`
- Data quality questions → use `datahub-cloud:datahub-quality`

## Workflow

1. **Identify the starting entity** — use the entity name or URN provided; if unclear, search for it first
2. **Determine direction**:
   - *"Where does it come from?"* → upstream traversal
   - *"What depends on it?"* → downstream traversal
   - *"Show me the full pipeline"* → both directions
3. **Fetch lineage** — use MCP lineage tools, defaulting to 3 hops; ask the user if they want to go deeper
4. **Summarize clearly** — describe the lineage path in plain language; note any critical dependencies or single points of failure

## Presenting results
- Lead with the most important path (e.g. direct upstream sources or top-level downstream consumers)
- For large graphs, summarize the shape ("5 upstream sources, 12 downstream consumers") before listing details
- Highlight entities that many others depend on
- Note when column-level lineage is available for a given platform

## MCP tools to use
- `search` — find the starting entity if no URN is provided
- `get_lineage` — traverse upstream or downstream lineage from an entity
- `get_lineage_paths_between` — find all paths between two specific entities
- `get_entities` — fetch additional details (owner, description) for entities in the lineage graph

## Rules
- Use DataHub MCP tools exclusively — do not use the DataHub CLI
- Never infer or guess lineage relationships — only report what MCP tools return
- If lineage is unavailable for an entity, explain that lineage may not have been ingested for that platform
