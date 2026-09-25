"""Build portable source and skill-upload ZIPs from this repository."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MANIFEST = json.loads((ROOT / "plugin.json").read_text())
NAME = MANIFEST["name"]
VERSION = MANIFEST["version"]
SKILLS = sorted((ROOT / "skills").glob("*/SKILL.md"))

if not SKILLS:
    raise SystemExit("No skills found under skills/<name>/SKILL.md")

files = [ROOT / "plugin.json", ROOT / "mcp.json", ROOT / "README.md"]
files.extend(path for path in (ROOT / "skills").rglob("*") if path.is_file())
DIST.mkdir(exist_ok=True)

portable_zip = DIST / f"{NAME}-portable-{VERSION}.zip"
with ZipFile(portable_zip, "w", ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, f"{NAME}/{path.relative_to(ROOT)}")

skills_zip = DIST / f"{NAME}-skills-{VERSION}.zip"
with ZipFile(skills_zip, "w", ZIP_DEFLATED) as archive:
    for path in files:
        if path.is_relative_to(ROOT / "skills"):
            archive.write(path, path.relative_to(ROOT))

print(portable_zip)
print(skills_zip)
