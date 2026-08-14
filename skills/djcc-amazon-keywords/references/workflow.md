# Five-stage workflow

## Stage 1: Source identity

- Record the absolute source path, byte size, modified time, SHA-256 hash, worksheet names, marketplace, and product direction.
- Sample at least three ASIN or keyword rows and retain their original titles.
- Resolve any identity conflict before analysis.

## Stage 2: Normalize monthly data

- Map source columns without silently discarding unknown fields.
- Store each reporting month in a separate worksheet.
- Keep search volume and ABA rank tied to their source month.
- Represent missing values as blank cells, not numeric zero.

## Stage 3: Build root statistics

- Normalize case and surrounding whitespace while retaining the original keyword.
- Count both system-suggested and manually marked roots.
- Preserve the source and review status of each root.
- Keep project-specific roots in the project workbook only.

## Stage 4: Decide relevance

- Form confirmed negative roots from system suggestions not explicitly rejected, plus manual additions.
- Match confirmed negative roots directly against candidate keywords.
- Append matched negative roots, the decision result, and a concise reason.
- Finish the result summary and review exceptions before creating product decision cards.

## Stage 5: Assess images

- Use product images only after textual and keyword decisions are complete.
- Record image evidence separately from text evidence.
- Do not let image similarity overwrite verified marketplace or source identity.

## Delivery checks

- Reconcile row counts between source, normalized data, decisions, and summary.
- Spot-check three representative records across all stages.
- List unresolved inputs and manual-review items.

