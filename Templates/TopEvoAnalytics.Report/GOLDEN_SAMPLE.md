# TopEvo Golden Sample

Permanent internal visual reference. Do not deploy this report to customers.

## Implementation

Overview uses the canonical TopEvo 1.0.0 theme and compact 1.4.1 component specification with unchanged 1.4.0 layout on the 1280 x 720 grid. Theme resource `StaticResources/RegisteredResources/TopEvo-1.0.0.json` is a synchronized copy; edit only the canonical source and then synchronize it.

`COMPONENTS.json` records the thirteen visual IDs (twelve retained, one new granularity selector), slots, geometry and existing model bindings. It is external authoring metadata, not a Power BI definition. TimeControl is the user-accepted rendered visual reference; other components retain their individual status. Existing report identity and shared-model reference are preserved.

The page contains one page-title text box, a native page navigator, one date-range slicer, two dimension dropdowns and a horizontal granularity tile selector, four count cards, an invoice-date trend, a customer ranking and a summary table. The navigator currently exposes the single Overview page; there are no placeholder destinations.

## Data and interaction contract

- KPIs: existing `_Measures` invoice count, open invoice count, closed invoice count and payment count. No calculations were created.
- Trend: shared Time Granularity field parameter, default Month (`Date[YearMonth]`), ascending chronological sorting, unchanged `_Measures[A8101OP Invoice Count]`. One visual switches between all five grains.
- Ranking: customer search name and invoice count, descending. Shows all available customer categories with native scrolling; no unsupported Top N filter was invented. Equal search names group together according to the existing model.
- Summary: customer search name and the four KPI measures; fixed column widths and business-facing captions.
- Primary groups: Branch -> Time control -> Customer. Keyboard order: Branch -> Date range -> granularity -> Customer. The Time control is one continuous 608 x 56 px white surface at x=336, y=72: date inputs use 280 px, immediately followed by 328 px of horizontal Day/Week/Month/Quarter/Year tiles. Customer moves to x=960. Component grouping is recorded in COMPONENTS.json; PBIR keeps two native slicers with independent behavior.
- Filters: Date range uses Date[Date] in Between mode with no saved bounds; Branch and Customer retain multi-select dropdowns. Display by is a separate strict single-select field parameter, default Month.
- Each data filter targets all seven analytical visuals; Display by targets only the trend. Slicers do not filter each other. Chart/table selections do not change KPIs or other visuals, keeping the reference page stable for component comparison.
- Payment counts refer to payments associated with the selected invoices through existing relationships; the period filter is invoice date, not payment date. Existing unmatched keys and relationship behavior still need data-level verification.

## Deliberate limits

- No comparison deltas, targets, refresh timestamp or currency amounts: suitable existing measures are absent or unnecessary for this count-based sample.
- No reset bookmark or drillthrough destination was fabricated. Use slicer clear controls; a future approved navigation/reset component can extend the sample.
- Theme integration was implemented directly in PBIR as requested. The user reported the first Desktop rendering; the compact revision has not been rendered by the agent.
- Report/page definitions pass their published schemas. The repository's visual-container 2.12.0 schema URL returns 404; visual structures were checked against published 2.9.0 using an in-memory schema-declaration substitution only. Files retain 2.12.0. This is a compatibility check, not full 2.12 certification.
- Theme parity, model field/measure existence, unique visual IDs, bounds, non-overlap and interaction references are statically checked. Actual rendering, data refresh, tab/focus behavior and embedded readability remain unverified.
- Desktop build: not yet recorded. Native desktop automation is unavailable in this session. Review the report in Desktop before approving components for future page generation.
- Existing `.platform` identity duplication across old reports is outside this page-authoring change; no identities were copied or replaced.

## Acceptance before approval

Open `Templates/TopEvoAnalytics.pbip` with the supported Desktop build and authorized local data. Verify theme load, all thirteen visuals, label fit, native card layout, dropdowns, date sorting, ranking scroll, table widths, focus order and empty states. Exercise each filter and confirm payments follow invoice-date scope. Record Desktop build and synthetic render evidence, then mark verified components Approved in the manifest. Keep customer data and machine-specific configuration out of Git.

## Compact refinement (component specification 1.1.0)

