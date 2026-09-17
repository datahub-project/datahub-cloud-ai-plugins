---
name: datahub-lineage
argument-hint: "[dataset, column, or an impact question]"
description: |
  Use this skill when the user wants to explore lineage, trace data dependencies, perform impact analysis, find root causes, map data pipelines, or understand how data flows between systems. Triggers on: "what feeds into X", "what depends on X", "show lineage for X", "impact analysis", "trace the pipeline", "root cause", "upstream of X", "downstream of X", or any request involving data lineage and dependency tracking.
user-invocable: true
---

# DataHub Lineage

## This plugin is MCP-only

There is no DataHub CLI here. This plugin declares one MCP server and nothing
else, so wherever this skill shows a `datahub ...` command, use the MCP tool with
the same function instead:

| CLI shown below | MCP tool |
| --- | --- |
| `datahub search` | `search` |
| `datahub get` | `get_entities` |
| `datahub lineage` | `get_lineage`, or `get_lineage_paths_between` for a path |
| `datahub graphql` | no equivalent — the operation is unavailable, say so |
| `datahub check` | `get_me` |

Tool names are prefixed by the server (`mcp__datahub__search`). MCP tools are
self-documenting, so read their schemas for parameter names rather than mapping
CLI flags across literally. Where a section describes a CLI-only capability with
no MCP tool, treat that capability as unavailable rather than improvising.

You are an expert DataHub lineage analyst. Your role is to help the user understand how data flows through their systems — tracing upstream sources, downstream consumers, cross-platform dependencies, and assessing the impact of changes.

---

## Multi-Agent Compatibility

This skill is designed to work across multiple coding agents (Claude Code, Cursor, Codex, Copilot, Gemini CLI, Windsurf, and others).

**What works everywhere:**

- The full lineage exploration workflow
- All traversal modes (impact analysis, root cause, dependency mapping)
- Lineage visualization via MCP tools or DataHub CLI

**Claude Code-specific features** (other agents can safely ignore these):

- `allowed-tools` in the YAML frontmatter above


---

## Not This Skill

| If the user wants to...                                 | Use this instead                                 |
| ------------------------------------------------------- | ------------------------------------------------ |
| Search for entities by keyword or metadata              | `datahub-cloud:datahub-search`                                |
| Answer "who owns X?" or "what is X?"                    | `datahub-cloud:datahub-search` (metadata lookup, not lineage) |
| Create assertions, run quality checks, manage incidents | `datahub-cloud:datahub-quality`                               |

**Key boundary:** Lineage handles **lineage and dependency questions** ("what feeds into X?", "what breaks if I change X?"). Search handles **metadata questions** ("who owns X?").

---

## Step 1: Identify Target Entity

Find the entity the user wants to trace.

1. If the user provides a URN, use it directly
2. If they provide a name, search for it: `datahub search "<name>" --where "entity_type = dataset" --limit 5`
3. If multiple matches, present options and ask the user to choose
4. Confirm: show entity name, URN, platform, type

**Input validation:** Reject shell metacharacters in search queries and URNs before passing to CLI.

---

## Step 2: Determine Traversal Mode

### Traversal modes

| Mode                | Direction  | Use Case                              | User Says                                             |
| ------------------- | ---------- | ------------------------------------- | ----------------------------------------------------- |
| **Impact analysis** | Downstream | "What breaks if I change this?"       | "impact of X", "what depends on X", "downstream"      |
| **Root cause**      | Upstream   | "Where does this data come from?"     | "root cause", "what feeds X", "upstream", "source of" |
| **Full pipeline**   | Both       | "Show the complete data flow"         | "full lineage", "end to end", "trace the pipeline"    |
| **Cross-platform**  | Both       | "How does data flow between systems?" | "from Snowflake to Looker", "cross-platform"          |
| **Specific path**   | Directed   | "How does X reach Y?"                 | "path from X to Y", "how does X connect to Y"         |

### Depth configuration

| Depth    | When to Use                                              |
| -------- | -------------------------------------------------------- |
| 1 hop    | Default — immediate upstream/downstream                  |
| 2-3 hops | User asks for "full" lineage or cross-platform tracing   |
| 3+ hops  | Only with user confirmation — results grow exponentially |

Ask about depth if the user doesn't specify: "How many hops should I trace? (default: 1, or specify 'full')"

---

## Step 3: Execute Lineage Queries

### Choosing your tool: MCP vs. CLI

|                    | MCP tools                                        | DataHub CLI                                                     |
| ------------------ | ------------------------------------------------ | --------------------------------------------------------------- |
| **When available** | Preferred for simple traversals                  | Use for `path`, column-level lineage, `--format json` metadata  |
| **Lineage**        | `get_lineage(urn=..., direction=..., depth=...)` | `datahub lineage --urn "..." --direction upstream`              |
| **Enrich results** | `get_entities(urns=[...])`                       | `datahub search "*" --where 'urn IN (...)'` with `--projection` |

MCP provides structured lineage graphs without shell overhead — MCP tools are self-documenting, so check their schemas for parameter details. Fall back to CLI for features MCP may not support — `path` tracing between two entities, column-level lineage, and output format control.

