# TopEvo analytics design system

Version: 1.0.0 | Status: visual foundation; Golden Sample components pending

## 1. Purpose and required inputs

TopEvo analytics is a compact, modern light interface for an embedded B2B ERP application. Use neutral surfaces, readable numbers, consistent alignment and restrained blue accents. Color communicates selection, comparison or business status. Avoid decorative gradients, large shadows and unnecessary chrome.

Every future generated page must use:

1. Shared `Templates/TopEvoAnalytics.SemanticModel`.
2. Canonical `Templates/Theme/TopEvo.json`.
3. The 1280 x 720 TopEvo grid below.
4. Approved components from `Templates/TopEvoAnalytics.Report`.
5. Business measures from `_Measures`.
6. No customer data or machine-specific paths in Git.

The Golden Sample is a permanent internal reference, not a customer report. Exclude it from customer deployment. Its current empty page is not an approved component library. This release establishes the theme and authoring contract only: no theme import, visual definitions, module redesign or semantic-model migration.

## 2. Compatibility and ownership

- Schema baseline: Microsoft's `reportThemeSchema-2.150.json` (Desktop 2.150 family). This is a validation baseline, not a claim that it is the newest release.
- The theme passed static validation against that schema. Desktop import, rendering, export and embedded-browser verification are pending.
- Validated Desktop build: **not yet recorded**. Record the exact build, theme version and verification date when approving the first Golden Sample.
- The theme's schema URL references a versioned filename on Microsoft's mutable main branch. Reproducible CI should cache/pin the schema content and record its hash.
- `TopEvo.json` owns encoded colors and defaults. This document owns layout, behavior and component usage. Update both and the changelog together.
- Report theme resources are distribution copies. Import the canonical theme through Desktop, preserve generated resource registration and verify parity. Do not replace Microsoft's base-theme file.

