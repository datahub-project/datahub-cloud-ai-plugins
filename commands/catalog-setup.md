---
name: catalog-setup
description: Verify and troubleshoot your DataHub Cloud connection
argument-hint: "[optional: what is going wrong]"
---

Verify the DataHub Cloud connection. $ARGUMENTS

There is nothing to install or configure — this plugin declares one MCP server at
`https://mcp.datahub.com/mcp` and authentication is OAuth.

1. **Check the server connected.** In Claude Code, run `/mcp`; the `datahub`
   server should be listed and authenticated. If it shows as needing
   authentication, sign in with `/mcp` or `claude mcp login datahub`.
2. **Confirm identity** with `get_me`, which reports the authenticated user and
   group memberships. This is the fastest way to tell a connection problem from a
   permissions problem.
3. **Prove the catalog answers** with a cheap `search` — if `get_me` works and
   `search` returns nothing, the account is connected but may lack read access to
   the assets in question.
4. **Report what you found**, not just pass or fail: which account you are
   signed in as, and what it can see.

Common causes when it isn't working:

- **Not signed in.** The endpoint answers `401` until OAuth completes; that is
  expected, not a fault.
- **No DataHub Cloud account.** This plugin requires one.
- **Tools missing rather than failing.** Tool availability follows your account's
  permissions, so a missing write tool is usually a permissions result.
