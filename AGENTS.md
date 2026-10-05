# TopEvo analytics authoring rules

## Architecture

- `Templates/TopEvoAnalytics.SemanticModel` is the single shared semantic-model source. All module and generated reports must reference it. Do not create semantic models inside reports.
- Use relative `datasetReference.byPath` references for local PBIP development. Deployment bindings belong in documented deployment configuration.
- `Templates/TopEvoAnalytics.Report` is the permanent Golden Sample and component reference report. It is not a customer report and must be excluded from customer deployment.
- Customer reports are overrides under `Customers/<customer-id>/overrides/`; they must not modify standard templates or fork the canonical model.

## Canonical template sources and responsibilities

| Source | Responsibility |
| --- | --- |
| `Templates/TopEvoAnalytics.SemanticModel` | Shared business calculations, translations, Date logic and relationships |
| `Templates/Theme/TopEvo.json` | Supported visual formatting defaults |
| `Templates/Theme/DESIGN_SYSTEM.md` | Design, layout and component rules |
| `Templates/TopEvoAnalytics.Report` | Golden Sample and rendered, verified component reference; only approved components may be propagated |
| `Templates/PageTemplates/*.layout.json` | Shared geometry and possible component slots, independent of module business bindings |
| `<module>/*.bindings.json` | Module-specific fields, measures, label catalogue references and component bindings |
| Generated PBIR report/page files | Power BI implementation artifacts produced from the canonical inputs |

- PBIR has no runtime parent-layout inheritance. Never insert unsupported `$ref`, `extends` or similar inheritance properties into PBIR; legitimate schema-defined properties such as `$schema` remain valid.
- TopEvo inheritance happens at repository/generation level: `Design System + Page Layout + Module Bindings + Semantic Model -> Generator -> PBIR`, using the canonical theme and approved Golden Sample components.
- Represent reusable layout rules centrally instead of manually duplicating them across reports. Keep reusable business logic in the shared model, never in layout files, binding files or report-local calculations.
- These paths define the architecture contract; they do not imply that page templates or a generator already exist. Implement or migrate them only within an explicitly requested task.

## STANDARD/CUSTOM classification and synchronization

- Classify reports and pages in external generator metadata as `STANDARD` (generated/synchronized from TopEvo templates) or `CUSTOM` (customer-specific override). Never infer permission to overwrite an artifact from its directory alone; an unclassified artifact is not eligible for automatic synchronization.
- Central template changes, such as an update to `overview.layout.json`, must be propagatable through the generator to eligible STANDARD artifacts. Synchronize shared geometry and component implementation while preserving module-specific bindings and existing target identities.
- Never automatically overwrite CUSTOM artifacts, including CUSTOM pages within an otherwise STANDARD report. Keep customer overrides clearly separated under `Customers/<customer-id>/overrides/`; do not propagate central changes blindly into them.
- Keep classification, template versions, provenance and generation mappings outside Power BI schema-controlled JSON unless the schema explicitly supports that metadata. Do not implement repository inheritance through invented PBIR properties.

## Design system and generation

