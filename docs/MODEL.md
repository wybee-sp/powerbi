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
| Quarter | Q1-Q4, sorted by hidden QuarterNumber |
| QuarterNumber | 1-4; hidden |
| YearQuarter | yyyy-Qn; sorted by hidden YearQuarterSort |
| YearQuarterSort | Year * 10 + QuarterNumber; hidden |
| Month | English full month name; sorted by hidden MonthNumber |
| MonthNumber | 1-12; hidden |
| YearMonth | yyyy-MM; sorted by hidden YearMonthSort |
| YearMonthSort | Year * 100 + MonthNumber; hidden |
| Day | Day of month, 1-31 |
| DayOfWeek | English full name; sorted by hidden DayOfWeekNumber |
| DayOfWeekNumber | Monday=1 through Sunday=7; hidden |
| Week | ISO 8601 week number, `WEEKNUM(Date, 21)` |
| ISOYear | Year containing the week's Thursday; may differ from calendar Year |
| YearWeek | ISO year + -W + two-digit week; sorted by hidden YearWeekSort |
| YearWeekSort | ISOYear * 100 + Week; hidden |

All attributes use `summarizeBy: none`. Names use explicit en-US formatting to match the existing model culture and avoid refresh-machine locale changes. Use YearWeek for cross-year weekly trends; do not pair calendar Year with ISO Week. Example: 2021-01-01 belongs to 2020-W53; 2024-12-30 belongs to 2025-W01. No automatic date hierarchy is created.

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

- Trend category: the shared Time Granularity field parameter, defaulting to `Date[YearMonth]`, with type-aware axis scaling and ascending parameter sort. Each resolved field uses its model sort key. Value remains `_Measures[A8101OP Invoice Count]`, which counts open-item invoice records through the existing header relationship; this is not a newly defined invoice business metric.
- Date range uses `Date[Date]` in Between mode with inclusive start/end inputs. It filters all analytical visuals independently of granularity.
- No zero-filling, blank exclusion, report calculations or automatic hierarchy. Months without activity can remain absent/blank according to existing measure/visual behavior; future calendar dates do not imply future activity.
- Unmatched invoice keys, null dates and `(Blank)` customer categories still require source/model investigation. Adding a calendar cannot repair those records.
- Sales, Purchases and Inventory PBIR are intentionally unchanged. Future migration must replace their date bindings with explicit Date fields; existing Inventory automatic-hierarchy references are not certified by this change.

## Validation and limitations

- Microsoft TOM 19.117.0 deserializes the model and resolves table/column, key, sort, hierarchy, field-parameter and relationship metadata.
- Static checks cover all 11 source-date references, one active Date edge, single-direction cardinalities, unchanged measures, report bindings and absence of ambiguous active Date paths.
- Calendar reference checks cover empty sources, leap days, future extension and ISO year boundaries. These checks do not execute DAX in Analysis Services.
- Refresh with authorized local data is still required to execute the calculated-table DAX, materialize/validate unique continuous dates and check source-date coverage. Desktop rendering of the revised trend remains pending.
- At refresh verify row count equals end minus start plus one, no blank/duplicate Date keys, full-year boundaries, correct sort behavior, monthly totals and invoice-to-payment filter propagation. Review extreme source-date outliers rather than adding arbitrary report filters.

