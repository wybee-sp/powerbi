Power BI architecture

- TopEvoAnalytics.SemanticModel is the single shared semantic model.
- Do not create semantic models inside individual reports.
- Sales.Report, Purchases.Report, etc. reference the shared model.
- Shared measures belong in _Measures.
- Raw/staging queries must not be exposed to reports.
- Report canvas is 1280x720 (16:9).
- All reports use the TopEvo theme.
- New report pages must follow the TopEvo dashboard layout.
- Customer-specific reports are overrides and must not modify standard templates.
- Never commit customer data, CSV/XML exports, PBIX files or .pbi caches.