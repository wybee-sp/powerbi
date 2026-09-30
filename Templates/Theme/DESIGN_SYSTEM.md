# TopEvo analytics design system

Component specification: 1.5.2 | Canonical theme: 1.0.0 | Status: TimeControl accepted as rendered Golden Sample reference

## 1. Purpose and required inputs

TopEvo analytics is a compact, modern light interface for an embedded B2B ERP application. Use neutral surfaces, readable numbers, consistent alignment and restrained blue accents. Color communicates selection, comparison or business status. Avoid decorative gradients, large shadows and unnecessary chrome.

Every future generated page must use:

1. Shared `Templates/TopEvoAnalytics.SemanticModel`.
2. Canonical `Templates/Theme/TopEvo.json`.
3. The 1280 x 720 TopEvo grid below.
4. Approved components from `Templates/TopEvoAnalytics.Report`.
5. Business measures from `_Measures`.
6. No customer data or machine-specific paths in Git.

The Golden Sample is a permanent internal reference, not a customer report. Exclude it from customer deployment. The Overview now implements the theme and component layout. The user reported a first Desktop rendering; the current TimeControl has now been accepted by the user as the rendered standard. Module reports are unchanged. The subsequent canonical Date integration is documented in `docs/MODEL.md`.

## 2. Compatibility and ownership

- Schema baseline: Microsoft's `reportThemeSchema-2.150.json` (Desktop 2.150 family). This is a validation baseline, not a claim that it is the newest release.
- The theme passed static validation against that schema. A first Desktop rendering was reported by the user. The current TimeControl rendering is user-accepted; independent export and embedded-browser verification remain unrecorded.
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
| KPI value | 28 pt compact; 30 pt theme default | Semibold |
| Section/visual title | 12-13 pt | Semibold |
| KPI label | 10 pt compact; 11 pt theme default | Regular |
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

| Compact Overview region | X | Y | Width | Height |
| --- | ---: | ---: | ---: | ---: |
| Page title | 20 | 16 | 600 | 48 |
| Page navigation | 648 | 16 | 608 | 40 |
| Branch filter | 24 | 72 | 192 | 56 |
| Time control: date range | 232 | 72 | 280 | 56 |
| Time control: granularity | 512 | 72 | 536 | 56 |
| Customer filter | 1064 | 72 | 192 | 56 |
| KPI 1 | 24 | 144 | 296 | 96 |
| KPI 2 | 336 | 144 | 296 | 96 |
| KPI 3 | 648 | 144 | 296 | 96 |
| KPI 4 | 960 | 144 | 296 | 96 |
| Trend | 24 | 256 | 816 | 224 |
| Ranking | 856 | 256 | 400 | 224 |
| Summary table | 24 | 496 | 1232 | 200 |

Navigation shares the header instead of consuming a filter slot. Branch and Customer each span two grid columns. The combined Time control spans eight grid columns (816 px), with contiguous date-range and granularity visuals on a single white surface. Its internal split is 280/536 px, with no canvas gutter or individual borders; standard 16 px gutters separate it from Branch and Customer. Date range uses two native date inputs; hide the redundant slider to preserve the compact 56 px height. Verify date-input legibility at embedded scale. Keep 16 px vertical gaps and the 24 px bottom margin. The table gains 16 px of height compared with the first sample. Its existing style is preserved.

The navigation starts at the seventh grid column (x=648). Its five-slot grid has 4 px internal spacing and a 32 px target height. It supports 3-5 short page names in one row; keep unused slots empty instead of inventing destinations. The current report contains only Overview. Validate both the one-page and five-page render before approving this component. Do not allow a single tab to become a full-width 608 px button.

Two equal panels remain 608 px each. The detail variant keeps this compact header and filter row, with table x=24, y=144, width=1232, height=552. Tooltip/mobile variants require separate dimensions and approval.

## 6. Component standards

These specifications are implemented in the Golden Sample where existing fields/measures support them. Approval awaits verification of the revised rendering.

### KPI cards

- KPI slots are optional. Render only KPIs backed by existing, validated semantic-model measures. Never render empty cards, Not available, N/A, placeholder text or invented KPIs merely to fill the grid. Document missing measures outside the report canvas. With zero suitable measures, omit the KPI row.
- Adapt the row to the available KPIs; the four-card geometry above is the Golden Sample variant, not a required slot count. On the standard 1232 px content width, use the following equal-width layouts with 16 px gutters:

