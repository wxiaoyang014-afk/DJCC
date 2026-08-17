#!/usr/bin/env python3
import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL_NS = {"p": "http://schemas.openxmlformats.org/package/2006/relationships"}

STAGE_REQUIRED = {
    "1-4": ["项目说明", "关键词汇总", "词根词频统计", "第四阶段判定", "否定词根与总结", "产品判定卡"],
    "5": ["模板说明", "关键词图片审核"],
    "6": ["使用说明", "广告-肯定核心", "广告-肯定拓展", "广告-泛词优先测试", "广告-泛词普通测试", "广告-否定词", "Listing词库"],
}

def sheet_map(zf):
    root = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    targets = {node.attrib["Id"]: node.attrib["Target"].lstrip("/") for node in rels.findall("p:Relationship", REL_NS)}
    result = {}
    for node in root.findall("m:sheets/m:sheet", NS):
        rid = node.attrib[f"{{{NS['r']}}}id"]
        target = targets[rid]
        result[node.attrib["name"]] = target if target.startswith("xl/") else f"xl/{target}"
    return result

def shared_strings(zf):
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iterfind(".//m:t", NS)) for si in root.findall("m:si", NS)]

def row_values(zf, sheet_path, row_number, strings):
    root = ET.fromstring(zf.read(sheet_path))
    row = root.find(f"m:sheetData/m:row[@r='{row_number}']", NS)
    if row is None:
        return []
    values = []
    for cell in row.findall("m:c", NS):
        value = cell.find("m:v", NS)
        raw = value.text if value is not None else ""
        if cell.attrib.get("t") == "s" and raw:
            raw = strings[int(raw)]
        elif cell.attrib.get("t") == "inlineStr":
            raw = "".join(t.text or "" for t in cell.iterfind(".//m:t", NS))
        values.append(raw)
    return values

def has_freeze_and_table(zf, sheet_path):
    root = ET.fromstring(zf.read(sheet_path))
    pane = root.find("m:sheetViews/m:sheetView/m:pane", NS)
    tables = root.find("m:tableParts", NS)
    return pane is not None and pane.attrib.get("state") in {"frozen", "frozenSplit"}, tables is not None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--stage", choices=STAGE_REQUIRED, required=True)
    parser.add_argument("--template", action="store_true", help="allow an empty fixed template without embedded Stage 5 images")
    args = parser.parse_args()
    errors = []
    if not args.workbook.is_file():
        errors.append("workbook not found")
    else:
        try:
            with zipfile.ZipFile(args.workbook) as zf:
                names = set(zf.namelist())
                sheets = sheet_map(zf)
                strings = shared_strings(zf)
                for required in STAGE_REQUIRED[args.stage]:
                    if required not in sheets:
                        errors.append(f"missing sheet: {required}")
                if args.stage == "1-4" and not any(name.endswith("月数据") for name in sheets):
                    errors.append("missing YYYY-MM月数据 sheet")
                for sheet_name, sheet_path in sheets.items():
                    frozen, table = has_freeze_and_table(zf, sheet_path)
                    if not frozen:
                        errors.append(f"header rows not frozen: {sheet_name}")
                    if not table:
                        errors.append(f"filter table missing: {sheet_name}")
                joined_strings = "\n".join(strings)
                if "DJCC_TEMPLATE_VERSION" not in joined_strings or "1.0.0" not in joined_strings:
                    errors.append("template version 1.0.0 not found")
                if args.stage == "5" and "关键词图片审核" in sheets:
                    expected = ["关键词", "关键词翻译"] + [f"Top {i}" for i in range(1, 11)] + ["图片匹配状态", "目标形态独立图片数", "同一排除形态独立图片数", "系统初始结论", "系统判定规则", "系统判定依据", "人工最终结论", "人工备注"]
                    actual = row_values(zf, sheets["关键词图片审核"], 2, strings)
                    if actual != expected:
                        errors.append("Stage 5 A-T header contract mismatch")
                if args.stage == "5" and not args.template:
                    has_image_parts = "xl/cellimages.xml" in names or any(n.startswith("xl/media/") for n in names)
                    if not has_image_parts:
                        errors.append("no embedded image parts")
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
            errors.append(f"invalid xlsx: {exc}")
    result = {"path": str(args.workbook.resolve()), "stage": args.stage, "template_mode": args.template, "ok": not errors, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main())
