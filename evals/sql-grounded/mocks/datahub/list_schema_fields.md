---
expect:
  urn: string
---

{
  "fields": [
    { "fieldPath": "date", "type": "DATE", "description": "The calendar date of the revenue record." },
    { "fieldPath": "region", "type": "VARCHAR", "description": "Geographic region (e.g. AMER, EMEA, APAC)." },
    { "fieldPath": "product_line", "type": "VARCHAR", "description": "Product line identifier." },
    { "fieldPath": "revenue_usd", "type": "FLOAT", "description": "Gross revenue in US dollars for the given date and region." },
    { "fieldPath": "order_count", "type": "INTEGER", "description": "Number of orders contributing to revenue." }
  ]
}
