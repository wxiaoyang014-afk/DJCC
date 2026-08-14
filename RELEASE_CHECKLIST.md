# Release checklist

## Structure

- [ ] Validate `skills/djcc-amazon-keywords` with `quick_validate.py`.
- [ ] Resolve every relative path from a clean clone.
- [ ] Confirm examples are fictional or explicitly redistributable.
- [ ] Confirm scripts never overwrite the input workbook.

## Workflow

- [ ] Verify source path, metadata, worksheets, marketplace, product direction, and at least three sampled records.
- [ ] Preserve each month in its own worksheet.
- [ ] Keep missing search volume and ABA rank blank rather than converting them to zero.
- [ ] Complete negative-root matching and the phase-four summary before product decision cards.
- [ ] Use images only in phase five.
- [ ] Keep product-specific roots and conclusions outside the reusable skill.

## Security and rights

- [ ] Scan the current tree and full Git history for secrets, cookies, accounts, private paths, customer data, and production workbooks.
- [ ] Check hidden worksheets, comments, document properties, external links, queries, pivot caches, macros, and embedded files.
- [ ] Confirm permission to redistribute every dataset, image, template, font, and dependency.
- [ ] Revoke and rotate any credential that was ever committed.

## Minimum acceptance scenarios

1. A normal multi-month workbook retains month-specific metrics and blank values.
2. A misleading filename or stale description triggers source revalidation instead of reusing an old conclusion.
3. A workbook on a path containing spaces or non-ASCII characters is inspected successfully, and malformed input fails clearly.

Release only after all three scenarios pass in a clean Agent environment.