- Read `Templates/Theme/DESIGN_SYSTEM.md` before creating or styling pages. Use canonical `Templates/Theme/TopEvo.json`; record foundation changes in `Templates/Theme/CHANGELOG.md`.
- Every generated page must use the shared model, canonical theme, 1280 x 720 TopEvo grid, approved Golden Sample components and business measures from `_Measures`.
- STANDARD analytical Overview pages use the 1280 x 720 canvas, approved Golden Sample geometry and canonical Date dimension only. Their primary bar is Branch -> TimeControl -> business-specific filters; TimeControl combines Date range with all five visible Day/Week/Month/Quarter/Year options.
- Primary bar order is mandatory: Branch -> TimeControl -> business-specific filters. TimeControl is the reusable date-range plus granularity component defined in DESIGN_SYSTEM.md; all five grains must be visible without selector scrolling/overflow and the selected grain must remain highlighted. Branch is always leftmost. Time control combines adjacent date-range inputs and visible Day/Week/Month/Quarter/Year single-select buttons on one shared surface; it may span two slots. Granularity is a presentation control inside this group, never a separate business-filter slot. Date range determines WHAT period is analyzed; granularity determines HOW it is grouped. Examples: Sales/Receivables: Branch -> Invoice-date Time control -> Customer; Purchases: Branch -> Purchase-date Time control -> Supplier; Inventory: Branch -> Date Time control -> Warehouse. Keyboard order follows Branch, date range, granularity, business filters. Exceptions require a documented business requirement in the affected report documentation.
- The current Golden Sample TimeControl is the user-accepted rendered visual standard. Preserve its layout and component members as recorded in COMPONENTS.json; date-quality investigations do not authorize layout changes. See docs/DATE_VALIDITY.md: identify source fields and rows before changing date transformations; preserve source records and audit invalid dates instead of silently discarding them.
- Render only KPIs backed by existing, validated semantic-model measures. Never create empty cards, Not available/N/A text, placeholders or invented KPIs to fill slots. Adapt the row to available measures: 1 full-width card where appropriate; 2, 3 or 4 equal-width cards with 16 px gutters (1232, 608, 400 or 296 px on the standard canvas). With zero suitable measures, omit the KPI row. More than four requires an explicit page-design decision; never automatically add a row. Document missing measures outside the canvas.
- Layout slots describe possible components, not mandatory placeholders. Apply the same rule to other optional components: omit unsupported components and use the template's documented layout variant; never fabricate data, labels or business definitions to fill space. Distinguish an unavailable component binding from a valid component showing an empty result for the selected period.
- Standard pages use 24 px margins, 16 px gutters and documented slots. Tooltip/mobile layouts need a documented variant.
- Components must be implemented, rendered and approved in the Golden Sample before generation. An empty report or written specification is not an approved visual template.
- Prefer native visuals. Specify business titles, units, empty states, tab order, alternative text and interactions. Never communicate status by color alone.
- The ERP host owns global navigation and authorized company context. Reports own analytical page navigation and filters. Filters and hidden objects are not security boundaries.
- Theme JSON supplies formatting defaults; layouts and module bindings are the generation inputs; PBIR encodes the resulting geometry, bindings and interactions. Keep generator manifests outside schema-controlled Power BI JSON.
- Report-local theme resources are synchronized copies of the canonical theme. Do not independently edit them or overwrite Microsoft base themes.

## Model rules

- New or migrated business measures belong in `_Measures`, with descriptions, format strings and domain display folders. Hide its placeholder column.
- Do not duplicate business calculations in visuals. Update report bindings when moving/renaming measures; preserve lineage where appropriate.
- Keep staging queries unloaded and technical fields hidden. Expose curated business fields; import only required attributes, not entire ERP configuration tables.
- Define table grain and validate key uniqueness across company/branch scope. Document inactive relationships and filtering exceptions.
- Use an explicit shared Date dimension and documented date roles. Do not generate automatic date-hierarchy dependencies.
- `Date` is the only canonical calendar. Follow `docs/MODEL.md`: daily unique `Date[Date]`, explicit sorted calendar fields, ISO weeks, and range coverage extended when new fact-date fields are added. Do not create InvoiceDate, DueDate, PaymentDate or report-specific calendar tables at this stage.
- Keep Auto Date/Time disabled. Use `Date[YearMonth]` for monthly trends and `Date[Date]` for shared date slicers. The default active role is invoice-header date; alternate roles stay inactive unless a separately explained shared-model measure deliberately changes date propagation. Do not introduce ambiguous active paths.
- Use the shared disconnected `Time Granularity` field parameter for switchable trends (Day, Week, Month, Quarter, Year); keep date-range selection on `Date[Date]`. Do not duplicate charts/calendars or use report calculations for grouping. Bind `Calendar Week` Year to `Date[ISOYear]` so ISO weeks do not split at calendar-year boundaries.
- Identifiers/status codes must not sum. Unit prices, rates and percentages require explicit aggregation rules.
- Define parsing locale, precision, currency, cancellations and credit notes. Do not silently reinterpret ambiguous values or treat missing data as zero.
- Styling does not authorize calculation, relationship or source-transformation changes. Make these separately scoped and validated changes.

## PBIR identity and compatibility

- Preserve IDs when editing existing artifacts. New reports need distinct `.platform` logical IDs and meaningful names; do not copy another report's identity.
- Generate unique IDs for new PBIR objects in their required identity scope. Never copy Golden Sample visual IDs into generated pages. Preserve existing target IDs during synchronization; update page order, bookmarks, navigation, interactions and dependencies together.
- Use property names from the pinned schema and Desktop-exported PBIR. Do not invent properties or bulk-upgrade schema versions.
- Record the validated Desktop build in the design system. Static schema success does not prove rendering works.
- Clear incidental saved customer/demo selections; retain only documented intentional defaults.

