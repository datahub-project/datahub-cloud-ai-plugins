# OpenAI submission worksheet

Create a **With MCP** draft in the [plugin submission portal](https://platform.openai.com/plugins). The source package uses the portable Agent Plugins layout; the portal requires the production MCP endpoint and a separate upload of the final `skills/` bundle.

## Listing copy

- **Name:** DataHub Cloud
- **Short description:** Explore your data catalog and draft grounded SQL.
- **Long description:** Find datasets and owners, trace upstream and downstream lineage, inspect data quality, and draft SELECT queries grounded in DataHub Cloud metadata.
- **Developer:** DataHub Project (select the matching verified publisher identity in the portal)
- **Website:** https://datahubproject.io
- **MCP URL type:** Universal
- **MCP URL:** https://mcp.datahub.com/mcp
- **Authentication:** OAuth; confirm the production server's configuration in the portal
- **Starter prompts:** Use the three `defaultPrompt` entries in `plugin.json`.
- **Release notes:** Initial portable DataHub Cloud plugin with catalog search, lineage, data quality, connection troubleshooting, and grounded SQL skills.

## Positive test cases

Use a reviewer demo account with a searchable dataset, a dataset with upstream lineage, and a dataset with assertion history. Replace the generic entity descriptions below with their actual demo-catalog names and URNs before entering tests in the portal.

| Prompt | Expected workflow | Expected result |
| --- | --- | --- |
| Find the demo orders dataset and show its owner and columns. | `datahub-search` uses `search`, `get_entities`, and `list_schema_fields`. | Matching dataset, URN, owner when present, and verified fields. |
| Show what feeds the demo orders dataset, up to three hops. | `datahub-lineage` uses `search` and `get_lineage` upstream. | Upstream entities and paths returned by DataHub, with URNs. |
| Which quality checks are failing for the demo revenue dataset? | `datahub-quality` uses `search` and `get_entities`. | Latest assertion outcomes and timestamps, or an explicit statement that no checks exist. |
| Draft a SELECT query for monthly revenue using the demo revenue dataset. | `datahub-sql-workflow` checks existing queries and schema before drafting. | SELECT SQL using verified tables and columns, with DataHub entity references and stated assumptions. |
| Test my DataHub Cloud connection. | `datahub-setup` calls `get_me` and performs a small `search`. | Authenticated connection status and a catalog access result. |

## Negative test cases

| Prompt or scenario | Expected behavior | Why |
| --- | --- | --- |
| Write a DELETE statement to remove rows from the demo orders dataset. | Decline the destructive SQL request within this workflow; offer a read-only SELECT alternative. | The SQL skill is scoped to SELECT queries. |
| Tell me the owner and columns of a dataset that does not appear in the demo catalog. | Report that no verified match was found; ask for a correct name or URN. | Catalog facts must come from DataHub results. |
| With an expired or unauthorized OAuth session, show the demo revenue assertions. | Report the authentication or permission failure and point to reconnection or an administrator. | The plugin cannot bypass DataHub access controls. |

## Publisher tasks before submitting

1. Confirm the publishing organization has **Apps Management** write access and a verified business identity that matches the DataHub publisher.
2. Supply production logo, support URL, privacy policy URL, terms URL, and intended availability regions in the portal. These values are not in this repository, so do not invent them in the manifest.
3. Ensure the production MCP endpoint supports reviewer OAuth login and provide a demo account with the datasets, lineage, and assertion history used by the tests. Confirm it needs no MFA, email approval, or private-network access during review.
4. Complete the portal's domain verification challenge for `mcp.datahub.com` (or an allowed parent host) using the exact token it supplies. Do not replace an existing plugin's challenge token.
5. Scan Tools and review each exposed tool's schema, output, and `readOnlyHint`, `openWorldHint`, and `destructiveHint` annotations. These are server properties and cannot be validated from this package alone. Remove auth secrets and unnecessary personal data from tool responses.
6. Upload the final skill bundle, replace demo placeholders in the eight test cases, review the scan results, and submit the draft for OpenAI review.

Requirements are from the [OpenAI submission guide](https://developers.openai.com/plugins/deploy/submission) and [portable packaging guide](https://developers.openai.com/plugins/build/plugins).
