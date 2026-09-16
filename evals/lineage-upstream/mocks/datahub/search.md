---
expect:
  query: string
---

{
  "searchResults": [
    {
      "entity": {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.analytics.orders,PROD)",
        "type": "DATASET",
        "name": "orders",
        "platform": { "name": "snowflake" },
        "properties": { "description": "Core orders table containing all customer transactions." }
      }
    }
  ],
  "total": 1
}
