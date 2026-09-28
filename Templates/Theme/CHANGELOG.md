# TopEvo visual foundation changelog

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