## Data and configuration

- Never commit customer data, CSV/XML exports, PBIX files, `.pbi` caches, credentials or machine-specific source paths. Keep local data/configuration outside Git according to `.gitignore`; check that ignored data has not already been tracked. Customer-specific report definitions remain separate from standard templates and must not embed customer data.
- Use synthetic examples and screenshots. No customer names or selections in reusable templates.
- Customer deployment must document tenant isolation or RLS and test effective identity; report filters cannot replace authorization.
- Existing violations are migration work, not permission to repeat them. Fix only within the requested scope and do not claim full compliance prematurely.

## Validation and completion

- Inspect the working tree and preserve unrelated changes. Honor requested file/domain boundaries.
- Validate themes against the documented Microsoft schema. For changed PBIR, check schemas, model paths, resources, bindings, page order, identities, bounds and dependencies.
- Before accepting generated reports, validate PBIR/TMDL syntax and schemas; ID uniqueness; model bindings and missing measures/columns; canvas bounds and component overlaps; TopEvo grid/layout and Branch -> TimeControl -> business-filter ordering; localization compatibility; theme/design-system compliance; and STANDARD/CUSTOM protection. Verify that synchronization preserves module bindings and leaves CUSTOM artifacts untouched.
- For model changes, validate refresh, keys, filter propagation, totals, dates and monetary precision with approved synthetic/local data.
- For report changes, open/save in the supported Desktop build and review renders. Test embedded sizing, long labels, empty states, filters, reset, drillthrough, keyboard navigation and contrast before component approval.
- Verify deployment excludes the Golden Sample and uses the intended shared model.
- Report exact changed files, checks and limitations. Do not claim Desktop/embedded validation when only static checks ran.

## Localization

- One report/page definition per business module; never create copies per language. Follow docs/LOCALIZATION.md and the canonical Templates/Localization catalogues for de-DE, en-US and ro-RO.
- Keep layout definitions language-neutral; module bindings reference the existing translation/label architecture rather than embedding language-specific layouts. Components must accommodate all supported localized text lengths without clipping or overlap. Important template changes require Power BI Desktop rendering verification; static validation is not proof of correct rendering.
- Preserve internal identifiers, lineage, business expressions and source parsing locale. Use TMDL culture translations for curated metadata and _ReportLabels measures for presentation text. Do not remove business caption fallbacks without a verified localized replacement. In Golden Sample KPI/table bindings, preserve the shared _VisualCaptions field parameter and its generated English initial captions; metadata translation alone does not guarantee safe Desktop captions.
- English is the mandatory fallback; missing English entries fail generation. Never expose translation keys or technical ERP names as fallback. Add catalogue entries before exposing new business fields.
- Angular owns language selection. Pass matching embed language/formatLocale, Time Granularity.Locale and (for caption-parameter consumers) _VisualCaptions.Locale filters; no report language selector. Keep grain selection on stable numeric Order and date filtering independent.
- Native navigation and business-data descriptions require the documented separate mechanisms. Bind accessibility text to shared label measures. Do not invent unsupported PBIR translation properties or claim locale translates ERP values. Preserve approved geometry; render every supported locale before release.

## Localized header and visual captions

- Follow the DESIGN_SYSTEM.md header rule: Golden Sample dynamic textbox title x20/y16/w600/h48, unchanged 20 pt text run and 4 px vertical container padding; one left-aligned paragraph, no card layout objects. The header ends at y64; primary filters start at y72. This header-only top-margin exception preserves the approved body layout. Never shrink text or overlap the next component to conceal clipping.
- End-user KPI/table captions must come from approved business translations, never technical ERP names. Preserve internal fields and measures; use the shared presentation parameter `_VisualCaptions` for the Golden Sample, generated from metadata.json and visual-captions.json. Keep fixed KPI Order filters and table column order. No report-local business measures, translated model-object renames or unsupported dynamic displayName expressions.
- Validate all three locale dictionaries, caption targets, geometry and text fit. Record actual Desktop/embedded rendering separately; font measurements and schema validation do not establish runtime fit or translation behavior. Do not propagate unrendered component changes as approved.

- Golden Sample date slicer stays x232/y72/w280/h56 with native header, Between mode, hidden slider and responsive=false. Its native header currently uses the English catalogue fallback; do not reintroduce the extra container title or claim full header localization/render approval. See docs/HEADER_DATE_SLICER_REPAIR.md.
