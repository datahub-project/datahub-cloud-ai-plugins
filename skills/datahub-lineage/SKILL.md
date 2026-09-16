---
name: datahub-lineage
description: Explore and visualize data lineage in DataHub Cloud — trace upstream and downstream dependencies for datasets, pipelines, and dashboards. Use this when the user wants to understand where data comes from or where it flows.
version: "1.0.0"
---

# DataHub Lineage Skill

Use the `datahub` MCP tools to explore lineage relationships across the catalog.

## Capabilities
- Trace upstream lineage (where does this data come from?)
- Trace downstream lineage (what depends on this data?)
- Identify column-level lineage when available
- Find impact of changes — what breaks if this dataset changes?
- Summarize the lineage graph in plain language

## Workflow

1. **Identify the starting entity** — find the entity URN using search if not provided
2. **Determine direction** — upstream, downstream, or both
3. **Set depth** — ask the user if they want a full graph or just immediate dependencies
4. **Fetch lineage** — use the lineage MCP tools with appropriate hop depth
5. **Summarize** — present the lineage clearly, highlighting critical paths and important dependencies

## Rules
- Limit lineage hops to 3 by default; ask the user if they want to go deeper
- When presenting large graphs, summarize the most important paths first
- Highlight entities that appear as single points of failure (many dependents, no alternatives)
- If column-level lineage is requested, note when it's not available for a given platform
- Never infer lineage — only report what MCP tools return

## Examples
- "What are the upstream sources for the revenue_metrics dataset?"
- "Show me everything that depends on the orders Snowflake table"
- "Trace lineage from the Kafka topic to the dashboard"
- "What would break if I deleted the customer_dim table?"