| KPI count | Card width | X positions | Grid span per card |
| --- | --- | --- | --- |
| 1 | 1232 px where appropriate | 24 | 12 columns |
| 2 | 608 px | 24, 648 | 6 columns |
| 3 | 400 px | 24, 440, 856 | 4 columns |
| 4 | 296 px | 24, 336, 648, 960 | 3 columns |

- More than four KPIs requires an explicit page-design decision; never automatically add another row. The row adapts to authored, approved measure availability, not transient blank results for a particular filter selection; handle valid measures with no data using their defined empty-state behavior.
- Value-only variant: y=144, 96 px high, 12 px vertical and 16 px horizontal padding. Sales Overview uses the two-card variant. Preserve the charts below at y=256.
- Label first: 10 pt regular secondary text, single line, left aligned. Primary value: 28 pt semibold primary text, left aligned. Do not duplicate the label as a container title.
- Optional comparison/status appears below the value at 9-10 pt with a named period or explicit status meaning. It requires an existing approved shared-model measure and an appropriate native reference-label binding; no static sample delta, report calculation or decorative status badge.
- With no comparison/status binding, omit that row entirely. The current four cards use this value-only variant. Do not display four repetitive "No comparison" placeholders.
- When comparison/status is enabled, use 112 px cards for the entire row. Keep KPI y=144; move chart y to 272 and use chart height 208. Keep the table at y=496, height=200. This preserves gaps and gives the additional line 16 px without compressing the value.
- If an enabled comparison has an unavailable baseline, display "No comparison" using approved model/component behavior; do not substitute zero. Status color applies to the optional line, accompanied by text/icon. White surface, subtle border and dark primary value remain unchanged.
- Bind explicit `_Measures` measures. All sample cards respond to the three slicers, not chart/table selections. Preserve unit/currency context when relevant.
- Reference-label configuration for the optional variant awaits a valid model measure and Desktop verification. The manifest documents this extension; it is not falsely marked implemented or approved.
- Test large/negative values and long labels at actual embedded size. Do not shrink values below 28 pt to compensate for a wrong card size.

### Charts

- Native lines for trends, horizontal bars for rankings, columns for period comparisons.
- Use explicit Date fields and chronological YearMonth sorting, never absent automatic hierarchies.
- Bar/column numeric axes start at zero. Set the correct numeric axis per component; orientation differs by chart type.
- Blue actuals, slate comparison. Add line-style distinctions or labels when needed. Single-series charts omit legends; comparison charts identify series clearly.
- Quiet gridlines, 2 px trend strokes, markers/data labels off by default. Add labels only where readable.
- Titles name metric and grouping. If axis titles are hidden, state units in title/subtitle/context.
- Rankings have stated Top N and explicit sort. Tooltips show exact values, units and period.
- Document cross-filter/highlight behavior. Avoid decorative gauges and unjustified dual axes.

### Tables and matrices

- The current Golden Sample summary table is the TopEvo table-style baseline: retain 6 px row padding, 10 pt Segoe UI, light semibold headers, white rows, subtle horizontal separators and no vertical grid. Its customer column is 400 px and four count columns are 190 px each. Compact-layout changes increase container height, not row density.
- Tables show records; matrices show meaningful hierarchies. Light semibold headers, white rows, horizontal separators; no default vertical grid.
- Target 28-32 px row height. Theme row padding is 6 px; verify rendered height.
- Set deliberate column widths. Avoid horizontal scrolling on overview pages. Long labels need an approved wrap/tooltip treatment.
- Align numbers right and text left in the component.
- Enable totals/subtotals only for meaningful aggregations. Do not sum identifiers, unit prices or percentages. Ratios need explicit total measures.
- Keep conditional formatting limited and readable. Define matrix expansion/subtotal state explicitly.

### Slicers and filters

