<img src="assets/logo-square.svg" alt="DataHub" width="56" align="left" hspace="12" vspace="4">

# DataHub Cloud — AI Plugins

Connects Claude, Codex and other agents to your [DataHub Cloud](https://datahub.com)
instance via the DataHub MCP server — catalog search, lineage exploration, data
quality, and SQL grounded in real metadata.

One plugin, three manifests: the same tree installs into Claude Code, Codex, and
any client implementing [Agent Plugins 1.0.0](https://agent-plugins.org/specification),
and one `skills/` directory serves all three.

## Installation

```bash
npx skills add datahub-project/datahub-cloud-ai-plugins
```

Or search for **datahub-cloud** in the Claude marketplace.

Codex discovers this repo's `.codex-plugin/plugin.json` when you install from a
clone; other clients read the root `plugin.json` and `mcp.json`.

## Authentication

The plugin connects to `https://mcp.datahub.com/mcp` over **OAuth 2.0 with dynamic
client registration** — no tokens, tenant URLs or environment variables, and no
credentials in the repo.

Sign in once, from a session:

```
/mcp
```

or from the shell:

```bash
claude mcp login datahub
```

The endpoint answers an unauthenticated request with `401` and a
`www-authenticate: Bearer resource_metadata="…"` pointer to its protected-resource
metadata (RFC 9728), advertising `openid` and `datahub:account` scopes plus a
`registration_endpoint`, so a conformant client registers itself with no
pre-shared client ID. A `401` before you sign in is expected, not a fault.

**A DataHub Cloud account is required.** Tool availability and read/write
permissions follow the account you sign in as, governed by DataHub — this plugin
sets no client-side capability flag.

## Skills

| Skill | Description |
|---|---|
| `datahub-search` | Find datasets, dashboards, owners, tags and domains |
| `datahub-lineage` | Trace upstream/downstream flow and assess blast radius |
| `datahub-quality` | Check assertions, freshness, volume and health |
| `datahub-sql-workflow` | Write SQL grounded in verified catalog metadata |
| `datahub-setup` | Verify and troubleshoot the connection |

These are the public base template skills — deliberately basic, and equivalent to
what is already published in
[datahub-project/datahub-skills](https://github.com/datahub-project/datahub-skills).

Skills are both model-invoked and user-invocable, so natural language reaches
them and so does an explicit call:

```
/datahub-cloud:datahub-search Find all Snowflake tables tagged PII in the Finance domain
/datahub-cloud:datahub-lineage What does the orders table feed into downstream?
/datahub-cloud:datahub-quality Show failing data quality checks for the revenue dataset
/datahub-cloud:datahub-sql-workflow Write a query for monthly active users by region
/datahub-cloud:datahub-setup Test my DataHub Cloud connection
```

The `datahub-cloud:` prefix is optional where the name does not collide, so
`/datahub-search` usually works too.

There is no `commands/` directory. Every skill is user-invocable by default, so a
command would have been a one-line wrapper over a skill you can already call — and
commands are not a component type in Agent Plugins 1.0.0, so dropping them means
all three clients see one identical surface.

Natural language reaches the same skills directly:

> "Who owns the customer_dim table?"
> "What would break if we deleted the orders dataset?"
> "Is the revenue_metrics table up to date?"

## MCP tools

| Tool | Used for |
|---|---|
| `search`, `get_entities`, `list_schema_fields` | Discovery and entity reads |
| `get_lineage`, `get_lineage_paths_between` | Table- and column-level lineage |
| `find_sql_context`, `get_dataset_queries`, `draft_sql_for_tables` | Grounded SQL |
| `search_documents`, `grep_documents` | Curated catalog documents |
| `get_me` | Authenticated identity, for connection checks |
| `list_lifecycle_stages` | Lifecycle and governance context |

Metadata writes — tags, glossary terms, owners, domains, descriptions — are
available when your account has permission. The exact set depends on your DataHub
version; run `/mcp` to see what resolved.

One filter gotcha, documented in the search skill: `tag`, `domain`,
`glossary_term`, `owner` and `container` filters take **full URNs**
(`urn:li:tag:PII`), not display names. A display name returns zero results
silently rather than erroring, so resolve the name to a URN first.
`entity_type`, `platform` and `env` take plain values.

## Evals

`evals/` holds four suites — catalog search, upstream lineage, quality check, and
grounded SQL — one per skill. Each has a prompt, mocked MCP responses, and three
graders: that the skill fired, that the right MCP tool was called, and an LLM
judgement on response quality. Results are gitignored.

## Manifest metadata

Five manifests across three schemas, plus two MCP configs, repeat the same
identity — so none is edited by hand. [`plugin-metadata.json`](plugin-metadata.json)
is the source of truth and [`scripts/apply-metadata.py`](scripts/apply-metadata.py)
generates them all:

| File | Read by |
|---|---|
| `.claude-plugin/plugin.json` + `.mcp.json` | Claude Code |
| `.codex-plugin/plugin.json` + `.mcp.json` | Codex (this one declares `skills`) |
| `plugin.json` + `mcp.json` | Agent Plugins 1.0.0 clients |

`--check` fails if any has drifted; `--check-urls` re-verifies every URL resolves,
which is worth running before a directory submission.

Where each field can live differs by schema. Only Codex reads the icon and legal
URLs as first-class fields; Claude Code's `metadata` block is free-form and it
doesn't read it, and the Agent Plugins root manifest is a closed schema with
nowhere to put them.

Before opening a PR:

```bash
./scripts/apply-metadata.py --check && claude plugin validate . --strict
```

## Related

- [datahub-skills](https://github.com/datahub-project/datahub-skills) — developer
  skills for building DataHub connectors, reviewing connector PRs, and writing
  ingestion code
- [DataHub documentation](https://docs.datahub.com)

## License

Apache-2.0. The DataHub mark is a trademark — see
[assets-NOTICE.md](assets-NOTICE.md).
