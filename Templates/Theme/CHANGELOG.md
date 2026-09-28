# TopEvo visual foundation changelog

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
