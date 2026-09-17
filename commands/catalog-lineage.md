---
name: catalog-lineage
description: Explore data lineage in DataHub Cloud
argument-hint: "[dataset, column, or an impact question]"
---

Trace lineage in DataHub Cloud for: **$ARGUMENTS**

1. **Resolve the target** with `search`, then confirm you have the right asset —
   getting the wrong `orders` table makes everything downstream wrong.
2. **Pick a direction and depth.** `get_lineage` takes upstream or downstream and
   a hop count. Impact analysis is downstream; root-cause is upstream. Start
   shallow: a 3-hop graph on a busy warehouse is unreadable, and deeper
   traversals are slow.
3. **For a specific path between two assets**, use `get_lineage_paths_between`
   rather than walking the graph manually — it returns intermediate
   transformations and the SQL behind them.
4. **Go column-level when the question is column-level.** Table lineage will
   claim a dashboard breaks when only an unused column changed.
5. **Report the blast radius concretely**: name the affected datasets,
   dashboards and pipelines with their URNs, and separate what definitely breaks
   from what merely depends on the asset.

If no arguments were given, ask which asset to trace.
