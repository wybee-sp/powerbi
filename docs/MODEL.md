# TopEvo shared semantic model

Canonical source: `Templates/TopEvoAnalytics.SemanticModel`. All module reports and the internal Golden Sample share this model. No report-specific or duplicated role-playing Date tables are allowed at this stage.

## Canonical Date dimension

`Date` is an imported DAX calculated table, evaluated on model refresh. Calendar construction is reusable model logic; no report-level calculation or business measure was added.

- One row per calendar day, produced by `CALENDAR` with full-year boundaries.
- Start: January 1 of the earlier of the earliest nonblank source date's year and the refresh date's year.
- End: December 31 of the year after the later of the latest nonblank source date and refresh date, capped at supported year 9999.
- Empty/all-null sources: January 1 of the current year through December 31 of next year. `TODAY()` is evaluated during refresh, not on report interaction.
- Bounds explicitly include all 11 typed calendar-date fields listed below. Future facts must extend this registry when introduced; no reliance on CALENDARAUTO or hidden date tables.
- Time-only `Erfassungseit HH:MM:SS [113]` fields and raw unparsed text fields are excluded. Existing date fields are produced as date values by Power Query. New timestamp sources must normalize to dates before relating to the daily key.
- Blank source values do not set the bounds. No filter removes blank fact dates or customer categories. Implausible but valid dates expand the calendar and must be corrected upstream rather than silently clipped.

TMDL marks the table with `dataCategory: Time` and `Date[Date]` with `isKey`, dateTime storage and `UnderlyingDateTimeDataType = Date`. This is classic marked-date-table metadata; no preview calendar feature or compatibility-level upgrade is needed. The model retains `__PBI_TimeIntelligenceEnabled = 0`.

## Calendar fields

| Field | Meaning / order |
| --- | --- |
| Date | Unique daily key at midnight; yyyy-MM-dd |
| Year | Calendar year |
| Quarter | Q1-Q4, sorted by hidden Quarter Number |
| Quarter Number | 1-4; hidden |
| Month | English full month name; sorted by hidden Month Number |
| Month Number | 1-12; hidden |
| Year-Month | yyyy-MM; sorted by hidden Year-Month Sort |
| Year-Month Sort | Year * 100 + Month Number; hidden |
| Day | Day of month, 1-31 |
| Day of Week | English full name; sorted by hidden Day of Week Number |
| Day of Week Number | Monday=1 through Sunday=7; hidden |
| Week | ISO 8601 week number, `WEEKNUM(Date, 21)` |
| ISO Year | Year containing the week's Thursday; may differ from calendar Year |
| Year-Week | ISO year + -W + two-digit week; sorted by hidden Year-Week Sort |
| Year-Week Sort | ISO Year * 100 + Week; hidden |

All attributes use `summarizeBy: none`. Names use explicit en-US formatting to match the existing model culture and avoid refresh-machine locale changes. Use Year-Week for cross-year weekly trends; do not pair calendar Year with ISO Week. Example: 2021-01-01 belongs to 2020-W53; 2024-12-30 belongs to 2025-W01. No automatic date hierarchy is created.

## Relationships and date roles

Every new date relationship is many-to-one in TMDL (`fromColumn` = fact date, `toColumn` = Date.Date), with single-direction filtering from Date to fact.

| Fact date (also included in calendar bounds) | State | Intended role |
| --- | --- | --- |
| a42001.InvoiceDate | Active | Default invoicing calendar |
| a42001.OrderDate | Inactive | Order-date analysis |
| a42001.ServiceDate | Inactive | Service-date analysis |
| a8101op_invoices.InvoiceDate | Inactive | Direct open-item invoice-date analysis |
| a8101op_invoices.DueDate | Inactive | Due-date analysis |
| a8101op_invoices.EntryDate | Inactive | Open-item entry-date analysis |
| a8101op_invoices.ValueDate | Inactive | Value date on invoice records, if business meaning is confirmed |
| a8101op_payments.InvoiceDate | Inactive | Invoice date recorded on payment records |
| a8101op_payments.DueDate | Inactive | Due date recorded on payment records, subject to business validation |
| a8101op_payments.EntryDate | Inactive | Payment-entry date |
| a8101op_payments.ValueDate | Inactive | Payment value date |

Default propagation is:

`Date -> a42001 -> a8101op_invoices -> a8101op_payments`

`a42001` also filters invoice lines. Existing customer and branch paths remain unchanged. Only the first Date relationship is active, so no parallel active Date-to-open-item or Date-to-payment path is introduced.

### Alternate roles

Inactive relationships do not change existing measures automatically. Future role-specific measures belong in `_Measures` and require a separately explained business definition before implementation. Use `USERELATIONSHIP` for the chosen role. For a direct open-item/payment role, explicitly disable the default `Date[Date]` to `a42001[InvoiceDate]` edge with `CROSSFILTER(..., NONE)` in the same calculation, so invoice-date filtering does not also reach that fact through the header chain. Retain customer/branch filtering and verify expected totals and unmatched records. For alternate a42001 dates, also make the intended default-edge suppression explicit and test it.

No such measure is added now. Existing payment measures continue to describe payments associated with selected invoice-header dates, not payments occurring in the selected value-date period. Inactive relationships do not supply alternative RLS propagation; tenant security remains separately validated. One shared Date table does not provide independent simultaneous invoice-date and payment-date slicers.

## Golden Sample

- Trend category: `Date[Year-Month]`, categorical axis, ascending category sort backed by Year-Month Sort. Value remains `_Measures[A8101OP Invoice Count]`, which counts open-item invoice records through the existing header relationship; this is not a newly defined invoice business metric.
- Existing invoice-date slicer now uses `Date[Date]`. Its selection mode and interactions remain unchanged.
- No zero-filling, blank exclusion, report calculations or automatic hierarchy. Months without activity can remain absent/blank according to existing measure/visual behavior; future calendar dates do not imply future activity.
- Unmatched invoice keys, null dates and `(Blank)` customer categories still require source/model investigation. Adding a calendar cannot repair those records.
- Sales, Purchases and Inventory PBIR are intentionally unchanged. Future migration must replace their date bindings with explicit Date fields; existing Inventory automatic-hierarchy references are not certified by this change.

## Validation and limitations

- Microsoft TOM 19.117.0 deserializes the model and resolves table/column, key, sort and relationship metadata.
- Static checks cover all 11 source-date references, one active Date edge, single-direction cardinalities, unchanged measures, report bindings and absence of ambiguous active Date paths.
- Calendar reference checks cover empty sources, leap days, future extension and ISO year boundaries. These checks do not execute DAX in Analysis Services.
- Refresh with authorized local data is still required to execute the calculated-table DAX, materialize/validate unique continuous dates and check source-date coverage. Desktop rendering of the revised trend remains pending.
- At refresh verify row count equals end minus start plus one, no blank/duplicate Date keys, full-year boundaries, correct sort behavior, monthly totals and invoice-to-payment filter propagation. Review extreme source-date outliers rather than adding arbitrary report filters.

References: [Microsoft date-table guidance](https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables), [ISO week numbering](https://learn.microsoft.com/en-us/dax/weeknum-function-dax), [TMDL serializer](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.tmdlserializer).