References: [Microsoft date-table guidance](https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables), [ISO week numbering](https://learn.microsoft.com/en-us/dax/weeknum-function-dax), [TMDL serializer](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.tmdlserializer).

## Analytical time grains (shared pattern)

The Date table remains one row per day. Grouping many daily rows into a week/month/quarter/year changes the visual axis, not the stored grain or relationship key. Existing business measures and Date relationships are unchanged.

| Choice | Axis field | Ordering |
| --- | --- | --- |
| Day | Date[Date] | Date ascending |
| Week | Date[YearWeek] | YearWeekSort, ISO year/week |
| Month | Date[YearMonth] | YearMonthSort |
| Quarter | Date[YearQuarter] | YearQuarterSort |
| Year | Date[Year] | Numeric year ascending |

Use year-qualified labels on standalone axes. Month names, quarter labels, week numbers and weekday names alone would combine different periods and are not interchangeable with these grain keys. YearMonth is yyyy-MM, YearQuarter is yyyy-Qn and YearWeek is ISO yyyy-Www.

### Explicit hierarchies

- `Calendar`: Year -> Quarter -> Month -> Date, using the corresponding Date columns.
- `Calendar Week`: Year -> Week -> Date. The level named Year deliberately uses ISOYear, while Week uses ISO week number. Calendar Year would split a single ISO week across two years. Thus 2021-01-01 belongs under Year 2020 / Week 53; 2024-12-30 belongs under Year 2025 / Week 1.
- These are model hierarchies, not automatic date hierarchies. Use them for drill navigation. The single-grain trend uses field-parameter columns instead, so selection replaces one axis rather than expanding several hierarchy levels at once.

### Shared field parameter

`Time Granularity` is a disconnected, five-row calculated field-parameter table in the canonical model. It is a UI selector, not a second Date table, and has no relationships. Its columns are Granularity (visible label), Fields (hidden NAMEOF reference with JSON ParameterMetadata) and Order (hidden 0-4). Granularity sorts by Order and groups by Fields, following native field-parameter metadata. Preserve all three columns and metadata when deploying the shared model.

The Golden Sample binds Category.fieldParameters to `Time Granularity[Fields]`, with ascending sortDirection and a cached initial Month projection. The slicer binds `Time Granularity[Granularity]`, shows Day/Week/Month/Quarter/Year, uses horizontal tiles with strict single selection and saves Month as the initial state. It filters only the trend. Other controls do not filter the parameter selector.

The date-range and granularity selectors are adjacent parts of the combined Time control, placed between Branch and business-specific filters. Their visual grouping does not combine their filtering semantics. The parameter changes grouping only. Date range remains a Between filter on `Date[Date]`, and branch/customer filters still apply. Selecting a partial month or ISO week aggregates only the selected days; grain selection must not silently extend the requested period. Ordinary count/sum measures should reconcile to the same selected-period total across all grains. Do not assume totals are additive for distinct counts, ratios or snapshots.

Power BI treats an unfiltered parameter as all fields. Do not add Select all or a clear action to this control; retain strict single selection. Test host reset/bookmark behavior and explicitly restore Month when resetting the page. A page/report filter permanently forcing Month would prevent switching and must not be added.

### Naming migration

Canonical names now follow the requested contract: QuarterNumber, MonthNumber, YearMonth, YearMonthSort, YearWeek, YearWeekSort, DayOfWeek and DayOfWeekNumber. Prior spaced/hyphenated names were renamed in place with lineage preserved; duplicate aliases were not added. ISOYear, YearQuarter and hidden YearQuarterSort complete the ISO/quarter contract. Existing Golden Sample references and manifests are migrated. External consumers using previous names must update before deployment. Module reports were not modified.

### Validation before release

Static validation verifies native TOM hierarchy/parameter metadata, all five NAMEOF targets and sort mappings, PBIR parameter references, default Month selection and interaction isolation. Reference cases cover ISO New Year boundaries and grouping the same date selection at all five grains. Actual DAX evaluation and field-parameter switching require Desktop/model refresh: test all five choices, chronological order, unchanged date-range inputs/KPI totals, partial periods, empty periods and bookmarks. No successful runtime interaction test is claimed yet.

Reference: [Microsoft field parameters](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters).

### TimeControl axis presentation

The shared parameter already implements all five canonical axis mappings above; no extra tables, measures or relationship changes are needed for TimeControl finalization. Golden Sample uses one line chart requesting continuous scaling for date/numeric fields and categorical fallback for text fields with parameter sortDirection Ascending and the selected column sort metadata. The initial YearMonth projection is the saved Month state. Readability settings are shared across grains; native label collision handling and chart scrolling preserve the selected data grain. See DESIGN_SYSTEM.md for the runtime acceptance checks.

The 1.4.0 correction removes the forced categorical axis and minimum category width. Date[Date] is verified as dateTime with date-only annotation and yyyy-MM-dd format. The field parameter itself, all sort keys and business measures are unchanged. All five runtime states remain pending as recorded in GOLDEN_SAMPLE.md.

## Date validity investigation

The current TimeControl rendering is accepted by the user as the visual standard; its layout is frozen. The reported 01.01.0106 lower bound remains an open data/model investigation. See [DATE_VALIDITY.md](DATE_VALIDITY.md) for confirmed parser risks, the source-field mapping, a read-only row diagnostic and a proposed validity policy. Responsible source rows cannot be identified until the local CSV exports are available. No transformation or calendar-bound change has been made.

## Localization

Native en-US/de-DE/ro-RO culture captions and selected descriptions preserve all model identifiers and business definitions. Hidden _ReportLabels contains presentation-only USERCULTURE measures. Time Granularity has five static rows per locale and a hidden Locale column; the embed host selects exactly one locale, with English default. Numeric Order preserves the chosen grain independently of language and date range. No relationships or business measures change. See LOCALIZATION.md and Templates/Localization for catalogues, fallback rules and unsupported report-text categories. This supersedes the earlier five-row parameter description: there are now 15 rows, with exactly five visible per host locale.


### Localized visual captions

The hidden disconnected `_VisualCaptions` table is presentation metadata for the Golden Sample, not a new business dimension. It maps stable Order values to the existing customer column and four `_Measures` count measures. Each field has en-US/de-DE/ro-RO captions generated from the canonical metadata catalogue. A hidden host-controlled Locale filter resolves one caption per field. No relationships, source transformations or business measure expressions change. See `docs/LOCALIZATION.md` for bindings and the matching embed locale contract. Keep technical names and lineage stable; never copy business expressions into translated wrapper measures merely to obtain a caption.
