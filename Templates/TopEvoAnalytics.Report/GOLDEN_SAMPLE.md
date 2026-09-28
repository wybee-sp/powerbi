# TopEvo Golden Sample

Permanent internal visual reference. Do not deploy this report to customers.

## Implementation

Overview uses the canonical TopEvo 1.0.0 theme and exact 1280 x 720 overview grid. Theme resource `StaticResources/RegisteredResources/TopEvo-1.0.0.json` is a synchronized copy; edit only the canonical source and then synchronize it.

`COMPONENTS.json` records the thirteen fresh visual IDs, slots, geometry and existing model bindings. It is external authoring metadata, not a Power BI definition. All components are Draft until Desktop rendering and embedded verification pass. Existing report identity and shared-model reference are preserved.

The page contains two header text boxes, a native page navigator, three dropdown slicers, four count cards, an invoice-date trend, a customer ranking and a summary table. The navigator currently exposes the single Overview page; there are no placeholder destinations.

## Data and interaction contract

- KPIs: existing `_Measures` invoice count, open invoice count, closed invoice count and payment count. No calculations were created.
- Trend: existing `a42001.InvoiceDate`, sorted ascending, and `_Measures[A8101OP Invoice Count]`. Uses actual dates, not a fabricated monthly hierarchy or missing Date dimension.
- Ranking: customer search name and invoice count, descending. Shows all available customer categories with native scrolling; no unsupported Top N filter was invented. Equal search names group together according to the existing model.
- Summary: customer search name and the four KPI measures; fixed column widths and business-facing captions.
- Slicers: invoice date, branch and customer. Multi-select dropdowns initially include all values, with no saved customer selection. Invoice date uses date selections rather than a squeezed range input.
- Each slicer filters all seven analytical visuals. Slicers do not filter each other. Chart/table selections do not change KPIs or other visuals, keeping the reference page stable for component comparison.
- Payment counts refer to payments associated with the selected invoices through existing relationships; the period filter is invoice date, not payment date. Existing unmatched keys and relationship behavior still need data-level verification.

## Deliberate limits

- No comparison deltas, targets, refresh timestamp or currency amounts: suitable existing measures are absent or unnecessary for this count-based sample.
- No reset bookmark or drillthrough destination was fabricated. Use slicer clear controls; a future approved navigation/reset component can extend the sample.
- Theme integration was implemented directly in PBIR as requested. No Desktop save/import was performed.
- Report/page definitions pass their published schemas. The repository's visual-container 2.12.0 schema URL returns 404; visual structures were checked against published 2.9.0 using an in-memory schema-declaration substitution only. Files retain 2.12.0. This is a compatibility check, not full 2.12 certification.
- Theme parity, model field/measure existence, unique visual IDs, bounds, non-overlap and interaction references are statically checked. Actual rendering, data refresh, tab/focus behavior and embedded readability remain unverified.
- Desktop build: not yet recorded. Native desktop automation is unavailable in this session. Review the report in Desktop before approving components for future page generation.
- Existing `.platform` identity duplication across old reports is outside this page-authoring change; no identities were copied or replaced.

## Acceptance before approval

Open `Templates/TopEvoAnalytics.pbip` with the supported Desktop build and authorized local data. Verify theme load, all thirteen visuals, label fit, native card layout, dropdowns, date sorting, ranking scroll, table widths, focus order and empty states. Exercise each filter and confirm payments follow invoice-date scope. Record Desktop build and synthetic render evidence, then mark verified components Approved in the manifest. Keep customer data and machine-specific configuration out of Git.
