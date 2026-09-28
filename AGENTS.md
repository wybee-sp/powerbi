# TopEvo analytics authoring rules

## Architecture

- `Templates/TopEvoAnalytics.SemanticModel` is the single shared semantic-model source. All module and generated reports must reference it. Do not create semantic models inside reports.
- Use relative `datasetReference.byPath` references for local PBIP development. Deployment bindings belong in documented deployment configuration.
- `Templates/TopEvoAnalytics.Report` is the permanent Golden Sample and component reference report. It is not a customer report and must be excluded from customer deployment.
- Customer reports are overrides under `Customers/<customer-id>/overrides/`; they must not modify standard templates or fork the canonical model.

## Design system and generation

- Read `Templates/Theme/DESIGN_SYSTEM.md` before creating or styling pages. Use canonical `Templates/Theme/TopEvo.json`; record foundation changes in `Templates/Theme/CHANGELOG.md`.
- Every generated page must use the shared model, canonical theme, 1280 x 720 TopEvo grid, approved Golden Sample components and business measures from `_Measures`.
- Primary bar order is mandatory: Branch -> TimeControl -> business-specific filters. TimeControl is the reusable date-range plus granularity component defined in DESIGN_SYSTEM.md; all five grains must be visible without selector scrolling/overflow and the selected grain must remain highlighted. Branch is always leftmost. Time control combines adjacent date-range inputs and visible Day/Week/Month/Quarter/Year single-select buttons on one shared surface; it may span two slots. Granularity is a presentation control inside this group, never a separate business-filter slot. Date range determines WHAT period is analyzed; granularity determines HOW it is grouped. Examples: Sales/Receivables: Branch -> Invoice-date Time control -> Customer; Purchases: Branch -> Purchase-date Time control -> Supplier; Inventory: Branch -> Date Time control -> Warehouse. Keyboard order follows Branch, date range, granularity, business filters. Exceptions require a documented business requirement in the affected report documentation.
- The current Golden Sample TimeControl is the user-accepted rendered visual standard. Preserve its layout and component members as recorded in COMPONENTS.json; date-quality investigations do not authorize layout changes. See docs/DATE_VALIDITY.md: identify source fields and rows before changing date transformations; preserve source records and audit invalid dates instead of silently discarding them.
- Standard pages use 24 px margins, 16 px gutters and documented slots. Tooltip/mobile layouts need a documented variant.
- Components must be implemented, rendered and approved in the Golden Sample before generation. An empty report or written specification is not an approved visual template.
- Prefer native visuals. Specify business titles, units, empty states, tab order, alternative text and interactions. Never communicate status by color alone.
- The ERP host owns global navigation and authorized company context. Reports own analytical page navigation and filters. Filters and hidden objects are not security boundaries.
- Theme JSON supplies formatting defaults; PBIR supplies geometry, bindings and interactions. Keep generator manifests outside schema-controlled Power BI JSON.
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
- Cloned pages/components need appropriate new IDs within the target report. Update page order, bookmarks, navigation, interactions and dependencies together.
- Use property names from the pinned schema and Desktop-exported PBIR. Do not invent properties or bulk-upgrade schema versions.
- Record the validated Desktop build in the design system. Static schema success does not prove rendering works.
- Clear incidental saved customer/demo selections; retain only documented intentional defaults.

## Data and configuration

- Never commit customer data, CSV/XML exports, PBIX files, `.pbi` caches, credentials or machine-specific source paths. Keep local data/configuration ignored by Git.
- Use synthetic examples and screenshots. No customer names or selections in reusable templates.
- Customer deployment must document tenant isolation or RLS and test effective identity; report filters cannot replace authorization.
- Existing violations are migration work, not permission to repeat them. Fix only within the requested scope and do not claim full compliance prematurely.

## Validation and completion

- Inspect the working tree and preserve unrelated changes. Honor requested file/domain boundaries.
- Validate themes against the documented Microsoft schema. For changed PBIR, check schemas, model paths, resources, bindings, page order, identities, bounds and dependencies.
- For model changes, validate refresh, keys, filter propagation, totals, dates and monetary precision with approved synthetic/local data.
- For report changes, open/save in the supported Desktop build and review renders. Test embedded sizing, long labels, empty states, filters, reset, drillthrough, keyboard navigation and contrast before component approval.
- Verify deployment excludes the Golden Sample and uses the intended shared model.
- Report exact changed files, checks and limitations. Do not claim Desktop/embedded validation when only static checks ran.
