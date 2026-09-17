---
name: datahub-setup
description: Verify and troubleshoot the DataHub Cloud connection — confirm the MCP server is reachable, authentication is working, and Claude can access the catalog. Use when the user wants to set up DataHub, test the connection, or fix connectivity issues.
version: "1.0.0"
argument-hint: "[optional: what is going wrong]"
---

# DataHub Setup Skill

Help users verify and troubleshoot their DataHub Cloud connection via the MCP server.

## When to use this skill
- "Set up my DataHub connection"
- "Is DataHub connected?"
- "Why isn't DataHub working?"
- "How do I authenticate with DataHub Cloud?"

## How the connection works

This plugin connects to DataHub Cloud via the MCP server at `https://mcp.datahub.com/mcp`. Authentication is handled automatically via OAuth — no tokens or environment variables needed.

## Verification workflow

1. **Test connectivity** — call `get_me` to confirm the MCP server is reachable and the user is authenticated; this returns the authenticated user's profile
2. **Smoke test** — run a minimal search to confirm catalog access end-to-end:

   ```
   search(query="*", count=1)
   ```

   Interpreting the pair matters more than either result alone:

   | `get_me` | `search` | Diagnosis |
   | --- | --- | --- |
   | fails | — | Not connected or not authenticated — sign in with `/mcp` |
   | works | returns results | Working normally |
   | works | returns nothing | Connected, but the account may lack read access |
3. **Confirm a known entity resolves** — `get_entities(urns=["urn:li:corpuser:datahub"])`.
   That entity exists on every DataHub instance, so a failure here is the
   connection or permissions, never a missing asset.
4. **Report status** — state whether the connection works and, if not, which of
   the checks above failed. Run them in order and stop at the first failure;
   a later check failing for an earlier reason is how people chase the wrong
   problem.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 401 Unauthorized | OAuth session expired | Re-authenticate via the MCP OAuth flow |
| 403 Forbidden | Insufficient permissions | Contact your DataHub admin |
| Connection timeout | Network can't reach mcp.datahub.com | Check firewall or VPN settings |
| Empty results, new instance | No metadata ingested yet | Normal — not a fault. Confirm with the DataHub admin before debugging further |
| Empty results, established instance | Auth works but permissions are limited | Contact your DataHub admin to expand access |

## Common mistakes

- **Declaring success without verifying.** Always run the checks; never report
  the connection as working because the plugin is installed.
- **Retrying instead of diagnosing.** When a check fails, work the
  troubleshooting table — a second identical attempt tells you nothing.
- **Reading an empty result as a failure.** On a newly ingested instance an
  empty catalog is expected.

## Rules
- Do not guide users through CLI installation, token creation, or environment
  variables — this plugin uses the MCP server and OAuth only
- Never claim the connection is fine without having called a tool
