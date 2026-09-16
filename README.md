# DataHub Cloud — Claude Plugin

A Claude Code plugin that connects Claude to your [DataHub Cloud](https://datahubproject.io) instance via the DataHub MCP server.

Search your data catalog, enrich metadata, trace lineage, and manage data quality — all from within Claude Code.

## Installation

```bash
npx skills add datahub-project/datahub-cloud-claude-plugin
```

Or via the Claude marketplace: search for **datahub-cloud**.

## Authentication

This plugin connects to the DataHub Cloud MCP server at `https://mcp.datahub.com/mcp`.

You'll need a **Personal Access Token (PAT)** from your DataHub Cloud instance:

1. Go to **DataHub Cloud → Settings → Access Tokens**
2. Create a new token with read/write permissions as needed
3. Set it as an environment variable:

```bash
export DATAHUB_TOKEN=your-token-here
```

## Skills

| Skill | Command | Description |
|---|---|---|
| `datahub-search` | `/catalog-search` | Search the catalog for any entity |
| `datahub-enrich` | `/catalog-enrich` | Add tags, owners, descriptions, and more |
| `datahub-lineage` | `/catalog-lineage` | Trace upstream/downstream lineage |
| `datahub-quality` | `/catalog-quality` | Check assertions and data health |
| `datahub-setup` | `/catalog-setup` | Configure and verify your connection |

## Usage Examples

```
/catalog-search Find all Snowflake tables tagged with PII
/catalog-enrich Add the Finance domain to the revenue_metrics dataset
/catalog-lineage What datasets does the orders table feed into?
/catalog-quality Show failing assertions in the Finance domain
/catalog-setup Test my DataHub Cloud connection
```

Skills are also automatically invoked when you ask Claude about your data catalog:

> "What's the lineage for the customer_dim table?"
> "Tag the orders dataset as Sensitive"
> "Find all datasets owned by the Data Engineering team"

## MCP Server

This plugin configures the DataHub Cloud MCP server automatically via `.mcp.json`:

```json
{
  "datahub": {
    "type": "http",
    "url": "https://mcp.datahub.com/mcp"
  }
}
```

## Related

- [datahub-skills](https://github.com/datahub-project/datahub-skills) — Developer-focused skills for building DataHub connectors, writing ingestion code, and reviewing connector PRs
- [DataHub Documentation](https://datahubproject.io/docs)
- [DataHub Cloud](https://www.acryldata.io)

## License

Apache 2.0
