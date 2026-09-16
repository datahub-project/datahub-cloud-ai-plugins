---
type: llm
focus: last_message
weight: 1
---

PASS if the response:
- Produces a valid SELECT query using only columns verified from the schema (date, region, revenue_usd)
- Aggregates revenue by month and region
- Applies a 6-month date filter
- Cites the revenue_metrics dataset as the source
- Does not invent column names not present in the schema

FAIL if the response:
- Uses column names not found in list_schema_fields (e.g. sale_date, amount, country)
- Includes INSERT, UPDATE, DELETE, or DDL statements
- Presents a query without referencing any DataHub catalog source
