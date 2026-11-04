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

Codex reads the root `plugin.json`, including `extensions.com.openai.interface`;
older Codex hosts use `.codex-plugin/plugin.json`. Other Agent Plugins clients
read the root `plugin.json` and `mcp.json`.

To install this checkout as a local Codex marketplace, run:

```bash
codex plugin marketplace add /absolute/path/to/datahub-cloud-ai-plugins
codex plugin add datahub-cloud@datahub-cloud-ai-plugins
```

## Authentication

The plugin connects to the DataHub MCP server over **OAuth 2.0 with dynamic
client registration** — no tokens or environment variables, and no credentials in
the repo.

**Claude Code** asks for a **DataHub MCP URL** when the plugin is enabled. Enter
your tenant's endpoint, any `https://` URL ending in `/mcp`:

| Deployment | DataHub MCP URL |
| --- | --- |
| DataHub Cloud | `https://<tenant>.acryl.io/mcp` or `https://<tenant>.datahub.com/mcp` |
| Custom domain | `https://<your-domain>/mcp` |
| Shared gateway (for example, a tenant behind an IP allowlist) | `https://mcp.datahub.com/mcp` |

Connecting straight to the tenant skips the gateway's tenant-selection screen.
Change the value later in `/config`.

**Codex and other Agent Plugins clients** connect to the shared gateway at
`https://mcp.datahub.com/mcp`. Agent Plugins 1.0.0 forbids substitution in remote
MCP URLs, and Codex has no install-time prompt for one, so these manifests keep a
fixed endpoint.

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

## Manifests

One plugin, described to three clients:

| Manifest | Read by | MCP config |
| --- | --- | --- |
| `.claude-plugin/plugin.json` | Claude Code | `.mcp.json` |
| `.codex-plugin/plugin.json` | Codex | `.codex-plugin/mcp.json` (this one declares `skills`) |
| `plugin.json` | Agent Plugins 1.0.0 clients | `mcp.json` |

They repeat the same identity — name, version, description, author, license,
keywords — so **change one and change all three**. OpenAI reads presentation and
legal URLs from `extensions.com.openai.interface` in the portable root manifest;
the `.codex-plugin/plugin.json` interface is a compatibility fallback. Keep those
two interface blocks in sync. Claude Code's `metadata` block is free-form and it
does not read it.

The three MCP configs differ in two ways:

- **Transport label.** `.mcp.json` and `.codex-plugin/mcp.json` use
  `"type": "http"`. The portable `mcp.json` uses `"type": "streamable-http"`, as
  required by the Agent Plugins schema.
- **Endpoint.** `.mcp.json` reads its URL from the Claude Code `userConfig`
  option `datahub_mcp_url` (`${user_config.datahub_mcp_url}`), so it carries no
  `oauth_resource`; the client takes the resource from the tenant's metadata.
  `.codex-plugin/mcp.json` and `mcp.json` both point to the shared gateway, and
  `scripts/package.py` fails the build if they differ.

Codex has its own MCP file because Codex doesn't substitute `${user_config.*}`.

Two things worth knowing when editing by hand:

- **`claude plugin validate` checks `.mcp.json` only on Claude Code v2.1.281 or
  later**, including that every `${user_config.KEY}` names a declared option.
  Check the server actually connects with `/mcp` either way.
- **The primary icon must stay 1:1.** Anthropic's MCP Directory submission
  requires a square SVG; `assets/logo-square.svg` is the square one and
  `assets/logo.svg` is the wide original.

Before opening a PR:

```bash
claude plugin validate . --strict
```

## Related

- [datahub-skills](https://github.com/datahub-project/datahub-skills) — developer
  skills for building DataHub connectors, reviewing connector PRs, and writing
  ingestion code
- [DataHub documentation](https://docs.datahub.com)

## Portable ZIP and releases

Download `datahub-cloud-portable-<version>.zip` from
[GitHub Releases](https://github.com/datahub-project/datahub-cloud-ai-plugins/releases).
Each ZIP contains a `datahub-cloud/` directory with the portable `plugin.json`
and `mcp.json`, Claude and Codex manifests, local marketplace metadata, skills,
and logo assets.
Extract the ZIP and use that directory with your client's local plugin installer.
Evaluation fixtures and local development files are excluded.

To build locally with Python 3.10 or newer:

```bash
python3 scripts/package.py
```

The build writes the ZIP and a `.zip.sha256` checksum to `dist/`. To verify a
download on macOS, run `shasum -a 256 -c <zip-filename>.sha256` in the download
directory; on Linux, use `sha256sum --check <zip-filename>.sha256`.

Before releasing, run the same checks used by CI:

```bash
python3 -m pip install -r requirements-dev.txt
ruff format --check scripts tests
ruff check scripts tests
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

To publish a new version:

1. Update `version` in `plugin.json`, `.claude-plugin/plugin.json`, and
   `.codex-plugin/plugin.json` to the same semantic version. Commit and merge
   those changes to `main` after the checks pass.
2. As a repository administrator, tag the merged commit and push the tag
   (replace `1.0.1` with your version):

   ```bash
   git switch main
   git pull --ff-only
   git tag -a v1.0.1 -m "DataHub Cloud 1.0.1"
   git push origin v1.0.1
   ```

3. The **Portable plugin release** workflow checks that the tagged commit is
   reachable from the current `main` branch, validates the version, builds the ZIP,
   and publishes a GitHub Release with the ZIP, checksum, and generated release
   notes. Tags such as `v1.1.0-rc.1` create prereleases. A tag/version mismatch
   fails before publication; existing releases are never overwritten.

Pull requests and pushes to `main` run the same packaging checks and retain the
ZIP as a workflow artifact. You can also run the workflow manually to build an
artifact without publishing a release. Publication uses the workflow's
`GITHUB_TOKEN` with `contents: write`; no separate release token is needed.

The repository's release-tag ruleset restricts creation and updates of `v*`
tags to repository administrators. This GitHub-side protection matters because
the workflow itself comes from the tagged commit. The ancestry check rejects
accidental tags on unmerged commits; the ruleset controls who can trigger a
release or change its workflow through a tag.

The ruleset configuration is recorded in `.github/release-tag-ruleset.json`.
It must be configured separately in GitHub; committing the file does not activate
the policy. For a new repository, an administrator can apply it with:

```bash
gh api --method POST repos/OWNER/REPO/rulesets \
  --input .github/release-tag-ruleset.json
```

Inspect existing rulesets before applying this configuration to avoid creating
duplicates. Ordinary PRs and manual artifact builds do not require a release tag
or a commit on `main`.

## License

Apache-2.0. The DataHub mark is a trademark — see
[assets-NOTICE.md](assets-NOTICE.md).
