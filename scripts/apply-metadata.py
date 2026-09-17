#!/usr/bin/env python3
"""Generate every manifest from plugin-metadata.json.

One plugin is described by five files across three schemas — Claude Code, Codex,
and Agent Plugins — plus two MCP configs that differ only in filename and
wrapper. Editing them by hand is how they drift, so this is the only thing that
writes them. Edit plugin-metadata.json, then run this.

  --check       verify the manifests already match, exit 1 if not
  --check-urls  additionally check every URL still resolves (needs network)
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
M = json.loads((HERE / "plugin-metadata.json").read_text())
CHECK = "--check" in sys.argv
CHECK_URLS = "--check-urls" in sys.argv


def claude_plugin():
    """Claude Code reads .claude-plugin/plugin.json. `metadata` is free-form and
    Claude Code does not read it, so it carries the fields the schema has no
    home for — the icon and the directory-submission URLs."""
    return {
        "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
        "name": M["name"],
        "displayName": M["displayName"],
        "version": M["version"],
        "description": M["description"],
        "author": M["author"],
        "homepage": M["homepage"],
        "repository": M["repository"],
        "license": M["license"],
        "keywords": M["keywords"],
        "metadata": {
            "icon": f"./{M['icon']}",
            "iconWide": f"./{M['iconWide']}",
            "tagline": M["tagline"],
            "documentationURL": M["documentationURL"],
            "privacyPolicyURL": M["privacyPolicyURL"],
            "termsOfServiceURL": M["termsOfServiceURL"],
            "dataProcessingAgreementURL": M["dataProcessingAgreementURL"],
            "supportURL": M["supportURL"],
            "connectionRequirements": M["connectionRequirements"],
        },
    }


def codex_plugin():
    """Codex reads .codex-plugin/plugin.json and synthesizes a metadata-less stub
    when it is absent. Field names matter: it is `defaultPrompt`, not
    `defaultPrompts`, and `category` must be one Codex recognizes."""
    return {
        "name": M["name"],
        "version": M["version"],
        "description": M["description"],
        "author": M["author"],
        "homepage": M["homepage"],
        "repository": M["repository"],
        "license": M["license"],
        "keywords": M["keywords"],
        "mcpServers": "./.mcp.json",
        "interface": {
            "displayName": M["displayName"],
            "shortDescription": M["shortDescription"],
            "longDescription": M["longDescription"],
            "developerName": M["author"]["name"],
            "category": M["category"],
            "capabilities": M["capabilities"],
            "websiteURL": M["websiteURL"],
            "privacyPolicyURL": M["privacyPolicyURL"],
            "termsOfServiceURL": M["termsOfServiceURL"],
            "supportURL": M["supportURL"],
            "brandColor": M["brandColor"],
            "composerIcon": f"./{M['icon']}",
            "logo": f"./{M['icon']}",
            "defaultPrompt": M["defaultPrompt"],
            "screenshots": [],
        },
    }


def agent_plugin():
    """Agent Plugins 1.0.0 root manifest. CLOSED schema: only these ten fields
    are permitted, so there is nowhere here for an icon or the legal URLs."""
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": M["name"],
        "version": M["version"],
        "description": M["description"],
        "author": M["author"],
        "homepage": M["homepage"],
        "repository": M["repository"],
        "license": M["license"],
        "keywords": M["keywords"],
    }


def claude_mcp():
    """Claude Code and Codex both read .mcp.json. The `mcpServers` wrapper is
    required — without it the server silently never loads, and `claude plugin
    validate` does not catch it because it only validates the manifest."""
    return {"mcpServers": {"datahub": {"url": M["mcpServerURL"]}}}


def agent_mcp():
    """Agent Plugins uses mcp.json, requires an explicit transport type, and
    pins a $schema that must match plugin.json's."""
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {"datahub": {"type": "streamable-http", "url": M["mcpServerURL"]}},
    }


TARGETS = [
    (HERE / ".claude-plugin/plugin.json", claude_plugin),
    (HERE / ".codex-plugin/plugin.json", codex_plugin),
    (HERE / "plugin.json", agent_plugin),
    (HERE / ".mcp.json", claude_mcp),
    (HERE / "mcp.json", agent_mcp),
]

drift = []
for path, build in TARGETS:
    want = json.dumps(build(), indent=2) + "\n"
    have = path.read_text() if path.exists() else None
    rel = path.relative_to(HERE)
    if have == want:
        continue
    if CHECK:
        drift.append(str(rel))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(want)
        print(f"  updated {rel}")

if CHECK and drift:
    print("manifests have drifted from plugin-metadata.json:", file=sys.stderr)
    for d in drift:
        print(f"  {d}", file=sys.stderr)
    print("run scripts/apply-metadata.py to regenerate", file=sys.stderr)
    sys.exit(1)

# Every declared asset path must resolve, and the primary icon must be square:
# Anthropic's MCP Directory submission requires a 1:1 SVG.
import re
for rel in (M["icon"], M["iconWide"]):
    assert (HERE / rel).is_file(), f"icon missing: {rel}"
vb = [float(x) for x in re.search(r'viewBox="([^"]*)"', (HERE / M["icon"]).read_text()).group(1).split()]
assert abs(vb[2] - vb[3]) < 0.01, f"primary icon not 1:1: {vb[2]}x{vb[3]}"
print("  manifests in sync with plugin-metadata.json; icon paths resolve")

if CHECK_URLS:
    import subprocess
    urls = sorted({v for v in M.values() if isinstance(v, str) and v.startswith("http")}
                  | {M["author"]["url"]})
    bad = []
    for u in urls:
        code = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-L", "--max-time", "15", u],
            capture_output=True, text=True).stdout.strip()
        # 401 is correct for the MCP endpoint (OAuth challenge); 403 is bot
        # protection on the support portal, not a dead link.
        ok = code.startswith("2") or (u == M["mcpServerURL"] and code == "401") or code == "403"
        print(f"    {code}  {u}{'' if ok else '   <-- CHECK'}")
        if not ok:
            bad.append(u)
    if bad:
        print("unreachable URLs:", ", ".join(bad), file=sys.stderr)
        sys.exit(1)
