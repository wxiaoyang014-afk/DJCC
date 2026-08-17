# DJCC workflow rules

## Contents

1. Source identity and product boundary
2. Stages 1-3
3. Stage 4
4. Product card and Stage 5
5. Stage 6
6. Validation and prohibited failures

## 1. Source identity and product boundary

Before adopting an input, record its absolute path, file name, byte size, modified time, SHA-256, Sheet names, required headers, marketplace, language, product direction, and at least three representative keywords or ASINs with original titles when present. If the file changes or conflicts with the user's description, invalidate old caches and reread the exact path.

Read the uploaded competitor workbook itself. Extract ASIN, link, original title, bullets, form, functions, power method, use areas, same/different-form signals, and available images. Enrich exact ASINs from Amazon, then SellerSprite, then Xiyou, then another user-approved authoritative source. Record evidence sources and flag conflicts. External lookup enriches the uploaded snapshot; it does not replace it.

Early competitor images may be inspected only to draft a provisional product boundary. Do not use that provisional boundary to classify keywords before Stage 4 and the product card are complete.

## 2. Stages 1-3

### Monthly and summary data

Create one `YYYY-MM月数据` Sheet per source month. Preserve each month's search volume and ABA rank separately. Missing means blank; numeric zero means an observed zero. Create `关键词汇总` from normalized exact keyword identity.

Normalize keyword identity by Unicode normalization, case folding where the marketplace language allows it, trimming outer whitespace, and collapsing repeated spaces. Preserve original keyword text. Do not merge tokens across punctuation, hyphens, brands, singular/plural forms, or spelling variants unless a reviewed project rule explicitly allows it.

### Root statistics and review

Create `词根词频统计` with coverage totals, coverage rate, monthly coverage, representative keywords, system suggestion, reason, and human review fields.

Use these explicit human actions:

- blank: no human decision;
- `新增否定`: add a root not selected by the system;
- `确认否定`: confirm the system suggestion;
- `移除否定`: explicitly reject/remove the system suggestion;
- `待复核`: exclude this root from automatic negative-root decisions until a human resolves it.

Confirmed negative roots equal: system suggestions whose human action is blank or `确认否定`, plus non-system roots marked `新增否定`, minus `移除否定`; any `待复核` root is excluded. `确认否定` is legal only for a system suggestion, and `新增否定` only for a non-system root. Mark illegal combinations `状态冲突，待人工核对` and pause that root. Match complete normalized tokens only, never raw substrings. Preserve each root's source and reason.

## 3. Stage 4

Base `第四阶段判定` on `关键词汇总`. Preserve all monthly values. Record the active threshold and zero-value policy in `项目说明` before applying rules.

Use mutually exclusive first-match ordering for any number of months:

1. `R1 否定词根`: confirmed negative-root hit.
2. `R2 搜索量全无效`: every configured month has blank search volume, or zero when the accepted project zero policy treats observed zero as unavailable.
3. `R3 低搜索量`: at least one available monthly search volume is below the accepted project threshold.
4. `R4 ABA全缺失`: every configured month's ABA rank is blank.
5. `R5 无效关键词`: keyword is empty after normalization, contains only punctuation/symbols, is a broken encoding fragment, or is otherwise demonstrably non-linguistic. Product irrelevance alone does not qualify as malformed.
6. `R6 保留`: none of R1-R5 matched.

Do not silently assume the historical threshold of 1,000. If the user has not accepted a threshold or zero policy, pause Stage 4 rather than guessing.

For every row show matched roots, root source, root reason, conclusion, rule code, and concrete evidence. `否定词根与总结` must count rows by the first matched rule so counts are mutually exclusive and reconcile to the total.

## 4. Product card and Stage 5

Create and confirm `产品判定卡` after Stage 4. A URL or ASIN is a pointer, not completed product content. Complete target form, core requirements, allowed boundaries, excluded forms, same-class evidence, different-class evidence, and source status. If lookup routes fail, keep the boundary unconfirmed and route ambiguous image cases to human review.

Adopt only Stage 4 retained keywords. Match keywords by normalized exact identity, never row position or substring. Use the source image workbook as the base and preserve Top1-Top10 cell images, formulas, relationships, media, styles, and editable conclusions.

Use this first-match Stage 5 ordering:

1. `I2 肯定`: at least four independent usable Top10 products clearly match the confirmed target form -> `肯定词库`.
2. `I3 否定`: keyword meaning and at least three independent usable images point to one same excluded form, while I2 is not met -> `否定词库`.
3. `I4 泛词`: available images span multiple relevant forms and the keyword is broad but commercially usable -> `泛词`.
4. `I1 缺图`: zero usable images, or the remaining usable evidence cannot execute I2-I4 -> `待人工复核`.
5. `I5 待复核`: mixed, weak, duplicate-dominated, or boundary-dependent evidence -> `待人工复核`.

Count variants of the same parent/product once when identity evidence allows. Never combine different excluded forms to reach I3. Missing images never auto-reject a keyword.

Keep separate columns for `系统初始结论` and `人工最终结论`. The human column uses the dropdown `肯定词库,泛词,待人工复核,否定词库`; do not overwrite the system conclusion.

After review, de-duplicate normalized keywords and compare with the full Stage 4 retained set. Build downstream libraries only from explicit human final conclusions. Report uncovered retained keywords as coverage gaps unless the user explicitly requests confirmed-only output.

## 5. Stage 6

Use only explicit Stage 5 final conclusions. Preserve monthly search volume and ABA rank.

Create:

- `使用说明` for accepted tier thresholds and configuration;
- `广告-肯定核心` and `广告-肯定拓展` from confirmed positives;
- `广告-泛词优先测试` and `广告-泛词普通测试` from confirmed generic terms;
- `广告-否定词` from confirmed negatives;
- `Listing词库` from confirmed positives only unless generic terms are explicitly approved.

Record every tier rule in `使用说明`, including whether an ABA threshold uses `任一月达标` or `所有月达标`. Do not invent a default ABA or search-volume boundary. Verify core + expansion equals confirmed positives, priority + regular equals confirmed generic terms, and advertising negatives equal confirmed negatives. The union of those three groups must equal confirmed positive + generic + negative keywords. Count `待人工复核` separately as a coverage gap; it enters no Stage 6 bucket.

## 6. Validation and prohibited failures

Check exact input identity, fixed Sheet/column contracts, blank-versus-zero preservation, duplicate normalized keywords, formula errors, threshold configuration, mutually exclusive counts, image relationships/media, header visibility, data validation, and all reconciliation totals. Spot-check at least three records end to end and visually inspect every visible Sheet.

Never reuse another project's marketplace, product card, visual seeds, roots, thresholds, or conclusions. Never clear and reconstruct a reviewed Sheet to append annotations. Never deliver an image-review workbook without the source images when an image workbook was supplied.
