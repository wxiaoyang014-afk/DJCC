#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/workflow-rules.md",
    "references/workbook-contract.md",
    "scripts/validate_workbook.py",
    "scripts/validate_package.py",
    "assets/templates/DJCC-Stage1-4-Template-v1.0.0.xlsx",
    "assets/templates/DJCC-Stage5-Image-Review-Template-v1.0.0.xlsx",
    "assets/templates/DJCC-Stage6-Ads-Listing-Template-v1.0.0.xlsx",
]

def safe_name(name):
    p = PurePosixPath(name)
    return not p.is_absolute() and ".." not in p.parts and "\\" not in name

def validate_dir(root):
    errors = []
    for rel in REQUIRED:
        path = root / Path(rel)
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {rel}")
    skill = root / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "name: djcc-amazon-keywords" not in text:
            errors.append("invalid SKILL.md frontmatter")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" not in target and not (root / target).exists():
                errors.append(f"broken local link: {target}")
    return errors

def validate_zip(path):
    errors = []
    with zipfile.ZipFile(path) as zf:
        infos = [i for i in zf.infolist() if not i.is_dir()]
        names = [i.filename.rstrip("/") for i in infos]
        if len(names) != len(set(names)):
            errors.append("duplicate ZIP entries")
        if "SKILL.md" not in names:
            errors.append("SKILL.md is not at ZIP root")
        for info, name in zip(infos, names):
            if not safe_name(name):
                errors.append(f"unsafe ZIP path: {name}")
            if info.file_size == 0:
                errors.append(f"empty ZIP entry: {name}")
        for rel in REQUIRED:
            if rel not in names:
                errors.append(f"missing ZIP entry: {rel}")
        if "SKILL.md" in names:
            text = zf.read("SKILL.md").decode("utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" not in target and target not in names:
                    errors.append(f"broken ZIP local link: {target}")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    target = args.target.resolve()
    errors = validate_zip(target) if target.is_file() and target.suffix.lower() == ".zip" else validate_dir(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
    print(json.dumps({"target": str(target), "sha256": digest, "ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main())
