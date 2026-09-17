---
name: catalog-quality
description: Check data quality assertions and results in DataHub Cloud
argument-hint: "[dataset, or a health question]"
---

Check data quality in DataHub Cloud for: **$ARGUMENTS**

1. **Find the asset** with `search`, then read its health with `get_entities` —
   assertion results, freshness, and volume signals travel with the entity.
2. **Separate failing from stale.** An assertion that hasn't run recently is a
   different problem from one that ran and failed; say which you found.
3. **When something is failing, trace upstream.** `get_lineage` upstream usually
   explains a freshness or volume breach faster than the asset's own history.
4. **Check lifecycle context** with `list_lifecycle_stages` before raising an
   alarm about a deprecated or pre-production asset.
5. **Report what a human should do next** — which asset, which check, which
   owner. Include URNs.

Writes such as creating assertions or resolving incidents depend on your
account's DataHub permissions. Show the intended change and get confirmation
before making one.

If no arguments were given, ask what to check.
