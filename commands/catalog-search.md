---
name: catalog-search
description: Search the DataHub Cloud data catalog
argument-hint: "[what to find, or a question about your data]"
---

Search the DataHub Cloud catalog to answer: **$ARGUMENTS**

Work through the DataHub MCP tools:

1. **Search** with `search`. Use `/q` syntax for precision — `tag:PII`, wildcards
   like `revenue_*`, and boolean logic. Filter by platform, domain or entity type
   rather than post-filtering a broad result set.
2. **Resolve names to URNs before filtering on them.** Tag, domain, glossary-term
   and owner filters take full URNs (`urn:li:tag:PII`), not display names — a
   display name returns zero results silently. Search for the tag or domain
   entity first to get its URN.
3. **Hydrate** the entities that matter with `get_entities`, and
   `list_schema_fields` when the question is about columns.
4. **Answer with evidence.** Cite the URN of every asset you rely on, and say
   what you checked rather than only what you concluded. If the catalog is
   ambiguous, say so instead of guessing.

If no arguments were given, ask what they want to find.
