# Portable workbook schema

Use these logical fields when mapping source workbooks. Column names may differ by source.

| Field | Type | Required | Rule |
|---|---|---:|---|
| marketplace | text | yes | Use the explicit marketplace code or name. |
| month | text/date | yes for metrics | Keep one month per worksheet. |
| asin | text | no | Preserve as an identifier, including leading zeros if present. |
| keyword | text | yes | Retain the original text alongside any normalized form. |
| original_title | text | yes for sampled products | Do not replace it with a generated title. |
| search_volume | number/blank | no | Blank means missing; zero means observed zero. |
| aba_rank | number/blank | no | Preserve monthly granularity. |
| root | text | no | Keep its source and review status. |
| root_source | enum | no | `system` or `manual`. |
| root_status | enum | no | `suggested`, `accepted`, or `rejected`. |
| matched_negative_roots | text/list | no | Populate during phase four. |
| decision | enum | no | `keep`, `exclude`, or `review`. |
| decision_reason | text | no | Use concise evidence, not unsupported inference. |

Do not add customer-specific identifiers, private commercial metrics, or product-specific root lists to the reusable schema.

