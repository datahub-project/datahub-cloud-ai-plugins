---
name: catalog-sql
description: Write accurate SQL grounded in the DataHub Cloud data catalog
argument-hint: "[the question the query should answer]"
---

Write SQL grounded in DataHub Cloud metadata to answer: **$ARGUMENTS**

Never write SQL from memory or from table names that merely look right.

1. **Ground first.** Call `find_sql_context` before writing anything or calling
   any other tool. It returns anchor documents, rendered query patterns, the
   dialect, and the datasets those patterns use.
2. **Prefer real queries over inference.** `get_dataset_queries` shows how
   analysts actually query a table — the joins, the filters, the grain. A pattern
   in production beats a schema guess.
3. **Verify every table and join key** against live schema with
   `list_schema_fields` before relying on a column. Confirm the grain, and check
   whether the filters you plan to apply are the ones existing queries use.
4. **Draft with `draft_sql_for_tables`** where it helps, then read the result
   critically — treat a low-confidence signal as a reason to go back to step 1,
   not a caveat to pass on.
5. **Cite your evidence.** Name the dataset URNs and the documents or queries the
   SQL is based on, and flag any assumption you could not verify.
6. **Read-only.** Produce a single `SELECT` (read-only CTEs are fine). Refuse DDL
   and DML. Executing the query needs a warehouse connection, which this plugin
   does not provide — hand the SQL over rather than pretending to run it.

If no arguments were given, ask what question the query should answer.
