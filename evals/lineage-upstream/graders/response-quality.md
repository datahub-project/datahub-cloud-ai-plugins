---
type: llm
focus: last_message
weight: 1
---

PASS if the response:
- Identifies both upstream sources (the Kafka topic orders-events and the dbt staging model stg_orders)
- Clearly describes the direction as upstream (where the data comes from)
- Mentions the platforms (Kafka, dbt)

FAIL if the response:
- Confuses upstream and downstream
- Invents sources not present in the lineage results
- Reports only one upstream source without explaining the other
