---
name: datahub-enrich
description: Add or update metadata on DataHub Cloud entities — add tags, glossary terms, owners, domains, descriptions, and structured properties to datasets, columns, dashboards, and other catalog assets.
version: "1.0.0"
---

# DataHub Enrich Skill

Use the `datahub` MCP tools to add and update metadata on catalog entities.

## Capabilities
- Add/remove tags on entities and columns
- Add/remove glossary terms
- Set owners (users or groups)
- Set or update domains
- Edit entity and column descriptions
- Set structured properties

## Workflow

1. **Identify the target** — find the entity URN using search if not provided
2. **Confirm intent** — if the change is destructive (removing an owner, clearing a tag), confirm with the user first
3. **Apply the change** — use the appropriate MCP mutation tool
4. **Verify** — fetch the entity after the change to confirm it was applied correctly
5. **Report** — summarize what was changed

## Rules
- Always resolve entity URNs before mutating — never guess a URN
- Ask for confirmation before removing metadata (owners, tags, glossary terms)
- When adding glossary terms, search for the term first to get the exact URN
- Only apply mutations the user has explicitly requested
- Report the exact URN and change made after each operation

## Examples
- "Tag the orders dataset as PII"
- "Add the Finance domain to all tables owned by alice@company.com"
- "Update the description for the revenue_metrics dashboard"
- "Set the Data Engineering team as owner of the ETL pipeline"
