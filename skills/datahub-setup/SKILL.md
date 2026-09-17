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
2. **Smoke test** — run a simple `search` call to confirm catalog access is working end-to-end
3. **Report status** — clearly state whether the connection is working and, if not, what the specific issue is

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 401 Unauthorized | OAuth session expired | Re-authenticate via the MCP OAuth flow |
| 403 Forbidden | Insufficient permissions | Contact your DataHub admin |
| Connection timeout | Network can't reach mcp.datahub.com | Check firewall or VPN settings |
| Empty results | Auth works but permissions are limited | Contact your DataHub admin to expand access |

## Rules
- Do not guide users through CLI installation — this plugin uses the MCP server only
