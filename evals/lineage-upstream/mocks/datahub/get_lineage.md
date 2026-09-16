---
expect:
  urn: string
---

{
  "relationships": [
    {
      "entity": {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:kafka,prod.orders-events,PROD)",
        "type": "DATASET",
        "name": "orders-events",
        "platform": { "name": "kafka" },
        "properties": { "description": "Raw order event stream from the transaction service." }
      },
      "type": "Consumes"
    },
    {
      "entity": {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,prod.stg_orders,PROD)",
        "type": "DATASET",
        "name": "stg_orders",
        "platform": { "name": "dbt" },
        "properties": { "description": "Staging model that cleans and normalises raw order events." }
      },
      "type": "Consumes"
    }
  ],
  "total": 2
}
