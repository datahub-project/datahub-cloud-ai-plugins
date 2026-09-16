---
expect:
  urns: array
---

{
  "entities": [
    {
      "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.analytics.revenue_metrics,PROD)",
      "type": "DATASET",
      "name": "revenue_metrics",
      "assertions": {
        "assertions": [
          {
            "assertion": {
              "urn": "urn:li:assertion:freshness-revenue-metrics",
              "type": "FRESHNESS",
              "description": "Updated within the last 26 hours"
            },
            "runEvents": {
              "runEvents": [
                {
                  "status": "COMPLETE",
                  "result": { "type": "FAILURE", "nativeResults": { "reason": "Last update was 31 hours ago" } },
                  "timestampMillis": 1757980800000
                }
              ]
            }
          },
          {
            "assertion": {
              "urn": "urn:li:assertion:volume-revenue-metrics",
              "type": "VOLUME",
              "description": "Row count between 1000 and 100000"
            },
            "runEvents": {
              "runEvents": [
                {
                  "status": "COMPLETE",
                  "result": { "type": "SUCCESS" },
                  "timestampMillis": 1757980800000
                }
              ]
            }
          }
        ]
      }
    }
  ]
}
