import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.package import DIRECTORIES, FILES, ROOT, build


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.output = Path(self.temporary.name) / "dist"
        for relative in FILES:
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        for relative in DIRECTORIES:
            shutil.copytree(ROOT / relative, self.root / relative)
        self.version = json.loads((self.root / "plugin.json").read_text())["version"]

    def edit_manifest(self, relative, **changes):
        path = self.root / relative
        manifest = json.loads(path.read_text())
        manifest.update(changes)
        path.write_text(json.dumps(manifest))

    def test_complete_zip_excludes_local_and_development_files(self):
        for relative in (
            "skills/.DS_Store",
            "skills/datahub-search/__pycache__/cached.pyc",
            "evals/results/local.json",
            ".git/config",
            "dist/old.zip",
        ):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("local file")
        archive = build(self.root, self.output, f"v{self.version}")
        self.assertEqual(archive.name, f"datahub-cloud-portable-{self.version}.zip")
        with ZipFile(archive) as package:
            names = package.namelist()
            self.assertIn("datahub-cloud/plugin.json", names)
            self.assertIn("datahub-cloud/mcp.json", names)
            self.assertIn("datahub-cloud/.claude-plugin/plugin.json", names)
            self.assertIn("datahub-cloud/.codex-plugin/plugin.json", names)
            self.assertIn("datahub-cloud/skills/datahub-search/SKILL.md", names)
            self.assertIn("datahub-cloud/.agents/plugins/marketplace.json", names)
            self.assertIn("datahub-cloud/assets/logo-square.svg", names)
            self.assertFalse(
                any(".DS_Store" in name or "__pycache__" in name for name in names)
            )
            self.assertFalse(
                any(name.startswith("datahub-cloud/evals/") for name in names)
            )
            self.assertFalse(
                any(name.startswith("datahub-cloud/.git/") for name in names)
            )
            self.assertFalse(
                any(name.startswith("datahub-cloud/dist/") for name in names)
            )
            self.assertIsNone(package.testzip())
        expected = (
            f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n"
        )
        self.assertEqual(archive.with_suffix(".zip.sha256").read_text(), expected)

    def test_build_is_reproducible_despite_source_timestamps(self):
        first = build(self.root, self.output).read_bytes()
        for path in self.root.rglob("*"):
            if path.is_file():
                os.utime(path, (1700000000, 1700000000))
        second = build(self.root, self.output / "second").read_bytes()
        self.assertEqual(first, second)

    def test_tag_mismatch_does_not_create_release_files(self):
        with self.assertRaisesRegex(ValueError, "Release tag"):
            build(self.root, self.output, "v99.0.0")
        self.assertFalse(self.output.exists())

    def test_client_manifest_version_mismatch(self):
        self.edit_manifest(".claude-plugin/plugin.json", version="99.0.0")
        with self.assertRaisesRegex(ValueError, "must match"):
            build(self.root, self.output)

    def test_prerelease_tag(self):
        for relative in (
            "plugin.json",
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
        ):
            self.edit_manifest(relative, version="1.1.0-rc.1")
        archive = build(self.root, self.output, "v1.1.0-rc.1")
        self.assertEqual(archive.name, "datahub-cloud-portable-1.1.0-rc.1.zip")

    def test_missing_asset(self):
        (self.root / "assets/logo-square.svg").unlink()
        with self.assertRaisesRegex(ValueError, "missing package asset"):
            build(self.root, self.output)

    def test_endpoint_mismatch(self):
        self.edit_manifest(
            ".mcp.json",
            mcpServers={"datahub": {"type": "http", "url": "https://example.com/mcp"}},
        )
        with self.assertRaisesRegex(ValueError, "MCP endpoint differs"):
            build(self.root, self.output)

    def test_missing_skill(self):
        shutil.rmtree(self.root / "skills")
        (self.root / "skills").mkdir()
        with self.assertRaisesRegex(ValueError, "at least one SKILL.md"):
            build(self.root, self.output)

    def test_reference_to_excluded_directory(self):
        (self.root / "evals").mkdir()
        self.edit_manifest(".codex-plugin/plugin.json", skills="./evals")
        with self.assertRaisesRegex(ValueError, "excluded from the package"):
            build(self.root, self.output)

    def test_invalid_versions(self):
        for version in ("../1.0.0", "v1.0.0", "01.0.0", "1.0.0-01", "1.0"):
            with self.subTest(version=version):
                self.edit_manifest("plugin.json", version=version)
                with self.assertRaisesRegex(ValueError, "semantic version"):
                    build(self.root, self.output)

    def test_symlinks_cannot_include_files_outside_plugin(self):
        outside = Path(self.temporary.name) / "private.txt"
        outside.write_text("private file")
        (self.root / "skills/private.txt").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symlinks are not supported"):
            build(self.root, self.output)


if __name__ == "__main__":
    unittest.main()
