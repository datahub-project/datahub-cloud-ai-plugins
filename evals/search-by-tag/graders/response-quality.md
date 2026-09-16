---
type: llm
focus: last_message
weight: 1
---

PASS if the response:
- Lists both datasets found (customers, orders)
- Identifies them as Snowflake datasets
- Mentions they are tagged PII
- Includes the entity URN or a direct reference for at least one result

FAIL if the response:
- Makes up dataset names not present in the search results
- Omits the tag context entirely
- Is just a raw JSON dump with no explanation
