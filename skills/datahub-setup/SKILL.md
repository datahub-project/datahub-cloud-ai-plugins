---
name: datahub-setup
description: Verify and troubleshoot the DataHub Cloud connection — confirm the MCP server is reachable, authentication is working, and Claude can access the catalog. Use when the user wants to set up DataHub, test the connection, or fix connectivity issues.
version: "1.0.0"
---

# DataHub Setup Skill

Help users verify and troubleshoot their DataHub Cloud connection via the MCP server.

## When to use this skill
- "Set up my DataHub connection"
- "Is DataHub connected?"
- "Why isn't DataHub working?"
- "How do I authenticate with DataHub Cloud?"

## How the connection works

This plugin connects to DataHub Cloud via the MCP server at `https://mcp.datahub.com/mcp`. No CLI installation is needed. Authentication uses a **Personal Access Token (PAT)** from your DataHub Cloud instance.

## Verification workflow

1. **Test connectivity** — call `get_me` to confirm the MCP server is reachable and the token is valid; this returns the authenticated user's profile
2. **Smoke test** — run a simple `search` call to confirm catalog access is working end-to-end
3. **Report status** — clearly state whether the connection is working and, if not, what the specific issue is

## Getting a Personal Access Token

1. Log into your DataHub Cloud instance
2. Go to **Settings → Access Tokens**
3. Click **Generate new token** — copy and store it securely
4. Set it as the `DATAHUB_TOKEN` environment variable, or configure it in your MCP client settings

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 401 Unauthorized | Token missing or expired | Generate a new token in DataHub Cloud Settings |
| 403 Forbidden | Token lacks permissions | Contact your DataHub admin to expand token scope |
| Connection timeout | Network can't reach mcp.datahub.com | Check firewall or VPN settings |
| Empty results | Token works but has limited scope | Verify the token has catalog read access |

## Rules
- Never display or log token values — always mask as `<REDACTED>` if asked to show configuration
- Do not guide users through CLI installation — this plugin uses the MCP server only
