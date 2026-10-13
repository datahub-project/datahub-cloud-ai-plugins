"""Build a reproducible portable plugin ZIP using only the Python standard library."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json")
FILES = (
    *MANIFESTS,
    "mcp.json",
    ".mcp.json",
    ".agents/plugins/marketplace.json",
    "README.md",
    "assets-NOTICE.md",
)
DIRECTORIES = ("skills", "assets")
VERSION_PATTERN = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*)?",
    re.ASCII,
)


def read_json(root: Path, relative: str) -> dict:
    value = json.loads((root / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative} must contain a JSON object")
    return value


def package_files(root: Path) -> list[Path]:
    paths = [root / relative for relative in FILES]
    for relative in DIRECTORIES:
        directory = root / relative
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError(f"Missing or symlinked package directory: {relative}")
        for path in directory.rglob("*"):
            if path.name == ".DS_Store" or "__pycache__" in path.parts:
                continue
            if path.is_symlink():
                raise ValueError(
                    f"Symlinks are not supported: {path.relative_to(root)}"
                )
            if path.is_file():
                paths.append(path)
    for path in paths:
        if path.is_symlink() or not path.is_file():
            raise ValueError(
                f"Missing or symlinked package file: {path.relative_to(root)}"
            )
    return sorted(paths)


def validate(root: Path, paths: list[Path], tag: str | None) -> tuple[str, str]:
    manifests = [read_json(root, relative) for relative in MANIFESTS]
    name = manifests[0].get("name", "")
    version = manifests[0].get("version", "")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(
            "Plugin name must contain lowercase words separated by hyphens"
        )
    if not isinstance(version, str) or not VERSION_PATTERN.fullmatch(version):
        raise ValueError("Plugin version must be a semantic version")
    for relative, manifest in zip(MANIFESTS, manifests):
        if manifest.get("name") != name or manifest.get("version") != version:
            raise ValueError(
                f"{relative} must match the portable manifest name and version"
            )
    if tag is not None and tag != f"v{version}":
        raise ValueError(f"Release tag {tag!r} must match plugin version v{version}")

    marketplace = read_json(root, ".agents/plugins/marketplace.json")
    if not any(plugin.get("name") == name for plugin in marketplace["plugins"]):
        raise ValueError("The local marketplace must include the portable plugin")

    portable_mcp = read_json(root, "mcp.json")["mcpServers"]
    legacy_mcp = read_json(root, ".mcp.json")["mcpServers"]
    if not portable_mcp or portable_mcp.keys() != legacy_mcp.keys():
        raise ValueError(
            "Portable and client MCP configurations must name the same servers"
        )
    for server, config in portable_mcp.items():
        if config.get("type") != "streamable-http" or not config.get(
            "url", ""
        ).startswith("https://"):
            raise ValueError(
                f"Portable MCP server {server} must use streamable-http and HTTPS"
            )
        if legacy_mcp[server].get("url") != config["url"]:
            raise ValueError(
                f"MCP endpoint differs between configurations for {server}"
            )

    included = {path.relative_to(root).as_posix() for path in paths}
    if not any(path.match("skills/*/SKILL.md") for path in paths):
        raise ValueError("The package must contain at least one SKILL.md")
    codex = manifests[2]
    for field in ("skills", "mcpServers"):
        relative = codex[field]
        if not relative.startswith("./") or not (root / relative).exists():
            raise ValueError(
                f"Codex {field} references a missing package path: {relative}"
            )
        if not (root / relative).resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Codex {field} references a path outside the plugin")
        packaged_path = (root / relative).relative_to(root).as_posix()
        if packaged_path not in included and not any(
            item.startswith(f"{packaged_path}/") for item in included
        ):
            raise ValueError(
                f"Codex {field} references a path excluded from the package"
            )
    interface = (
        manifests[0].get("extensions", {}).get("com.openai", {}).get("interface", {})
    )
    for field in ("composerIcon", "logo"):
        if field in interface and interface[field].removeprefix("./") not in included:
            raise ValueError(f"Portable {field} references a missing package asset")
    return name, version


def build(root: Path, output: Path, tag: str | None = None) -> Path:
    paths = package_files(root)
    name, version = validate(root, paths, tag)
    output.mkdir(parents=True, exist_ok=True)
    archive_path = output / f"{name}-portable-{version}.zip"
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for path in paths:
            entry = ZipInfo(
                f"{name}/{path.relative_to(root).as_posix()}", (1980, 1, 1, 0, 0, 0)
            )
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = ZIP_DEFLATED
            archive.writestr(entry, path.read_bytes())
    with ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    archive_path.with_suffix(".zip.sha256").write_text(
        f"{digest}  {archive_path.name}\n", encoding="utf-8"
    )
    return archive_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument(
        "--tag", help="Require a release tag matching the manifest version"
    )
    args = parser.parse_args()
    try:
        archive = build(ROOT, args.output, args.tag)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
    print(archive)
    print(archive.with_suffix(".zip.sha256"))


if __name__ == "__main__":
    main()
