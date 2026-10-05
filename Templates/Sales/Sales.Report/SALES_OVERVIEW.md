# Sales Overview

Uses the approved Golden Sample 1280 x 720 layout and frozen TimeControl, canonical theme and shared semantic model. Existing report identity, dataset reference and Overview page ID are preserved. Existing Sales visual IDs are retained for redesigned components; new components receive unique IDs. The pre-existing empty Receivables page is retained but hidden from navigation. It has no Sales content.

## Measures and scope

- Net Revenue = existing a42001[Net Revenue] = SUM(a420011[NetAmount]), with existing EUR format. Used by KPI, dynamic trend, descending customer ranking and summary.
- Invoice Count = existing a42001[Invoice Count] = COUNTROWS(a42001). It counts header rows, not distinct invoice numbers or open items. Used by KPI and summary.
- Average Invoice Value is absent and is not rendered.
- No additional suitable Sales measure exists. Only the two available KPIs render, each 608 x 96 px at x=24/648, y=144, with a 16 px gutter. Payment/open-item measures are not substituted for Sales metrics.

These are existing model definitions, not newly validated business totals. They remain on a42001 as an explicit legacy reuse exception to the preferred _Measures home: moving them would broaden scope and risk other report references. No model or report calculations were created. Source exports are unavailable here, so currency uniformity, cancellations/credits, header grain, key uniqueness, locale parsing and totals still require data-owner validation before deployment. The existing Net Revenue measure does not add status/cancellation filters. EUR is inherited from the model, not a new conversion assumption.

## Interaction contract

Branch -> TimeControl -> Customer. Date[Date] filters invoice headers through the existing active relationship; headers filter Sales lines. Time Granularity changes only the revenue trend, with Day=Date, Week=YearWeek, Month=YearMonth, Quarter=YearQuarter, Year=Year and existing chronological sort metadata. Month is default. Branch/date/customer filter both active KPI cards, the trend, ranking and summary. The approved selector geometry and styles are preserved. Customer names with identical labels aggregate together, as in the current model. No blank exclusions or date-quality workarounds were added.

## Validation

Static validation covers model bindings, parameter targets, report resources, identity preservation, geometry and interactions. Visual schema 2.12 URL remains unavailable; compatibility checks use published 2.9 in memory without changing declarations. Sales Desktop rendering, five-state interaction checks, refresh and revenue reconciliation remain pending. The known ancient-date issue remains open in docs/DATE_VALIDITY.md. This is an implemented Sales page, not a claim of deployment readiness.

## Initial implementation file inventory (historical)

- `Templates/Sales/Sales.Report/COMPONENTS.json`
- `Templates/Sales/Sales.Report/SALES_OVERVIEW.md`
- `Templates/Sales/Sales.Report/StaticResources/RegisteredResources/TopEvo-1.0.0.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/page.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/077d31a04274ad85ed05/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/0aa8e8393114177d073d/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/180c9822021860e112cb/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/4147a08e764043acbe6d/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/48080225a009c7816619/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/83289b6c6dda4d7292bf/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/8eedc44eb7424924b051/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/c85dcd65ae5d7a09692d/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/d5eafabc9a22487ab761/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/e61b9b4c725baec66b1d/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/f0f9619e57eeb2b79732/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/f600a358f6b04952b55a/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/ReportSection/visuals/fdce3d4398dea1000cb5/visual.json`
- `Templates/Sales/Sales.Report/definition/pages/cc2566e279b27d3608e1/page.json`
- `Templates/Sales/Sales.Report/definition/pages/pages.json`
- `Templates/Sales/Sales.Report/definition/report.json`

## Adaptive KPI revision

Removed both unavailable KPI placeholder visuals and their interaction references. Net Revenue and Invoice Count retain their IDs, bindings and styles, with two equal 608 px cards. The manifest is synchronized. TimeControl and all other visual geometry are unchanged. The two deleted placeholder files in the historical inventory above no longer exist.

## Localization integration

This report remains a single definition for de-DE, en-US and ro-RO. Shared model captions and _ReportLabels measures supply translated UI text; Time Granularity.Locale is a hidden host-controlled filter with English default. Numeric Order=2 preserves the initial Month selection across languages. Geometry and business bindings remain stable, but text-measure headers and native visual titles replace literal header text. The localized render is not yet approved: verify all languages and screen-reader text in Desktop/embedding. Native page-navigation captions still use English until the host navigation contract in docs/LOCALIZATION.md is integrated.


## Central generation adoption

`Templates/Sales/overview.bindings.json` now declares this report/Overview STANDARD and preserves its existing IDs, Sales queries and label keys. The hidden Receivables page is protected and outside generator ownership. The central `Templates/PageTemplates/overview.layout.json` describes the shared geometry and Golden Sample sources. Run the candidate/validation workflow in `docs/GENERATION.md`; the current Golden Sample render gate prevents live synchronization. Existing Sales PBIR remains unchanged by this adoption. The two existing measures on a42001 are explicitly documented legacy bindings; no measure migration or new business calculation is introduced.
