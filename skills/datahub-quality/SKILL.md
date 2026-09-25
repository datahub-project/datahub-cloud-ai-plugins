---
name: datahub-quality
description: Check data quality in DataHub Cloud — view assertion results, find failing checks, investigate data freshness and volume issues, and understand the health of datasets. Use when the user asks about data quality, reliability, or health.
---

# DataHub Quality Skill

Help users understand and investigate data quality using DataHub MCP tools.

## When to use this skill
- "Is the orders table healthy?"
- "Show me failing data quality checks"
- "When was customer_dim last updated?"
- "Which datasets in Finance have quality issues?"
- "Are there any active data incidents?"

## When NOT to use this skill
- General catalog search → use `datahub-cloud:datahub-search`
- Lineage questions → use `datahub-cloud:datahub-lineage`

## Workflow

1. **Identify the scope** — single dataset, a domain, a team's assets, or the full catalog
2. **Fetch assertions** — retrieve the quality checks defined for the target entities
3. **Check results** — get the latest run status for each assertion (pass / fail / no data)
4. **Investigate failures** — for failing checks, retrieve the failure reason, affected columns, and timestamp
5. **Summarize health** — present results in plain language, grouped by dataset when covering multiple entities

## Assertion types to look for
- **Freshness** — was the dataset updated recently enough?
- **Volume** — does the row count look normal?
- **Field / column** — are column values within expected ranges or formats?
- **Schema** — has the table structure changed unexpectedly?
- **SQL** — custom metric queries defined by the data team

## Presenting results
- Lead with an overall health summary ("2 of 5 checks failing")
- For each failure, include: check type, what failed, when it last failed
- Note when a dataset has no quality checks defined ("no monitoring configured")
- Do not suggest fixes or data corrections — report what the assertions found

## MCP tools to use
- `search` — find datasets or filter by `hasFailingAssertions`, `hasActiveIncidents`
- `get_entities` — fetch assertion definitions and latest run results for a dataset
- `list_lifecycle_stages` — check the lifecycle/health stage of an entity

## Rules
- Use DataHub MCP tools exclusively — do not use the DataHub CLI
- This skill is read-only — do not create, modify, or delete assertions
- Never fabricate assertion results — only report what MCP tools return