- Mandatory primary-filter order on all standard pages: **Branch -> Time control -> business-specific filters**. Branch is always leftmost; the combined date/period and granularity group immediately follows it. Keyboard order is Branch -> date range -> granularity -> business filters.
- Sales/Receivables: Branch -> Invoice date -> Customer. Purchases: Branch -> Purchase date -> Supplier. Inventory: Branch -> Date -> Warehouse. Choose the ERP operating context first, then the period and business dimension.
- Preserve this order across pages. An exception requires a documented business requirement and its rationale in the affected report documentation.
- Display by belongs inside the Time control immediately adjacent to the date inputs. It is a presentation control, not a business filter or separate standard slot. The Golden Sample order is Branch -> [Date range + Day / Week / Month / Quarter / Year] -> Customer. Date range determines WHAT period is analyzed; granularity determines HOW it is grouped.
- Visible labels, consistent dropdowns and search for long lists.
- Define selection mode and intentional defaults. Synchronize relevant slicers across related pages.
- Display active date range and currency. Reset restores documented defaults, not incidental author selections.
- Advanced filters use a secondary panel. Validate date-input width.
- Authorized company context comes from the host/security model; slicers cannot enforce tenant isolation.

### Header and navigation

- Left: 20 pt module/page title. Right: compact native page navigation; reserve contextual actions for a separate documented variant. No internal development labels on the canvas. Refresh time must come from a genuine refresh timestamp, not the current clock.
- ERP host owns global navigation; reports switch analytical pages. Use 10 pt short labels, centered in 32 px tabs. Default text is secondary gray; hover uses a pale blue fill; selected uses blue semibold text, pale fill and a 2 px bottom accent. Keep the navigator container transparent, with zero padding and no outer border. Exclude hidden/tooltip pages.
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

## 10. Known model/data dependencies from the first Desktop rendering

The user reported a broken-looking invoice-date trend and a `(Blank)` customer category. These remain visible and are not styling defects to conceal.

- Trend: the canonical Date integration uses the shared Time Granularity parameter (default `Date[YearMonth]`) with the existing invoice-count measure and a separate date-range slicer on `Date[Date]`. A refresh/render must verify this change. Source date parsing/nulls, invoice/open-item key matches and relationship propagation can still affect results; the exact cause of any remaining data issue is not established by visual feedback alone.
- Customer `(Blank)`: check empty customer search names, missing/unmatched customer keys and uniqueness across company scope. Equal search names also group together under the existing binding. Fix source/model semantics in a separately scoped change.
- Do not add exclusion filters for blanks, substitute labels, switch axes to disguise gaps, coalesce missing values or introduce report-level calculations. Preserve the existing bindings and data visibility until the underlying cause is resolved.
- Static PBIR checks cannot prove data correctness. Approval requires model/data verification and another Desktop render; no claim of production data readiness is implied by this visual refinement.

## 11. Time range and display granularity

Every analytical trend distinguishes two controls:

- **Date range** selects the inclusive start/end of the analyzed period, using Date[Date]. It filters data and KPI totals.
- **Display by** selects Day, Week, Month, Quarter or Year, in that order. It changes only the grouping of the same period in one trend visual.

Use the shared Time Granularity field parameter. Month is the default; native horizontal tile slicer with strict single selection, no Select all. Show Day, Week, Month, Quarter and Year together in one row at 10 pt; preserve visible selected/focus states. The two native visuals form one reusable Time control, not a new model filter. Use a shared white surface, aligned headers and no internal card borders. Avoid dropdowns for the five fixed grains. The chart title is grain-neutral ("Invoice activity"); the visible selector states the grain. Axis fields and sorting come from the shared model, as specified in MODEL.md. Use year-qualified week/month/quarter labels so periods cannot merge across years. The axis requests continuous scaling for real date/numeric fields; text period fields use categorical axes. It and sorts chronologically via parameter sortDirection and the selected column's SortByColumn metadata.

Do not create five separate charts, use weekday names for daily analysis, encode grouping in a report measure or add another calendar table. Explicit Calendar and Calendar Week hierarchies support drill navigation elsewhere; the Display by control selects one standalone grain.

In the Golden Sample, Branch/Date range/Customer filter all seven analytical visuals. Display by targets only the trend, not KPIs, rankings, the table or other slicers. All incoming interactions to Display by are disabled. Selection of Week does not extend the range to complete weeks: edge buckets remain partial. Show no fabricated zero values or blank-exclusion filters.