References: [Microsoft custom themes](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom), [theme schema](https://github.com/microsoft/powerbi-desktop-samples/blob/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.150.json), [PBIP report definitions](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report).

## 3. Palette

| Token | Hex | Use |
| --- | --- | --- |
| Canvas | `#F5F7FA` | Page, wallpaper and table headers |
| Surface | `#FFFFFF` | Content surfaces and controls |
| Text primary | `#182230` | Values, headings and body |
| Text secondary | `#526174` | Supporting labels and axes |
| Border | `#DCE3EB` | Quiet surface boundaries |
| Gridline | `#E9EEF4` | Chart guides and row separators |
| Primary | `#2F5D8C` | Actuals, links and active controls |
| Selected surface | `#EAF0F7` | Selected controls and sequential-scale minimum |
| Comparison | `#7D8FA3` | Previous period/reference series |
| Secondary series | `#537F83` | Optional third series |
| Favorable | `#247451` | Favorable business outcome |
| Attention | `#946200` | Warning or threshold attention |
| Unfavorable | `#B54745` | Unfavorable business outcome |

Default series order: primary, comparison, secondary series. Prefer at most three series. A palette neither limits series count nor associates a color permanently with a measure: approved components must bind semantic colors explicitly. Keep status colors out of the categorical palette. Theme `neutral` means attention; ordinary neutral text uses Text secondary.

An increase is favorable only when the metric definition says so. Pair status color with text or symbols. Pale borders/gridlines are decorative; interactive focus and selection need stronger indicators. Acceptance targets: 4.5:1 for normal text and 3:1 for large text and essential graphical controls. Verify at the actual embedded size.

## 4. Typography and formats

Use Segoe UI, with Segoe UI Semibold for hierarchy. Font sizes are Power BI points; layout uses canvas pixels. Verify font availability and scaling in the embedded host.

| Element | Size | Weight |
| --- | --- | --- |
| Page title | 20-22 pt | Semibold |
| KPI value | 30 pt default; 28-32 allowed | Semibold |
| Section/visual title | 12-13 pt | Semibold |
| KPI label | 11 pt | Regular |
| Table values and filters | 10-11 pt | Regular |
| Secondary context | 9-10 pt | Regular |

Use sentence case and concise business captions. Left-align text, right-align numeric table values. Avoid source codes in labels. Permit deliberate two-line titles; do not repeatedly shrink fonts for long content.

- Model measures own numeric format strings. Keep measures numeric rather than using DAX FORMAT for presentation.
- Counts: whole numbers with locale-aware grouping. Percentages: normally one decimal; distinguish percentage change from percentage-point difference.
- Detail amounts: normally two decimals. State KPI/chart display units consistently; tooltips expose exact values.
- Show reporting currency. Never aggregate different currencies without an explicit conversion rule.
- Use a documented display locale. Source parsing locale is a separate data contract.
- Distinguish unavailable values from zero. Show "No comparison" for an unavailable or unsuitable baseline.

## 5. Canvas and grid

Standard pages: 1280 x 720, Fit to page. Outer margin 24 px; gutter 16 px; surface padding 16 px; internal spacing steps 4/8 px. Default radius 4 px; no shadow.

Content width is 1232 px: twelve 88 px columns plus eleven 16 px gutters. A span of n columns is `88*n + 16*(n-1)` px. Column start is `24 + 104*i` for zero-based i. Use integer positions. Set and validate geometry explicitly in PBIR; importing the theme does not lay out a page.

| Overview region | X | Y | Width | Height |
| --- | ---: | ---: | ---: | ---: |
| Header/context | 24 | 24 | 1232 | 40 |
| Navigation and filters | 24 | 80 | 1232 | 56 |
| KPI 1 | 24 | 152 | 296 | 104 |
| KPI 2 | 336 | 152 | 296 | 104 |
| KPI 3 | 648 | 152 | 296 | 104 |
| KPI 4 | 960 | 152 | 296 | 104 |
| Trend | 24 | 272 | 816 | 224 |
| Ranking | 856 | 272 | 400 | 224 |
| Summary table | 24 | 512 | 1232 | 184 |

The control strip has four 296 px slots at x=24/336/648/960: compact page navigation, period, branch and business entity. Labels and controls fit within the 56 px height. Extra filters use a secondary panel; Reset belongs in the header action area. A date range may need an approved wider variant; never compress inputs until unreadable.

Two equal panels use 608 px each. A detail-page variant keeps header/controls and gives the table x=24, y=152, width=1232, height=544. The overview table shows a short summary. Tooltip/mobile variants need separately documented dimensions and approval.

## 6. Component standards

These specifications await Golden Sample implementation and approval.

### KPI cards

- Three or four consistent cards per overview; default four-card geometry above.
- Order: label, value, comparison with named period. White surface, subtle border, dark value; status color on comparison text/icon.
- Bind explicit `_Measures` measures. Declare whether cards respond to chart selections.
- The theme supplies card typography; bindings, reference labels, alignment and comparison states are component settings.
- Keep currency/unit visible. Test large/negative values, blanks and missing baselines.

### Charts

- Native lines for trends, horizontal bars for rankings, columns for period comparisons.
- Use explicit Date fields and chronological Year-Month sorting, never absent automatic hierarchies.
- Bar/column numeric axes start at zero. Set the correct numeric axis per component; orientation differs by chart type.
- Blue actuals, slate comparison. Add line-style distinctions or labels when needed. Single-series charts omit legends; comparison charts identify series clearly.
- Quiet gridlines, 2 px trend strokes, markers/data labels off by default. Add labels only where readable.
- Titles name metric and grouping. If axis titles are hidden, state units in title/subtitle/context.
- Rankings have stated Top N and explicit sort. Tooltips show exact values, units and period.
- Document cross-filter/highlight behavior. Avoid decorative gauges and unjustified dual axes.

### Tables and matrices

- Tables show records; matrices show meaningful hierarchies. Light semibold headers, white rows, horizontal separators; no default vertical grid.
- Target 28-32 px row height. Theme row padding is 6 px; verify rendered height.
- Set deliberate column widths. Avoid horizontal scrolling on overview pages. Long labels need an approved wrap/tooltip treatment.
- Align numbers right and text left in the component.
- Enable totals/subtotals only for meaningful aggregations. Do not sum identifiers, unit prices or percentages. Ratios need explicit total measures.
- Keep conditional formatting limited and readable. Define matrix expansion/subtotal state explicitly.

### Slicers and filters

- Visible labels, consistent dropdowns and search for long lists. Primary filters: period, branch, business entity.
- Define selection mode and intentional defaults. Synchronize relevant slicers across related pages.
- Display active date range and currency. Reset restores documented defaults, not incidental author selections.
- Advanced filters use a secondary panel. Validate date-input width.
- Authorized company context comes from the host/security model; slicers cannot enforce tenant isolation.

### Header and navigation

- Left: module/page title. Right: reporting context and actions. Refresh time must come from a genuine refresh timestamp, not the current clock.
- ERP host owns global navigation; reports switch analytical pages. Active pages use blue underline/tint and clear labels.
- Navigation bookmarks must not unintentionally capture old data selections. Reset bookmarks separately capture intentional filter defaults.
- Drillthrough includes Back and entity context; retain authorized context.
- Provide meaningful accessible names, visible focus and logical tab order. Target controls at least 32 px high and verify at embedded scale.

### Empty and unavailable states

- Distinguish no matching rows, unavailable comparison and refresh failure/staleness.
- Give a short explanation and a relevant recovery action where possible.
- Do not invent zero values or freshness. Document whether the host owns loading/error presentation.

## 7. Theme coverage and limitations

The JSON defines structural/status colors, four primary text classes, global surfaces/padding/titles, page backgrounds and filter-pane defaults. Specific styles cover `cardVisual`, `lineChart`, `clusteredBarChart`, `clusteredColumnChart`, `tableEx`, `pivotTable` and `slicer`. Text, shapes, images and button/navigation containers opt out of global surface backgrounds/borders.

- This schema uses `cardVisual.label` and `cardVisual.value` for the new card. Formatting names differ from older card types and UI captions.
- Custom defaults are layered with base-theme and local visual formatting. Existing overrides can take precedence; inspect/reset relevant properties during adoption.
- Themes cannot enforce this grid, model selection, field bindings, identities, interactions, accessibility text, bookmarks, security or deployment exclusions.
- The schema exposes page-size properties, but dimensions remain explicit PBIR requirements. The theme does not impose global dimensions on tooltip pages.
- Palettes do not guarantee semantic series mapping or prevent additional generated colors.
- Exact row heights, column widths, number formats, status thresholds, date sorting, navigation states and KPI reference labels need component/model settings and runtime checks.
- Extensible/wildcard schema areas mean validation alone cannot prove every setting is honored. Prefer explicit native properties and verify in Desktop.
- Font files are not distributed with a theme; verify Segoe UI in the target environment.

## 8. Golden Sample and generation workflow

Permanent source: `Templates/TopEvoAnalytics.Report`, referencing the shared model. It remains internal after working examples are added.

1. In a separately authorized step, implement an overview and component-reference page using synthetic/local test data. Commit no customer exports.
2. Author native components in Desktop and retain exported PBIR. Apply the canonical theme and grid.
3. Maintain an external manifest recording Draft/Approved status, version, Desktop build, IDs, field roles, measures, geometry, formatting exceptions, interactions, accessibility and dependencies.
4. Approve after static checks, rendering and interaction tests. There are **no Approved components in this release**; production generation waits for that gate.
5. Clone approved components with appropriate IDs and validated bindings. Update page order, navigation, bookmarks, interactions and filters together.
6. Import/synchronize the canonical theme and preserve registered resources. Check parity rather than hand-styling distribution copies.
7. Record design-system/component versions in external generation metadata, not arbitrary Power BI JSON properties.
8. Validate outputs and exclude the reference report from customer deployment.

Suggested manifest slots: `header.context`, `navigation.pages`, `filter.period`, `filter.branch`, `filter.entity`, `kpi.primary`, `kpi.secondary`, `chart.trend`, `chart.ranking`, `table.summary`. These are external roles, not new PBIR properties. Matrix, tooltip, drillthrough and empty-state examples belong on the reference page.

## 9. Validation and releases

Foundation checks: JSON parsing/schema validation, theme/document consistency, `git diff --check` and exact changed-file review.

Before adoption/component approval:

- Import into the recorded Desktop build; open/save PBIP and inspect resource references.
- Check canvas bounds, margins, overlap, typography and numeric formats.
- Validate bindings against the shared model and `_Measures`; test dates, filters and meaningful totals.
- Test long labels, large/negative values, empty states and missing comparisons.
- Verify reset, navigation, drillthrough, keyboard order, alternative text, focus and contrast in the embedded host.
- Review synthetic screenshots; confirm no customer selections, credentials or machine paths enter Git.
- Confirm customer deployment excludes the Golden Sample and uses the intended shared-model instance.

Version theme, documentation and component manifests together: major for incompatible contracts, minor for compatible additions, patch for fixes. Record migrations in the changelog. Customer overrides may compose approved components without changing standard templates or model contracts. Existing module/model issues remain separate migration work; this foundation does not certify them as compliant.
