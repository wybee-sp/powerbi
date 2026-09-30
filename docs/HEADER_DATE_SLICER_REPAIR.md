# Header and date-slicer repair — 2026-09-30

**Status: PBIR correction prepared; Power BI Desktop rendering verification is still required.**

The user rendered commit `84b945a` and supplied a screenshot showing a clipped title and a date slicer reduced to a filter icon. This supersedes any expectation that the preceding schema/font checks established a working layout. No new rendering success is claimed here.

## Actual definition inspected

Title visual `3a5ca5c0fdc8424c93f4` was a `cardVisual`, not a textbox. Its outer height was already 48 px, and its card value font was 20 pt. There were no paragraph/text-run properties to adjust. Increasing the card's nominal height again would exceed the permitted band or repeat an unsuccessful approach. The screenshot establishes clipping; it does not establish which undocumented card-internal sizing rule caused it.

The title is restored as a native `textbox`, retaining its visual ID and localized measure. It has exactly one left-aligned paragraph and one dynamic text run at **20pt Segoe UI Semibold**, with no list indentation or blank paragraph. The run references a matching `objects.values` selector; that value queries `_ReportLabels[HeaderReceivablesOverview]`. The native dynamic-textbox structure follows [Microsoft's authoring example](https://github.com/microsoft/skills-for-fabric/blob/main/skills/powerbi-report-authoring/references/textbox.md). Card Data queries and card-specific layout/formatting objects are removed.

The textbox has 4 px top/bottom padding, 0 px horizontal padding, transparent background, and no border. There is no negative padding or overflow setting. The calculated font line budget is approximately 35.75 px within 40 px usable height; this is only a preparatory check, not proof of Desktop rendering.

## Geometry before and after

Coordinates come from the checked-in PBIR immediately before this repair, not estimates from the screenshot.

| Visual | Old x | Old y | Old width | Old height | New x | New y | New width | New height |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Title | 24 | 16 | 608 | 48 | 20 | 16 | 600 | 48 |
| Navigation | 648 | 24 | 608 | 32 | 648 | 16 | 608 | 40 |
| Date range | 232 | 72 | 280 | 56 | 232 | 72 | 280 | 56 |

All primary filters remain **y72 → y72**. The title ends at y64, leaving 8 px before the filters. It ends horizontally at x620, leaving 28 px before navigation begins at x648. All KPI, chart, table, Branch, Customer and granularity rectangles remain unchanged. No title/filter/navigation bounds intersect.

## Date slicer

The localization diff replaced the approved native slicer header with a separate visual-container title while retaining a 280 × 56 px outer rectangle. This changed the space available to the date inputs. Responsive slicers can collapse to a filter icon when their usable area is too small; this is [documented Microsoft behavior](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-slicer-filter-responsive) and matches the user's screenshot.

This repair restores the native slicer header, hides the additional container title, and explicitly sets `objects.general.responsive=false`. Between mode, hidden slider, Date[Date] query, sorting, range filters, interactions and outer geometry are preserved. Display by is untouched.

The native header uses the approved catalogue's English **Date range** fallback. Moving a dynamic visual-title expression to the native header is not assumed to be supported. Native-header localization remains a documented limitation; the localized accessibility label remains bound. This avoids claiming an untested dynamic-header workaround while restoring the previously approved appearance.

## Verification and remaining gate

- Static PBIR/model-reference compatibility checks pass.
- The updated preparatory layout check validates the dynamic text-run selector, label-measure target, 20pt text style, actual outer rectangles, header/filter separation and nonresponsive native date header.
- No model, source, business calculation, relationship, Sales, Purchases or Inventory files change.
- **Desktop render: not performed.** Windows app inspection found the remote-desktop session, but automatic approval rejected access with `Computer Use was not approved to use Remote Desktop Connection`. The session was not operated and this repository was not transferred to it.

Required before calling this fixed: open the changed Golden Sample in Desktop, refresh/reload external definitions, and confirm the whole title including descenders is visible, navigation does not overlap it, and both editable date inputs are visible and functional. Check the current Desktop build at actual page size, then the supported locales. Keep the correction pending if any glyph, input or navigation control is clipped. Schema validation and font-budget checks do not satisfy this gate.

## Changed files

- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/3a5ca5c0fdc8424c93f4/visual.json`
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/d8f5a9bed09924c8f6f5/visual.json`
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/5ddcb2a5d4d5d4b8fc09/visual.json`
- `Templates/TopEvoAnalytics.Report/COMPONENTS.json`
- `Templates/Localization/report-bindings.json`
- `Templates/Theme/DESIGN_SYSTEM.md`
- `Templates/Theme/CHANGELOG.md`
- `AGENTS.md`
- `tools/localization/validate_golden_layout.py`
- `docs/LOCALIZATION.md`
- `docs/GOLDEN_SAMPLE_LOCALIZATION_VALIDATION.md`
- `docs/HEADER_DATE_SLICER_REPAIR.md` (new)
