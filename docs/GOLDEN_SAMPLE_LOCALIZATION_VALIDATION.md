# Golden Sample localization correction — 2026-09-30

Status: implemented and statically checked; Desktop/embedded rendering remains pending. This correction is not a new visual approval.

## Causes and correction

- The header had been converted from a textbox to a card inside a 608 × 32 px rectangle. A 20 pt Segoe UI Semibold line has approximately 35.75 px ascent plus descent at 96 DPI, before padding. The previous rectangle was insufficient, and implicit card insets further reduced usable space.
- The title now occupies x24/y16/w608/h48 with 4 px vertical padding and zero internal card/callout/layout padding. Its content height is 40 px. Font size stays 20 pt. The transparent header-only container exception accommodates the font without moving any body component. The header ends at y64; filters start at y72.
- Removing all local business captions made Desktop display raw technical names. The Golden Sample now resolves KPI/table captions through a shared presentation field parameter. The original fields/measures and numeric formatting remain in place; the parameter supplies the caption for the selected locale. English business captions are stored as the initial resolved state.
- Table columns retain explicit 400/190/190/190/190 px widths with auto-size disabled. Four KPI cards retain their approved rectangles, labels and values, with redundant inner padding removed.

## Static evidence

Microsoft TOM 19.117.0 deserializes the model. Validation checks the existing cultures and all 15 new caption rows against the metadata catalog, parameter bindings, original KPI measure selections, locale filter defaults and PBIR schema compatibility. Report declarations remain unchanged; the published visual 2.9 compatibility schema is used because the declared 2.12 schema is unavailable in the cached validation baseline.

Text measurements use the actual installed Segoe UI and Segoe UI Semibold fonts, at fourfold resolution, with a 10% horizontal reserve. These are font-budget checks, not screenshots. They do not measure Power BI's internal chrome, selection buttons or native rendering engine.

| Check | en-US | de-DE | ro-RO |
| --- | --- | --- | --- |
| Title width in 608 px | 368.9 px | 362.2 px | 339.7 px |
| Title line height in 40 px usable area | 35.75 px | 35.75 px | 35.75 px |
| Filter-label text budget | Pass | Pass | Pass |
| Widest KPI caption in 264 px | 89.8 px | 128.7 px | 99.2 px |
| Five table headings in fixed columns | Pass | Pass | Pass |
| Native navigation English fallback, `Overview` | Fits | Fits | Fits |
| All five translated TimeControl labels in 536 px | Pass | Pass | Pass |
| Actual Power BI render and locale switching | Pending | Pending | Pending |

All 13 visual rectangles remain inside 1280 × 720 with no intersections. Header/body clearance is checked. All body positions, visual IDs/types, interactions, shared-model reference, theme, original business model files and relationships are preserved. No Sales, Purchases or Inventory files are changed.

Run:

```powershell
./tools/localization/Validate-Localization.ps1 -TomLibraryPath <TOM-directory> -SchemaDirectory <schema-directory>
python ./tools/localization/validate_golden_layout.py --font-directory <Segoe-UI-font-directory>
```

The Python check requires Pillow. The PowerShell check requires the same pinned Microsoft TOM runtime and report/visual schema bundles documented in LOCALIZATION.md. No fonts, binaries or machine paths are stored in Git.

## Required runtime acceptance

No local Power BI Desktop app was found in the Windows app inventory or standard executable location. The user's earlier screenshot comes from a remote desktop session; the modified local repository was not opened or rendered there. No Desktop build, model refresh, DAX execution or embedded session is claimed for this correction.

For each locale, use matching embed language/formatLocale and both hidden report filters (`Time Granularity.Locale` and `_VisualCaptions.Locale`). Confirm title measures use the same locale. Open/refresh in the supported Desktop build and test a real embedded session:

1. Title is fully visible at actual size, with clear separation from filters; inspect German/Romanian diacritics.
2. Branch, date range, Display by and Customer captions fit; both date inputs remain usable.
3. Four KPIs show the localized business captions and original measure values. No technical names, duplicate cards or clipped captions.
4. Table has exactly five columns in the same order, localized headings, preserved widths, correct totals and no unwanted horizontal overflow.
5. Native navigation remains the documented English fallback; verify fit. Translating page navigation still requires the separate host integration. Do not mistake this for completed multilingual navigation.
6. All five TimeControl options fit with no overflow arrow; selected-state highlight works in every locale. Test all grains, unchanged date selection and totals.
7. Reset/bookmark/re-embed retains matching locale filters and fixed KPI Order filters. Verify caption-parameter expansion after locale changes, including returning to English.

If any runtime check fails, retain the component's pending status. Do not compensate with smaller title fonts, renamed business fields, report-local calculations or language-specific pages.

## Exact file inventory

Created:

- `Templates/Localization/visual-captions.json`
- `Templates/TopEvoAnalytics.SemanticModel/definition/tables/_VisualCaptions.tmdl`
- `tools/localization/validate_golden_layout.py`
- `docs/GOLDEN_SAMPLE_LOCALIZATION_VALIDATION.md`

Changed:

- `AGENTS.md`
- `Templates/Theme/DESIGN_SYSTEM.md`
- `Templates/Theme/CHANGELOG.md`
- `Templates/TopEvoAnalytics.Report/COMPONENTS.json`
- `Templates/TopEvoAnalytics.Report/definition/report.json`
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/3a5ca5c0fdc8424c93f4/visual.json` — header
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/153e904422493224e572/visual.json` — invoice KPI
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/a267601474d5703ee78e/visual.json` — open-invoice KPI
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/44bde52db62b1cce7f88/visual.json` — closed-invoice KPI
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/369387969e38ec6613f3/visual.json` — payment KPI
- `Templates/TopEvoAnalytics.Report/definition/pages/ReportSection/visuals/8fcfab21f72e5ed59047/visual.json` — summary table
- `Templates/TopEvoAnalytics.SemanticModel/definition/model.tmdl`
- `tools/localization/Build-Localization.ps1`
- `tools/localization/Validate-Localization.ps1`
- `docs/LOCALIZATION.md`
- `docs/MODEL.md`
