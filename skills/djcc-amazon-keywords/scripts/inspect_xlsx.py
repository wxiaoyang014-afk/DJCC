#!/usr/bin/env python3
"""Inspect XLSX identity without third-party dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
DOC_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def shared_strings(archive: ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(node.itertext()) for node in root.findall("m:si", NS)]


def workbook_sheets(archive: ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("r:Relationship", REL_NS)}
    result = []
    for sheet in workbook.findall("m:sheets/m:sheet", NS):
        rel_id = sheet.attrib[f"{{{DOC_REL}}}id"]
        target = targets[rel_id].replace("\\", "/").lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        result.append((sheet.attrib["name"], target))
    return result


def cell_value(cell: ET.Element, strings: list[str]) -> str:
    value = cell.find("m:v", NS)
    if value is None:
        inline = cell.find("m:is", NS)
        return "" if inline is None else "".join(inline.itertext())
    raw = value.text or ""
    if cell.attrib.get("t") == "s" and raw.isdigit():
        index = int(raw)
        return strings[index] if index < len(strings) else raw
    return raw


def sample_rows(archive: ZipFile, target: str, strings: list[str], limit: int) -> list[list[str]]:
    root = ET.fromstring(archive.read(target))
    rows = []
    for row in root.findall("m:sheetData/m:row", NS):
        values = [cell_value(cell, strings) for cell in row.findall("m:c", NS)]
        if any(values):
            rows.append(values)
        if len(rows) >= limit:
            break
    return rows


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--rows", type=int, default=4, help="non-empty rows sampled per sheet")
    args = parser.parse_args()
    path = args.workbook.expanduser().resolve()
    if not path.is_file():
        parser.error(f"file not found: {path}")

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    stat = path.stat()
    try:
        with ZipFile(path) as archive:
            strings = shared_strings(archive)
            sheets = workbook_sheets(archive)
            samples = {name: sample_rows(archive, target, strings, args.rows) for name, target in sheets}
    except (BadZipFile, KeyError, ET.ParseError) as exc:
        parser.error(f"invalid or unsupported XLSX: {exc}")

    report = {
        "path": str(path),
        "size_bytes": stat.st_size,
        "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "sha256": digest,
        "sheets": [name for name, _ in sheets],
        "sample_rows": samples,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