For a reset component, restore Date range and Display by explicitly and independently (default grain Month). Clearing a native field parameter means all fields, so do not expose a clear/all action for this selector. Test the host's reset and bookmark behavior. The same disconnected parameter can control related trends when intentional, but cross-page slicer synchronization must be explicitly chosen.

The compact reference remains 1280 x 720 with 24 px margins, 16 px gutters and an unchanged KPI/chart/table layout. The control row has three conceptual groups: Branch (192 px), Time control (816 px) and Customer (192 px). The Time control occupies eight grid columns, forming a continuous surface. Validate both date inputs and all five grain buttons without wrapping or scrolling at actual scale; do not shrink text below the design standard. All five grain transitions, range retention, ISO boundaries and unchanged KPI totals must pass Desktop/embedded verification before component approval.


### TimeControl component contract (1.4.0)

TimeControl is one reusable component composed of two native slicers. Keep its 816 x 56 px group between Branch and the business filter, with date inputs at x=232 (280 px) and Display by at x=512 (536 px). Preserve the shared white surface, identities, independent bindings and interactions when reusing it. COMPONENTS.json records both members; copying only one member does not reproduce the component.

All five labels must be visible: Day | Week | Month | Quarter | Year. The selector uses Segoe UI 10 pt, 2 px item padding and no horizontal container padding, making all 536 px available. Preserve native selected-state highlighting and strict single selection; Month remains the saved default. Do not override all tile backgrounds with one static color. No selector scrolling, clipped text, wrapping or overflow is acceptable at the supported embedded size. Actual fit and highlight require Desktop/embedded verification; static layout checks cannot certify them.

The Invoice activity axis resolves one shared field parameter:

| Display by | Canonical axis | Chronological ordering |
| --- | --- | --- |
| Day | Date[Date], actual date | Date ascending |
| Week | Date[YearWeek] | YearWeekSort |
| Month | Date[YearMonth] | YearMonthSort |
| Quarter | Date[YearQuarter] | YearQuarterSort |
| Year | Date[Year] | Numeric ascending |

Axis labels use 10 pt Segoe UI with no numeric abbreviation. Request Scalar (continuous) scaling for Day and numeric Year. Day resolves to the real Date[Date] column, which remains dateTime with date-only metadata and yyyy-MM-dd format; automatic tick selection can show fewer ticks over long ranges without changing daily aggregation. Text YearWeek, YearMonth and YearQuarter use categorical fallback, preserving model sort keys. Remove the old 60 px minimum category width: it forced daily categories into narrow, truncated labels and scrolling.

The parameter binding remains Category.fieldParameters -> Time Granularity[Fields], not a label substitution. Its five NAMEOF targets and model sort keys are checked individually. The saved Month projection and corresponding sort are the initial state; parameter sortDirection Ascending governs resolved fields. Runtime transitions from Month to Day and back must confirm Desktop resolves the field and axis type correctly. No per-grain tick interval expressions or automatic hierarchies are added.

Microsoft documents that text axes are always categorical and dates/numbers support continuous scaling: [axis guidance](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-customize-x-axis-and-y-axis). The mixed-type parameter behavior still requires runtime verification.

Before approval, test all five selections over a fixed range, an ISO year boundary and a multi-year range. Check chronological labels, unchanged date inputs and KPI totals, selected-state highlighting, all five buttons without selector overflow, and keyboard traversal. Capture the Desktop build and actual render evidence.

## Accepted TimeControl reference (1.4.1)

The user finalized the current rendered implementation as the standard. Freeze the existing 1280 x 720 layout: Branch x24/w192; TimeControl x232/w816 with date range w280 and granularity x512/w536; Customer x1064/w192; all y72/h56. Preserve the active-grain styling and parameter bindings. No PBIR layout change accompanies this acceptance. Earlier pending-render notes describe the development history; this acceptance supersedes the TimeControl visual approval status, but does not claim agent-operated tests or a recorded Desktop build. Date validity is a separate open model investigation in docs/DATE_VALIDITY.md.

## Localization standard

