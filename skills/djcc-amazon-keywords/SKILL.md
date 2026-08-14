---
name: djcc-amazon-keywords
description: Build, correct, and verify DJCC-style Amazon keyword-library workbooks. Use when an Agent must validate workbook identity, preserve monthly search-volume and ABA-rank data, review roots and negative roots, complete phase-four product decisions, or perform phase-five image assessment.
---

# DJCC Amazon keyword workflow

## Start with the source gate

1. Ask for the current workbook path, marketplace, and product direction.
2. Run `scripts/inspect_xlsx.py <workbook.xlsx>` when Python is available.
3. Confirm the exact path, size, modification time, file hash, worksheet names, and at least three representative ASIN or keyword rows with their original titles.
4. Stop and reread the exact file whenever those facts conflict with the user's current description. Never trust an older result or a matching filename.

Read [workflow.md](references/workflow.md) before executing the five-stage workflow. Read [schema.md](references/schema.md) when creating or mapping workbook columns.

## Apply the non-negotiable rules

- Keep every month in an independent worksheet.
- Preserve search volume and ABA rank as month-specific values.
- Leave missing values blank; never replace missing data with `0`.
- Include both system suggestions and manual markings in root statistics.
- Define confirmed negative roots as system suggestions not explicitly rejected, plus manually added roots.
- Complete phase-four negative-root matching and its result summary before creating product decision cards.
- Use product images only in phase five.
- Keep marketplace-, product-, customer-, and project-specific roots or conclusions in the project output, not in this reusable skill.

## Verify before delivery

- Re-run the source gate if the input file changed.
- Check at least three representative records end to end.
- Scan all monthly sheets for lost month granularity and missing values converted to zero.
- Confirm phase four is complete before any product decision card.
- Report assumptions, unmatched fields, and unresolved data gaps plainly.

