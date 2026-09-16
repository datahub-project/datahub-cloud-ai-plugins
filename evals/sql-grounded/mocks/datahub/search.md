---
expect:
  query: string
---

{
  "searchResults": [
    {
      "entity": {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.analytics.revenue_metrics,PROD)",
        "type": "DATASET",
        "name": "revenue_metrics",
        "platform": { "name": "snowflake" },
        "properties": { "description": "Daily revenue aggregations by product line and region. Grain: one row per day per region." }
      }
    }
  ],
  "total": 1
}
