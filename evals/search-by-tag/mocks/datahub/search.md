---
expect:
  query: string
---

{
  "searchResults": [
    {
      "entity": {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.analytics.customers,PROD)",
        "type": "DATASET",
        "name": "customers",
        "platform": { "name": "snowflake" },
        "properties": { "description": "Core customer records including PII fields such as name, email, and address." },
        "tags": { "tags": [{ "tag": { "urn": "urn:li:tag:PII", "properties": { "name": "PII" } } }] },
        "ownership": { "owners": [{ "owner": { "urn": "urn:li:corpuser:alice", "username": "alice" } }] }
      }
    },
    {
      "entity": {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.analytics.orders,PROD)",
        "type": "DATASET",
        "name": "orders",
        "platform": { "name": "snowflake" },
        "properties": { "description": "Order transactions including customer identifiers." },
        "tags": { "tags": [{ "tag": { "urn": "urn:li:tag:PII", "properties": { "name": "PII" } } }] },
        "ownership": { "owners": [{ "owner": { "urn": "urn:li:corpuser:bob", "username": "bob" } }] }
      }
    }
  ],
  "total": 2
}
