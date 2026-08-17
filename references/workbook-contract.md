# Fixed workbook contract — template version 1.0.0

Use the supplied templates. Dynamic month columns repeat once per configured month in chronological order.

## Common visual standard

- Font: Calibri or a compatible sans-serif.
- Title row: dark blue fill, white bold text, 16 pt, height 30.
- Header row: medium blue fill, white bold text, wrapped, height 30.
- Editable human cells: pale yellow fill.
- System result cells: pale blue fill.
- Exception/review cells: pale orange fill.
- Hide gridlines, freeze rows through the header, enable filters on populated tables, and keep identifiers as text.
- Counts use `#,##0`; coverage uses `0.0%`; dates use `yyyy-mm-dd`; missing values remain blank.

## Template A: `DJCC-Stage1-4-Template-v1.0.0.xlsx`

Required Sheets in order:

1. `项目说明`
2. `YYYY-MM月数据` repeated per month
3. `关键词汇总`
4. `词根词频统计`
5. `第四阶段判定`
6. `否定词根与总结`
7. `产品判定卡`

Fixed columns:

- Month Sheet: `关键词,关键词翻译,月搜索量,ABA周排名,数据来源`
- `关键词汇总`: `关键词,关键词翻译`, then `YYYY-MM月搜索量,YYYY-MM ABA周排名` pairs, then `数据来源`
- `词根词频统计`: `词根,中文翻译,覆盖关键词数,关键词覆盖率`, monthly coverage columns, `代表关键词,建议否定标记,建议否定原因,人工审核动作,人工备注,确认来源,审核状态`
- `第四阶段判定`: summary columns, then `命中确认否定词根,词根判定来源,词根说明,第四阶段结论,判定规则代码,判定依据`
- `否定词根与总结`: `统计类型,统计项目,数量,说明`
- `产品判定卡`: `字段,内容,证据来源,确认状态`

## Template B: `DJCC-Stage5-Image-Review-Template-v1.0.0.xlsx`

Required Sheets are `模板说明,关键词图片审核`. `模板说明` stores `DJCC_TEMPLATE_VERSION=1.0.0`. Sheet `关键词图片审核` uses exactly columns A-T:

`关键词,关键词翻译,Top 1,Top 2,Top 3,Top 4,Top 5,Top 6,Top 7,Top 8,Top 9,Top 10,图片匹配状态,目标形态独立图片数,同一排除形态独立图片数,系统初始结论,系统判定规则,系统判定依据,人工最终结论,人工备注`

Columns C-L are reserved for source images/formulas. Column S is editable and has the four-value conclusion dropdown. Keep all other system columns auditable.

## Template C: `DJCC-Stage6-Ads-Listing-Template-v1.0.0.xlsx`

Required Sheets:

`使用说明,广告-肯定核心,广告-肯定拓展,广告-泛词优先测试,广告-泛词普通测试,广告-否定词,Listing词库`

Every keyword tier Sheet uses the following exact expansion: `关键词,关键词翻译`, then repeat `YYYY-MM月搜索量,YYYY-MM ABA周排名` in chronological order for every configured month, then `最终词库结论,分层结果,分层规则,数据来源,人工备注`.

## Version rule

Write `DJCC_TEMPLATE_VERSION=1.0.0` in `项目说明`, `模板说明`, or `使用说明` according to the template. Never silently migrate an older workbook. Preserve unknown user columns and report them before mapping into a newer template.
