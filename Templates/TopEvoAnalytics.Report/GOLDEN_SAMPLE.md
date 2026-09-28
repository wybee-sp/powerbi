# TopEvo Golden Sample

Permanent internal visual reference. Do not deploy this report to customers.

## Implementation

Overview uses the canonical TopEvo 1.0.0 theme and compact 1.1.0 component layout on the 1280 x 720 grid. Theme resource `StaticResources/RegisteredResources/TopEvo-1.0.0.json` is a synchronized copy; edit only the canonical source and then synchronize it.

`COMPONENTS.json` records the twelve retained visual IDs, slots, geometry and existing model bindings. It is external authoring metadata, not a Power BI definition. All components are Draft until Desktop rendering and embedded verification pass. Existing report identity and shared-model reference are preserved.

The page contains one page-title text box, a native page navigator, three dropdown slicers, four count cards, an invoice-date trend, a customer ranking and a summary table. The navigator currently exposes the single Overview page; there are no placeholder destinations.

## Data and interaction contract

- KPIs: existing `_Measures` invoice count, open invoice count, closed invoice count and payment count. No calculations were created.
- Trend: shared `Date[Year-Month]`, sorted ascending using model Year-Month Sort, and unchanged `_Measures[A8101OP Invoice Count]`. Uses explicit monthly calendar fields.
- Ranking: customer search name and invoice count, descending. Shows all available customer categories with native scrolling; no unsupported Top N filter was invented. Equal search names group together according to the existing model.
- Summary: customer search name and the four KPI measures; fixed column widths and business-facing captions.
- Slicers: invoice date, branch and customer. Multi-select dropdowns initially include all values, with no saved customer selection. Invoice date uses shared `Date[Date]` selections rather than a squeezed range input.
- Each slicer filters all seven analytical visuals. Slicers do not filter each other. Chart/table selections do not change KPIs or other visuals, keeping the reference page stable for component comparison.
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

Open `Templates/TopEvoAnalytics.pbip` with the supported Desktop build and authorized local data. Verify theme load, all twelve visuals, label fit, native card layout, dropdowns, date sorting, ranking scroll, table widths, focus order and empty states. Exercise each filter and confirm payments follow invoice-date scope. Record Desktop build and synthetic render evidence, then mark verified components Approved in the manifest. Keep customer data and machine-specific configuration out of Git.

## Compact refinement (component specification 1.1.0)

- Removed development-only header context. Navigation now shares the header: 608 x 32 px, five grid slots, default/hover/selected styling. No dummy pages were added.
- Filters occupy three 400 x 56 px slots at y=72. Four value-only KPIs use 296 x 96 px at y=144, 10 pt labels and 28 pt values. Optional comparison/status is documented as a 112 px variant requiring a valid shared-model measure; it is not fabricated in these cards.
- Charts move to y=256; table moves to y=496 and gains 16 px height. Table style, columns and interactions are unchanged. The subsequent Date-dimension step changes only the trend and date-slicer calendar bindings.
- First-render issues remain visible: broken-looking invoice-date trend and `(Blank)` customer. Root cause needs model/data investigation (date parsing, key matching, relationship propagation and customer-name completeness). No blank-exclusion filter, substitute category, report calculation or axis workaround was introduced. See design-system section 10.
- Revised Desktop rendering, optional KPI reference-label behavior and navigation with 3-5 actual pages require verification. Components remain Draft.

## Shared calendar integration

The canonical Date dimension now supplies the monthly trend and date slicer. See `docs/MODEL.md` for range, ISO weeks and inactive date roles. Existing count measures are unchanged. This addresses the missing shared calendar, not null dates or unmatched invoice/customer records. No blank category is hidden. A data refresh and Desktop render are still needed to verify the result.
