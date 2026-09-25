# DataHub Cloud AI plugin

A portable [Agent Plugins](https://developers.openai.com/plugins/build/plugins) package for exploring a DataHub Cloud catalog through the [DataHub MCP server](https://mcp.datahub.com/mcp). It includes skills for catalog search, lineage, data quality, connection troubleshooting, and SQL grounded in catalog metadata.

## Package layout

| Path | Purpose |
| --- | --- |
| `plugin.json` | Portable plugin identity and OpenAI presentation metadata |
| `mcp.json` | Portable Streamable HTTP connection to DataHub Cloud |
| `skills/` | Workflows shared across supported hosts |
| `.codex-plugin/plugin.json`, `.mcp.json` | Codex compatibility files for older plugin hosts |
| `.claude-plugin/plugin.json`, `commands/` | Claude Code compatibility files |

The MCP server uses OAuth for access to each user's DataHub Cloud catalog. Do not put credentials in this package.

## Use the plugin

Ask in natural language, for example:

- "Who owns the customer_dim dataset?"
- "What depends on the orders table?"
- "Which checks are failing for revenue_metrics?"
- "Draft a SELECT query for monthly revenue by product line using verified schema."
- "Test my DataHub Cloud connection."

The five workflows live in `skills/datahub-search`, `skills/datahub-lineage`, `skills/datahub-quality`, `skills/datahub-sql-workflow`, and `skills/datahub-setup`. Claude Code also provides `/catalog-search`, `/catalog-lineage`, `/catalog-quality`, `/catalog-sql`, and `/catalog-setup` commands.

## Submit to OpenAI

Use a **With MCP** submission in the [OpenAI plugin portal](https://platform.openai.com/plugins). Submit `https://mcp.datahub.com/mcp` as a **Universal** remote MCP URL, and upload the final `skills/` bundle in the same draft. The portable `plugin.json` and `mcp.json` are the source package for compatible hosts; the portal separately scans the remote MCP server and its tools. See [submission/README.md](submission/README.md) for the listing copy, test cases, and remaining publisher tasks.

Run `python3 submission/package.py` to build both ZIPs in `dist/`: a portable package for compatible hosts and a skills bundle for the portal's Skills tab. Rebuild after editing a skill or manifest.

OpenAI's [submission guide](https://developers.openai.com/plugins/deploy/submission) requires domain verification, an approved publisher identity, reviewer access to authenticated tools, and a completed listing before review. These steps require access to the DataHub service and the publishing organization.

## Other installation options

To add this checkout as a local Codex marketplace, run `codex plugin marketplace add /absolute/path/to/datahub-cloud-ai-plugins`, then `codex plugin add datahub-cloud@datahub-cloud-ai-plugins`. The marketplace catalog is `.agents/plugins/marketplace.json`; its plugin source points to this repository root.

For Claude Code skills, run `npx skills add datahub-project/datahub-cloud-ai-plugins` or find **datahub-cloud** in the Claude marketplace. Other hosts that support Agent Plugins can load this repository's portable package.

## Links

- [DataHub documentation](https://docs.datahub.com/)
- [DataHub developer skills](https://github.com/datahub-project/datahub-skills)

Licensed under Apache-2.0.
