---
expect:
  urn: string
---

{
  "queries": [
    {
      "query": "SELECT DATE_TRUNC('month', date) AS month, region, SUM(revenue_usd) AS total_revenue FROM prod.analytics.revenue_metrics GROUP BY 1, 2 ORDER BY 1 DESC, 2",
      "description": "Monthly revenue rollup by region",
      "lastModified": "2026-08-01"
    }
  ]
}
