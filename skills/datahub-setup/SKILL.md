---
name: datahub-setup
description: Help the user configure and verify their DataHub Cloud connection in Claude Code — set up the MCP server, test connectivity, and confirm authentication is working.
version: "1.0.0"
---

# DataHub Setup Skill

Guide the user through connecting Claude Code to their DataHub Cloud instance via the MCP server.

## Capabilities
- Verify the MCP server is reachable and authenticated
- Help configure authentication (personal access tokens)
- Test connectivity by running a simple search
- Troubleshoot common connection issues

## Workflow

1. **Check connectivity** — attempt a simple MCP call to verify the server is reachable
2. **Verify authentication** — confirm the user's token is valid and has the right permissions
3. **Run a smoke test** — execute a simple catalog search to confirm end-to-end functionality
4. **Report status** — clearly state whether the connection is working and what instance it's connected to

## MCP Server Details
- **URL**: `https://mcp.datahub.com/mcp`
- **Auth**: Personal Access Token (PAT) from DataHub Cloud Settings → Access Tokens
- **Transport**: HTTP

## Configuration

The DataHub Cloud MCP server is pre-configured in this plugin's `.mcp.json`. If authentication is required, users typically need to set their PAT as an environment variable or pass it in the MCP server configuration.

Common environment variable: `DATAHUB_TOKEN`

## Troubleshooting
- **401 Unauthorized**: Token is missing or expired — generate a new one from DataHub Cloud Settings
- **403 Forbidden**: Token exists but lacks permissions — contact your DataHub admin
- **Connection refused / timeout**: Check network access to `mcp.datahub.com`
- **No results returned**: Authentication may be working but the user's permissions scope may be limited

## Examples
- "Set up my DataHub Cloud connection"
- "Test if DataHub is connected"
- "Why isn't DataHub working?"
- "How do I authenticate with DataHub Cloud?"