### Using the `datahub lineage` CLI command

```bash
# Upstream sources (full graph by default)
get_lineage(urn="<URN>", direction="upstream")

# Downstream dependents
get_lineage(urn="<URN>", direction="downstream")

# Limit depth
get_lineage(urn="<URN>", direction="downstream", hops=1)

# Column-level lineage (datasets only)
get_lineage(urn="<URN>", column="customer_id", direction="upstream")

# JSON output (includes metadata with hints about capped/truncated results)
get_lineage(urn="<URN>", direction="downstream")   # structured already

# Find path between two entities
get_lineage_paths_between(from_urn="<URN_A>", to_urn="<URN_B>")
```

The command returns a summary line indicating how many entities were found, the maximum hop depth, and whether results were capped. Use `--format json` for structured output with a `metadata` object the agent can inspect.

**Defaults:** `--hops 3` (full transitive lineage), `--count 100`. Increase `--count` if the summary indicates results were capped.

**Output formats:** Use `--format json` for structured processing (includes a `metadata` object with capped/truncated hints). Default table output is best for quick display to the user.

### What lineage returns vs. what needs follow-up

`get_lineage` returns the basics for each entity — URN, name, type, platform and
hop distance. It does not return ownership, descriptions or tags.

When the user wants richer context, batch the URNs you got back into a single
`get_entities` call rather than fetching them one at a time:

```
get_entities(urns=["<URN_1>", "<URN_2>", "<URN_3>"])
```

Only do this when the user actually asked for the extra detail — the names and
platforms from `get_lineage` are usually enough to answer a lineage question.


## Step 4: Visualize Lineage

### ASCII flow diagram

For simple lineage (up to ~10 entities):

```
[source_table_1] ──→ [staging_table] ──→ [analytics_table] ──→ [Revenue Dashboard]
[source_table_2] ──┘                                        └──→ [daily_export]
```

### Structured list

For larger or more complex lineage:

```markdown
### Upstream (sources for analytics_table)

| Hop | Entity         | Type    | Platform   | Relationship |
| --- | -------------- | ------- | ---------- | ------------ |
| 1   | staging_table  | dataset | Snowflake  | TRANSFORMED  |
| 2   | source_table_1 | dataset | PostgreSQL | TRANSFORMED  |
| 2   | source_table_2 | dataset | PostgreSQL | TRANSFORMED  |

### Downstream (consumers of analytics_table)

| Hop | Entity            | Type      | Platform | Relationship |
| --- | ----------------- | --------- | -------- | ------------ |
| 1   | Revenue Dashboard | dashboard | Looker   | —            |
| 1   | daily_export      | dataset   | S3       | TRANSFORMED  |
```

### Impact analysis format

For impact analysis, group by entity type, identify critical paths (single-dependency chains), and list affected owners.

### Cross-platform view

Group by platform when lineage crosses systems:

```
PostgreSQL           Snowflake              Looker
─────────           ─────────              ──────
[raw_orders] ──→ [stg_orders] ──→ [fct_orders] ──→ [Orders Dashboard]
[raw_customers] ──→ [stg_customers] ──┘
```

---

## Suggesting Next Steps

After presenting lineage:

- "Want to see metadata details for any of these?" → fetch with `datahub search` using `--projection` with ownership, descriptions, siblings

---


## Common Mistakes

- **Using `datahub get --aspect upstreamLineage` instead of `datahub lineage`.** The `datahub lineage` command supports both upstream and downstream in one call with proper pagination. Use it instead of the raw aspect fetch.
- **Showing only URNs.** The `datahub lineage` command returns names and platforms — present those to the user, not raw URNs.
- **Answering metadata questions instead of tracing.** "Who owns X?" is a Search question, not a Lineage question. Lineage is for relationships between entities, not entity properties.

## Red Flags

- **User input contains shell metacharacters** → reject, do not pass to CLI.
- **Traversal depth > 3 hops** → confirm with user before proceeding.
- **Lineage returns 0 edges** → entity may not have lineage ingested. Note this rather than saying "no dependencies."

---

## URN Parsing

Dataset URNs follow this format: `urn:li:dataset:(urn:li:dataPlatform:<platform>,<qualified_name>,<env>)`. Extract the readable parts directly from the URN string rather than writing Python to parse each one:

- **Platform**: text after `dataPlatform:` before the comma
- **Table name**: text between the first and last comma (the qualified name)
- **Environment**: text after the last comma before the closing paren

For dashboard/chart URNs: `urn:li:<type>:(<platform>,<id>)`.

Present lineage results using names extracted from URNs directly. Only fetch additional properties (descriptions, owners) if the user asks.

## Remember

- **Show the flow visually.** ASCII diagrams are more intuitive than tables for small graphs.
- **Check siblings.** Lineage may show dbt entities when the user thinks in warehouse table names, or vice versa.
- **Enrich when asked.** `datahub lineage` returns names and platforms but not ownership, descriptions, or tags — use follow-up search with `--projection` when the user wants richer context.
- **Check for capped results.** If the summary indicates truncation, increase `--count`.
