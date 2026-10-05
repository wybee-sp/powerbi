# TopEvo visual foundation changelog

## Generation workflow 1 - 2026-10-05

- Adds central Overview layout, Sales bindings and a read-only candidate plan with guarded synchronization. Geometry/component implementations remain based on the current Golden Sample.
- Adds STANDARD/CUSTOM ownership protection, stable target identities, adaptive optional components, static/TOM/schema validation and idempotence tests.
- Current template review remains PENDING; no live Sales PBIR or other report/model definitions were synchronized.

## Component specification 1.5.2 - 2026-09-30

- Replaces the still-clipped Golden Sample title card with a dynamic textbox at x20/y16/w600/h48, retaining 20 pt. Navigation moves to y16/h40; filters remain at y72.
- Restores the native date-slicer header and disables responsive icon collapse without changing TimeControl geometry, Date binding or range semantics. Native date caption currently uses English fallback.
- Records the user-rendered failure of 1.5.1. The new correction requires Desktop rendering verification; static validation is not acceptance.

## Component specification 1.5.1 - 2026-09-30

- Corrects Golden Sample header insets and reserves a 48 px title container without moving TimeControl or the body; title stays 20 pt.
- Adds presentation-only localized caption bindings for the existing four KPI measures and summary columns; preserves business definitions and internal identifiers.
- Fixes table column widths and removes redundant KPI card insets. Theme JSON, Sales, Purchases and Inventory are unchanged.
- Adds three-locale static layout/caption checks; Desktop/embedded rendering remains pending.

## Component specification 1.5.0 - 2026-09-28

- Requires adaptive 1/2/3/4-card KPI rows backed by existing validated measures; no empty cards, filler text or invented metrics. More than four requires an explicit design decision.
- Sales now has two equal 608 px KPI cards with a 16 px gutter. Removes unavailable placeholders and their interactions. TimeControl layout and semantic model are unchanged.

## Component specification 1.4.1 - 2026-09-28

- Records user acceptance of the rendered TimeControl as the frozen Golden Sample standard; no layout or visual definitions changed.
- Separates visual acceptance from the open ancient-date investigation; adds source mapping, proposed date-validity policy and read-only diagnostic. No source data or transformations changed.

## Component specification 1.4.0 - 2026-09-28

- Corrects reported selector overflow by widening TimeControl to 816 px with a 536 px granularity selector, preserving Branch -> TimeControl -> Customer.
- Removes forced categorical date-axis behavior and 60 px category slots; requests continuous date/numeric scaling with text-period fallback.
- Verifies all five parameter targets statically and records each Desktop state as Pending. Prior render success did not establish component completion.

## Component specification 1.3.1 - 2026-09-28

- Names the reusable pair TimeControl and records its no-overflow, active-highlight and independent-range acceptance contract.
- Uses full selector width with reduced item padding; preserves selected-state styling and saved Month.
- Adds explicit trend axis font/category spacing and documents the existing five canonical parameter mappings and native density limitations. Desktop verification remains pending; model and theme unchanged.

## Component specification 1.3.0 - 2026-09-28

- Replaces the separate Display by slot with a combined 608 px Time control: adjacent date inputs and horizontal Day/Week/Month/Quarter/Year tiles on one continuous white surface.
- Mandatory primary order is Branch -> Time control -> business-specific filters, with matching keyboard order. Customer moves after the Time control.
- Keeps existing model bindings, default Month and filter interactions. Theme and semantic model are unchanged. Desktop verification of tile fit and selection styling remains pending.

## Component specification 1.2.1 - 2026-09-28

- Makes Branch -> Date / Period -> business-specific filters mandatory across standard pages; business exceptions must be documented.
- Swaps Golden Sample Branch and Date range positions and keyboard order; Display by remains a separate control after Customer.
- Synchronizes component metadata and authoring rules. Theme and model remain unchanged; Desktop rendering is pending.

## Component specification 1.2.0 - 2026-09-28

- Adds shared time-granularity selector and independent Date range control to the Golden Sample; one trend supports Day/Week/Month/Quarter/Year.
- Documents explicit calendar hierarchies, ISO week-year behavior, sortable axis fields and naming migration in MODEL.md.
- Control strip now uses four 296 px slots. Canonical theme remains 1.0.0; runtime field-parameter verification is pending.

## Component specification 1.1.0 - 2026-09-28

- Compact Golden Sample header/navigation, three equal filters and 96 px value-only KPIs; table gains 16 px height without restyling.
- Defines optional comparison/status KPI variant and five-slot native navigation states.
- Removes internal development text from the canvas and documents the visible date/customer model issues without report workarounds.
- Canonical theme stays at 1.0.0; visual bindings, model and module reports are unchanged. Revised rendering remains pending.

## 1.0.0 - 2026-09-28

### Added

- Canonical light ERP theme with restrained colors, Segoe UI typography, surfaces and native visual defaults.
- Design system documenting the 1280 x 720 grid, components, interactions, accessibility, formatting and generation workflow.
- Permanent internal Golden Sample designation for `Templates/TopEvoAnalytics.Report`; excluded from customer deployment.
- Repository rules for shared-model architecture, `_Measures`, PBIR identities, theme ownership and validation.

### Validation and adoption

- Theme statically validated against Microsoft's `reportThemeSchema-2.150.json`.
- No theme import or visual PBIR definitions in this release. Golden Sample components await implementation and approval.
- Desktop import/rendering and embedded validation are pending. Record the exact runtime build during adoption.
- Sales, Purchases, Inventory and the semantic model are unchanged. Existing model/identity issues remain separately scoped migration work.

### Compatibility

- Theme defaults cannot enforce layout, bindings, business rules or interactions. Local visual formatting may override them.
- New-card typography uses `cardVisual.label` and `cardVisual.value` from the schema.
- Synchronize report-local custom theme resources from the canonical source when adopting the foundation.

## Localization architecture - 2026-09-28

- Adds en-US/de-DE/ro-RO model captions, shared label measures/catalogues and locale-filtered grain presentation rows.
- Golden Sample and Sales use metadata captions and expression-based titles without language-specific pages or geometry changes. Accessibility text uses localized measures; native navigation remains a documented host integration item.
- Business calculations, relationships, source transformations, Purchases and Inventory remain unchanged. Desktop/embedded language validation remains required.
