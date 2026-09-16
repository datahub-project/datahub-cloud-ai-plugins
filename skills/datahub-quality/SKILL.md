---
name: datahub-quality
description: Explore and manage data quality in DataHub Cloud — view assertions, check results, investigate failures, and understand the health of datasets and pipelines.
version: "1.0.0"
---

# DataHub Quality Skill

Use the `datahub` MCP tools to inspect and manage data quality assertions and results.

## Capabilities
- List assertions defined on a dataset
- Check the latest assertion run results (pass/fail)
- Investigate assertion failures with details and timestamps
- Summarize the overall health of a dataset or domain
- Identify datasets with no assertions (no coverage)

## Workflow

1. **Identify the scope** — single dataset, domain, or all datasets owned by a team
2. **Fetch assertions** — retrieve assertion definitions for the target entities
3. **Check results** — fetch the latest run results for each assertion
4. **Analyze** — identify failures, flapping assertions, and gaps in coverage
5. **Report** — summarize health status clearly with actionable details for failures

## Rules
- Always show the assertion type (volume, freshness, field, SQL, schema) alongside results
- For failures, include the failure reason, affected columns/conditions, and timestamp
- When no assertions are found, note that this dataset has no quality monitoring
- Do not suggest fixing data issues — only report what the assertions found
- Group results by dataset when reporting on multiple entities

## Examples
- "What's the data quality status for the orders dataset?"
- "Show me all failing assertions in the Finance domain"
- "Which datasets owned by the Data Engineering team have no quality checks?"
- "When did the freshness assertion on customer_dim last fail?"