Use one layout for de-DE, en-US and ro-RO. Metadata captions belong in the shared model; report titles belong in Templates/Localization/labels.json and _ReportLabels measures. The Golden Sample uses a dynamic textbox header; Sales retains its text-measure card. The Golden Sample date slicer uses its approved native header with English fallback; other slicer captions use native visual titles. The Golden Sample header follows the 48 px container rule below; Sales migration is separate. The theme palette is unchanged. Validate the 536 px TimeControl selector with Tag/Woche/Monat/Quartal/Jahr and Zi/Săptămână/Lună/Trimestru/An as well as English; do not shrink fonts or duplicate pages to accommodate a language.

Missing translations fall back to approved English text. Native navigation currently retains English pending the documented host integration; alt text uses shared localized measures; model translations alone cannot translate them. See docs/LOCALIZATION.md for the support assessment, embed contract and release checklist. Presentation label cards are headers, not KPI fillers.

### Header and caption regression correction (1.5.1)

The Golden Sample title is a native dynamic textbox at x20/y16/w600/h48, at 20 pt Segoe UI Semibold. The earlier card-based implementation still clipped in the user's Desktop rendering and is superseded. Keep one left-aligned paragraph with one dynamic text run; `objects.general[].properties.paragraphs` is an array, and the run's value selector references `objects.values` evaluating `_ReportLabels[HeaderReceivablesOverview]`. Preserve 20pt in the textStyle; do not replace it with 20px. Do not add empty paragraphs, list indentation, or card layout objects. Keep 4 px top/bottom container padding and 0 px horizontal padding, with transparent background and no border. This is a header-only geometry exception to the usual 24 px margin. Do not use negative padding or overflow, and do not reduce the title font size.

Reserve at least 40 px usable height for a single 20 pt title line (48 px including padding). Measure the longest supported translation in the actual font. Do not enable a second line inside this single-line slot: a future longer title needs an explicitly reviewed larger header/layout variant. The title ends at y64; every filter/body component starts at or below y72, leaving at least 8 px clear space. Navigation is x648/y16/w608/h40 in the same header band. The 16 px gutters between body rows, approved TimeControl geometry and all KPI/chart/table rectangles remain unchanged. Never fix clipping by extending a visual over the next row.

For KPI cards, retain label-above-value, 10 pt caption and 28 pt value. Clear redundant internal card/callout padding; outer padding remains 12 px vertical and 16 px horizontal, with 4 px between label and value. Use the localized caption parameter below rather than a raw technical name. Summary columns retain 400/190/190/190/190 px widths with automatic resizing disabled, so longer translated headings cannot push columns outside the table.

The Golden Sample uses the hidden shared `_VisualCaptions` field parameter for its four KPI captions and five summary columns. It supplies translated business captions from `Templates/Localization/metadata.json` without changing business expressions or identifiers. `visual-captions.json` maps stable numeric Order to each original field. Saved projections carry English business captions; Power BI resolves the parameter caption for the host-selected locale. Each KPI has a fixed hidden Order filter; the table resolves all five fields in their defined order. These are caption bindings, not selectable business metrics. Do not remove these bindings or replace them with technical field names. Do not freeze parameter-resolved captions with independent custom card-label text.

The host sets `_VisualCaptions[Locale]` together with `Time Granularity[Locale]` and the matching embed locale. Metadata translations remain necessary for model authoring and other visuals; they are insufficient evidence that Desktop captions are safe. English fallback must be supplied by the catalog before generation. Native navigation still uses its documented English fallback; do not claim translated navigation until host integration is verified.

See `docs/GOLDEN_SAMPLE_LOCALIZATION_VALIDATION.md` for the three-locale static checks and outstanding runtime checks. Passing text measurements is not Power BI rendering approval.


### Date input restoration and runtime gate (1.5.2)

The Golden Sample date slicer retains x232/y72/w280/h56. Restore its native slicer header and hide the added visual-container title; preserve Between mode, Date[Date], slider hidden and all existing interactions. Set `objects.general.responsive=false` explicitly so the date inputs do not turn into a filter icon. The native header currently uses the catalog's English `Date range` fallback. Do not assume the container-title measure expression can be moved to the native header without a Desktop test; complete native-header localization is pending. Display by and the remaining TimeControl geometry are unchanged.

The user rejected the previous card-header correction after rendering. Static schema and font tests did not detect its runtime clipping. The replacement textbox and restored slicer are **pending Desktop verification**, not approved components. Review `docs/HEADER_DATE_SLICER_REPAIR.md` before generation or release.
