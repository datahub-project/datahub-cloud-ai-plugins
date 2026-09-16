# DataHub Cloud — Claude Plugin

A Claude plugin that connects Claude to your [DataHub Cloud](https://datahubproject.io) instance via the DataHub MCP server — enabling catalog search, lineage exploration, data quality monitoring, and SQL grounded in real metadata.

## Installation

```bash
npx skills add datahub-project/datahub-cloud-ai-plugins
```

Or search for **datahub-cloud** in the Claude marketplace.

## Authentication

This plugin connects to DataHub Cloud via the MCP server at `https://mcp.datahub.com/mcp`. Authentication is handled automatically via OAuth — no tokens or environment variables needed.

## Skills and Commands

| Skill | Command | Description |
|---|---|---|
| `datahub-search` | `/catalog-search` | Find datasets, dashboards, owners, tags, domains |
| `datahub-lineage` | `/catalog-lineage` | Trace upstream/downstream data flow and dependencies |
| `datahub-quality` | `/catalog-quality` | Check assertions, freshness, volume, and data health |
| `datahub-sql-workflow` | `/catalog-sql` | Write SQL grounded in verified catalog metadata |
| `datahub-setup` | `/catalog-setup` | Verify and troubleshoot the DataHub Cloud connection |

## Usage Examples

```
/catalog-search Find all Snowflake tables tagged PII in the Finance domain
/catalog-lineage What does the orders table feed into downstream?
/catalog-quality Show failing data quality checks for the revenue dataset
/catalog-sql Write a query for monthly active users by region
/catalog-setup Test my DataHub Cloud connection
```

Skills are also invoked automatically from natural language:

> "Who owns the customer_dim table?"
> "What would break if we deleted the orders dataset?"
> "Is the revenue_metrics table up to date?"
> "Help me query monthly revenue by product line"

## MCP Tools

This plugin uses the following DataHub MCP tools:

| Tool | Used by |
|---|---|
| `search` | search, lineage, quality, sql-workflow |
| `get_entities` | search, lineage, quality |
| `get_lineage` | lineage |
| `get_lineage_paths_between` | lineage |
| `list_schema_fields` | search, sql-workflow |
| `get_dataset_queries` | sql-workflow |
| `draft_sql_for_tables` | sql-workflow |
| `search_documents` / `grep_documents` | search, sql-workflow |
| `get_me` | setup |
| `note_metadata_observation` | sql-workflow |
| `list_lifecycle_stages` | quality |

## Related

- [datahub-skills](https://github.com/datahub-project/datahub-skills) — Developer skills for building DataHub connectors, reviewing connector PRs, and writing ingestion code
- [DataHub Documentation](https://datahubproject.io/docs)

## License

Apache 2.0
