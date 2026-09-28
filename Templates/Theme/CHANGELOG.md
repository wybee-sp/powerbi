# TopEvo visual foundation changelog

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
