---
name: djcc-amazon-keywords
description: Build, clean, audit, and advance DJCC-style Amazon keyword-library workbooks across stages 1-6. Use for source identity checks, monthly keyword normalization, root review, fourth-stage filtering, product decision cards, Top10 image review, and advertising or Listing keyword tiers.
---

# DJCC Amazon keyword library

Execute the workflow in auditable stages. Preserve source evidence, monthly granularity, human decisions, workbook structure, and embedded images.

## Required reading

Before any workbook work, read:

1. [workflow-rules.md](references/workflow-rules.md) for decision logic and stage gates.
2. [workbook-contract.md](references/workbook-contract.md) for fixed Sheet names, columns, editable fields, styles, and template versions.

Use the matching workbook under `assets/templates/` as the output base for Stages 1-4 and 6. For Stage 5, use the supplied template only as the column/style contract; the physical output base must be the user's image-bearing workbook so embedded images and relationships are preserved.

## Non-negotiable sequence

1. Pass the source identity gate.
2. Build monthly Sheets, `关键词汇总`, and `词根词频统计`.
3. Pause for human root review and preserve the returned workbook exactly.
4. Apply the mutually exclusive Stage 4 rules and create `否定词根与总结`.
5. Complete and confirm `产品判定卡`.
6. Use images only for Stage 5 classification.
7. Build Stage 6 only from explicitly reviewed Stage 5 conclusions.

Never skip a stage gate, convert missing values to zero, collapse monthly metrics into best/highest values, treat blank human cells as rejection, use raw substring root matching, or carry product-specific decisions into the reusable skill.

## Cross-platform behavior

- If Python or workbook tooling is unavailable, continue with readable files and manual checks; report every unavailable validation. Do not claim validation passed.
- If Amazon or a product-data connector is unavailable, use the uploaded competitor workbook as the durable fallback and mark product boundaries unconfirmed where evidence is insufficient.
- If embedded-image preservation cannot be verified, do not overwrite the source image workbook. Produce no result-only substitute unless the user requests it.

## Delivery gate

Run `scripts/validate_workbook.py <workbook.xlsx> --stage <1-4|5|6>` when Python is available. Also visually inspect every visible Sheet and reconcile source, retained, removed, reviewed, and tier totals. Report unresolved inputs plainly.