- Removed development-only header context. Navigation now shares the header: 608 x 32 px, five grid slots, default/hover/selected styling. No dummy pages were added.
- Filters occupy three 400 x 56 px slots at y=72. Four value-only KPIs use 296 x 96 px at y=144, 10 pt labels and 28 pt values. Optional comparison/status is documented as a 112 px variant requiring a valid shared-model measure; it is not fabricated in these cards.
- Charts move to y=256; table moves to y=496 and gains 16 px height. Table style, columns and interactions are unchanged. The subsequent Date-dimension step changes only the trend and date-slicer calendar bindings.
- First-render issues remain visible: broken-looking invoice-date trend and `(Blank)` customer. Root cause needs model/data investigation (date parsing, key matching, relationship propagation and customer-name completeness). No blank-exclusion filter, substitute category, report calculation or axis workaround was introduced. See design-system section 10.
- Revised Desktop rendering, optional KPI reference-label behavior and navigation with 3-5 actual pages require verification. Components remain Draft.

## Shared calendar integration

The canonical Date dimension now supplies the monthly trend and date slicer. See `docs/MODEL.md` for range, ISO weeks and inactive date roles. Existing count measures are unchanged. This addresses the missing shared calendar, not null dates or unmatched invoice/customer records. No blank category is hidden. A data refresh and Desktop render are still needed to verify the result.

## Time-granularity demonstration (component specification 1.2.0)

Date range and Display by retain independent behavior within the combined Time control (component specification 1.3.0). The range uses two date inputs without a slider. Display by supports Day, Week, Month, Quarter and Year, default Month; the shared model owns its NAMEOF targets and chronological sort keys. The chart title is Invoice activity. No measures or relationships changed in this extension. See MODEL.md for explicit hierarchies and the ISO-year rule for Calendar Week.

The previous three-wide-filter description is historical; the current control row uses Branch (296 px), combined Time control (608 px) and Customer (296 px). Verify all five grain buttons remain visible without wrapping or scrolling before approval. Before approval, refresh the model and test all five choices against one fixed range, including partial periods and New Year ISO weeks. Verify date-range retention and unchanged KPI/table totals. Static checks do not establish runtime field-parameter behavior.

## TimeControl finalization (1.3.1)

TimeControl retains its current geometry and selected-state styling. Granularity tiles now use the full 328 px width with 2 px item padding. The dynamic trend keeps the five canonical parameter targets and ascending model sorting; explicit 10 pt axis labels and 60 px category spacing protect readability. Long ranges may scroll the chart, never the selector. Desktop verification of all five visible options and every axis transition remains required; components remain Draft.

## Correction after Desktop feedback (1.4.0)

The previous selector still overflowed and Day labels were truncated. That rendering does not approve TimeControl. Current layout is Branch x24/w192, TimeControl x232/w816 (date w280, granularity w536), Customer x1064/w192. The prior geometry descriptions above are historical. The old categorical-axis override and 60 px minimum category width are replaced by a Scalar request; dates/numbers can use automatic continuous ticks and text periods remain categorical.

| State | Bound field | Sort | Static reference check | Desktop interaction |
| --- | --- | --- | --- | --- |
| Day | Date[Date] | Date | Passed | Pending |
| Week | Date[YearWeek] | YearWeekSort | Passed | Pending |
| Month | Date[YearMonth] | YearMonthSort | Passed | Pending |
| Quarter | Date[YearQuarter] | YearQuarterSort | Passed | Pending |
| Year | Date[Year] | Year | Passed | Pending |

Verify all five options are simultaneously visible without arrows, the active option remains highlighted, and switching each option retains date bounds and KPI totals. Day must show meaningful continuous date ticks over a multi-year selection. Record real Desktop results in this table before approving the component. No Desktop process or native Desktop automation is available in the current session; TimeControl remains incomplete pending these checks.

## Accepted rendered reference (1.4.1)

The user has finalized the current TimeControl as the TopEvo standard. Its current visual layout, member IDs, active-state styling and field bindings are frozen. COMPONENTS.json records user-confirmed acceptance, not agent-executed Desktop testing; the Desktop build and independent per-state test evidence remain unrecorded. This supersedes earlier TimeControl pending-approval statements and does not retroactively turn the historical test matrix into executed tests. The reported date lower bound 01.01.0106 is tracked separately in docs/DATE_VALIDITY.md; no source cause is claimed without row evidence.

## Localization integration

This report remains a single definition for de-DE, en-US and ro-RO. Shared model captions and _ReportLabels measures supply translated UI text; Time Granularity.Locale is a hidden host-controlled filter with English default. Numeric Order=2 preserves the initial Month selection across languages. Geometry and business bindings remain stable, but text-measure headers and native visual titles replace literal header text. The localized render is not yet approved: verify all languages and screen-reader text in Desktop/embedding. Native page-navigation captions still use English until the host navigation contract in docs/LOCALIZATION.md is integrated.
