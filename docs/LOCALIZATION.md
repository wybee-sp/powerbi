# TopEvo localization architecture

## Support assessment before implementation

The repository saves PBIR report schema 3.3.0, page schema 2.1.0 and visual-container schema 2.12.0. These are file-format versions, not a Power BI Desktop product build. Theme validation uses schema 2.150. The exact Desktop build that last saved these reports is not recorded and no installed Desktop build was discovered in the standard location. Do not infer a supported Desktop build from theme import version metadata. Native TMDL cultures are supported by the Microsoft TOM 19.117.0 serializer used for validation. Visual schema 2.12 is unavailable at its published URL; static compatibility validation uses published 2.9 without changing file declarations.

Microsoft supports translated model Caption, Description and DisplayFolder properties. Report-layout literal text and native page names are not model metadata and do not automatically translate. A supported alternative for visual titles is a string measure evaluated with USERCULTURE(). These limitations were identified before binding report label measures. No language-specific reports/pages or business calculations are introduced.

## Five separate language concerns

| Concern | Owner | Implementation |
| --- | --- | --- |
| ERP UI language | Angular | Normalize to de-DE, en-US or ro-RO; otherwise en-US |
| Power BI locale | Embed configuration | settings.localeSettings.language and formatLocale; re-embed on change |
| Semantic-model metadata | Shared model | Culture captions/descriptions in cultures/*.tmdl; stable internal identifiers |
| Report-owned UI text | Shared label catalogue and report bindings | Hidden _ReportLabels measures evaluate USERCULTURE; field-value visual titles and text-measure header cards |
| Multilingual business data | ERP exports plus shared model | Requires actual translated source data; not provided by metadata captions |

The model culture en-US and sourceQueryCulture de-DE are unchanged. Source parsing locale is not the viewer language. Currency remains the existing business currency; changing locale is not currency conversion.

## Canonical sources and generation

- Templates/Localization/metadata.json: business-facing object captions in all three locales, plus descriptions for Sales measure semantics and the Date table. All seven existing business measures, all ten existing table captions, the currently exposed Date fields/hierarchies and curated business columns are covered. Raw configuration fields, hidden keys and uncurated ERP columns are not blanket-translated; do not expose them in generated reports without approved English captions and catalogue entries. Translations must not invent meanings for technical source fields.
- Templates/Localization/labels.json: report/UI messages, supported locales and required English fallback. Includes Sales/Receivables headings, filter labels, five grains, chart/table titles, navigation labels and a future no-data label. The no-data message is available but no new empty-state overlay is added.
- Templates/Localization/text-inventory.json: before-change inventory of user-facing literals in both reports with file/JSON-pointer provenance and classification, followed by metadata entries and business-data examples. No literal tooltip or axis-title messages beyond those recorded were found; many axes have titles hidden. Customer/branch names and calculated English calendar names are data, not UI captions.
- Templates/Localization/report-bindings.json: current shared-label measure bindings.
- Templates/Localization/navigation.json: stable report/page IDs to navigation message keys for future Angular integration.
- tools/localization/Build-Localization.ps1: generate cultures, label measures and localized parameter rows using Microsoft TOM. Run from any directory with `-TomLibraryPath <directory containing the TOM DLLs>`. No machine-specific library path is stored. Existing lineage and business expressions are preserved.

For each configured metadata/message key, missing German/Romanian text uses the English entry during generation. Missing English is a build error; never display a key or an ERP identifier as fallback. Native Power BI metadata fallback is not a substitute for this build rule: complete en-US/de-DE/ro-RO entries are emitted for the curated surface. Unsupported requested locales are normalized to en-US by the host, and label measures independently default to English. Legacy technical model names remain unchanged.

## Report bindings in Golden Sample and Sales

- Headers now use an existing native cardVisual pattern with a text measure, replacing literal textbox contents in the same rectangle and with the same visual ID. These are presentation labels, not new business KPIs.
- Charts and table titles use field-value expressions referring to _ReportLabels measures.
- Slicer captions use the same native visual-title mechanism; literal slicer headers are disabled. Rectangle geometry, grid positions, data bindings, single-selection behavior and interactions are preserved. Title/header spacing and clipping must be rendered in all three languages before approval.
- KPI labels and table column headings defer to model captions. Local displayName/nativeQueryRef overrides and KPI custom label text were removed so they do not mask translations. Default total captions are left to the native locale-aware visual.
- Default tooltips inherit translated field captions and original business values; they do not translate customer names.
- The shared Date columns keep existing values and formats. Month/weekday row strings generated in English remain English if explicitly used; the approved trend uses date/year-qualified period keys, so it does not depend on those names.

## TimeControl presentation data

Time Granularity now has 15 static presentation rows: five per locale. Stable Fields NAMEOF targets and numeric Order (0..4) are unchanged. Locale is a new hidden selector column, with no relationship to any fact or Date table. This is not a new date table or business calculation. Imported calculated rows never use USERCULTURE(), because calculated tables are refresh-time objects rather than per-viewer evaluations.

Both reports save a hidden report filter Time Granularity[Locale] = en-US. Angular replaces that filter at load. The saved Month selection filters Order=2 instead of the English word Month, so it works for all three languages. Exactly five rows must remain after the host filter. Do not clear that filter, save all locales in bookmarks or provide a report language slicer. Month=2 is a stable initial state; other user grain selections can be preserved by numeric Order across re-embedding. The date-range slicer remains independent.

## Angular embed contract (integration not implemented here)

Use a current supported powerbi-client SDK and the documented settings.localeSettings contract:

```typescript
const supported = ["de-DE", "en-US", "ro-RO"];
const locale = supported.includes(erpUiLanguage) ? erpUiLanguage : "en-US";
const localeFilter = {
  $schema: "http://powerbi.com/product/schema#basic",
  target: { table: "Time Granularity", column: "Locale" },
  operator: "In",
  values: [locale],
  filterType: models.FilterType.Basic,
  requireSingleSelection: true
};
const config = {
  type: "report",
  id: reportId,
  embedUrl,
  accessToken: embedToken,
  tokenType: models.TokenType.Embed,
  settings: {
    localeSettings: { language: locale, formatLocale: locale },
    panes: { pageNavigation: { visible: false } }
  }
};
// Phased embedding: apply the hidden data-language filter before first render.
const report = powerbi.load(container, config);
report.on("loaded", async () => {
  await report.updateFilters(models.FiltersOperations.Replace, [localeFilter]);
  await report.render();
});
```

Replace only the locale target; do not replace the entire filter collection or tenant/security context. Await failures and show a host error rather than rendering 15 options. When ERP language changes, preserve allowed analytical state, call powerbi.reset(container), then load again with matching locale settings and locale filter. Reapply the locale filter after reset/bookmark operations. Do not rely on updateSettings to switch language on an existing iframe. Validate USERCULTURE output under the actual embedding authentication mode; a locale-filter change alone does not change model culture or labels.

No Angular or Caché source code was modified. The example is a contract requiring SDK/service verification in the target application.

## Native navigation limitation and accessibility

Native page display names and pageNavigator captions do not have model-translation storage. They retain their current English fallback in these files. Hiding the embed page-navigation pane does NOT hide the on-canvas pageNavigator. Proposed production solution: Angular owns translated page navigation using navigation.json and report.setPage(stablePageId), and the on-canvas navigator is suppressed through a separately validated embed custom-layout configuration, or replaced with approved measure-caption buttons in a future component change. No unsupported page-name expression or guessed custom-layout property is inserted here. Complete multilingual navigation therefore remains an integration item; do not claim that locale alone completes it.

Accessibility altText uses shared label-measure expressions, following Microsoft’s documented dynamic-alt-text mechanism. Screen-reader behavior still requires validation in the supported Desktop/embedded build. Native navigation remains the outstanding UI integration limitation and does not justify language copies of reports.

## Multilingual ERP business-data pattern

No translated article-description columns are currently present; do not fabricate them. When ERP supplies them, retain stable business keys and load actual locale-tagged labels in a shared description dimension, or explicit language columns with a field parameter. Choose the requested label, then a supplied English label; if neither exists, use a localized neutral description such as “Description unavailable” with a data-quality record, not a translation key. Never translate identifiers or customer/branch proper names by metadata rules. Ensure one label per business key/locale and no fact-row multiplication. The host must apply the same normalized locale to that future selector. Existing relationships and source exports remain untouched in this task.

## Validation and release limits

Static TOM/PBIR checks verify cultures, stable metadata targets, label references, three sets of five grain rows, English fallbacks, model/report paths, and unchanged business calculations/relationships/geometry. Static schema acceptance cannot prove conditional-title rendering or metadata-language behavior. Exact Desktop build, DAX runtime evaluation and embedded three-locale checks remain unrecorded.

Before release, open/save with the supported Desktop build, then test embedded de-DE/en-US/ro-RO and an unsupported locale mapped to en-US. Check all five grains per locale, no overflow, unchanged date selection/totals, German/Romanian diacritics, title and KPI fit, column captions, tooltip captions, default totals, re-embedding and reset/bookmark behavior. Confirm that labels and metadata follow the locale settings while parameter rows follow the matching locale filter. Verify translations with a German/Romanian business reviewer. Desktop metadata preview may not match service behavior; the embedded test is required. Publish-to-web does not support this multilingual architecture.

Sources: [dynamic accessibility text](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports), [multilingual navigation](https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-page-navigation), [translation categories and limitations](https://learn.microsoft.com/en-us/power-bi/guidance/multiple-language-translation), [expression-based titles](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-format-visual-titles), [embed settings](https://learn.microsoft.com/en-us/javascript/api/overview/powerbi/configure-report-settings), [loading translated data](https://learn.microsoft.com/en-us/power-bi/guidance/data-translation-load-report-bookmark).

### Checks completed in this task

- Microsoft TOM deserialization passed; 83 caption/description/level translations per culture were verified against the catalogue.
- All 15 locale/grain rows and canonical Date targets, initial locale filters and numeric Month selections passed static checks.
- Expression-based labels, model references and report/visual schema compatibility passed.
- Re-running model localization generation produced identical output. An isolated generation test with missing Romanian label/caption entries correctly emitted the English fallbacks.
- Existing report identities, visual geometry, business/source model files, relationships, Purchases and Inventory were confirmed unchanged.
- No DAX evaluation, Desktop render or embedded-language execution is claimed.

Run tools/localization/Validate-Localization.ps1 with -TomLibraryPath and -SchemaDirectory pointing to the pinned TOM runtime and bundled Microsoft report/visual schemas. The schema directory currently expects topevo-report-bundle.json and topevo-visual-bundle.json. These external validation dependencies are not shipped as product assets.

See [LOCALIZATION_FILES.md](LOCALIZATION_FILES.md) for the exact created/modified file inventory.
