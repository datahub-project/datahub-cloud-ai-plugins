---
type: llm
focus: last_message
weight: 1
---

PASS if the response:
- Identifies that the freshness assertion is failing
- Explains the failure reason (last update was 31 hours ago, exceeds the 26-hour threshold)
- Notes that the volume assertion is passing
- Presents a clear health summary (1 of 2 checks failing)

FAIL if the response:
- Reports the dataset as fully healthy when a check is failing
- Invents assertion types or failure reasons not present in the results
- Suggests fixes or data corrections (this skill is read-only)
