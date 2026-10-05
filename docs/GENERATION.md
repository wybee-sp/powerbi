# TopEvo Overview generation and synchronization

## Scope and ownership

`Templates/PageTemplates/overview.layout.json` is the shared, language-neutral geometry contract. It references existing Golden Sample visual implementations instead of copying their formatting into a second hand-maintained component library. It contains the canvas, fixed slots, adaptive KPI row, summary-column width variants and optional-slot/interaction policies.

`Templates/Sales/overview.bindings.json` supplies Sales fields, existing measure queries, label keys, numeric display units/precision and stable target IDs. Its complete query fragments preserve parameter/sort behavior from the current Sales Overview. It does not contain geometry or business calculations. Net Revenue and Invoice Count remain on `a42001`, with a documented legacy exception; this task does not migrate the shared model.

`tools/generation/generate.py` compiles these inputs into PBIR candidates. It replaces Golden Sample business queries and labels rather than transferring Receivables semantics. The first implementation supports synchronization of an existing module Overview and adding/removing its managed visual components. It does not create entire new reports or pages, deploy reports, or discover and update every module automatically. Run it explicitly for each registered STANDARD binding manifest.

The Sales report and Overview are classified STANDARD in the binding manifest. The pre-existing hidden Receivables page is explicitly protected from this workflow. It is not adopted as generated content. CUSTOM or unclassified report/page targets, unknown visuals, changes of existing IDs, unsafe paths and customer override paths are refused. After the first successful apply, the external `Sales.Report/GENERATION.json` records visual ownership and template fingerprint. No TopEvo metadata is added to schema-controlled PBIR.

## Commands

Python 3.11+ is sufficient for planning and behavioral tests; no third-party Python package is required. Execute from the repository root:

```powershell
python -B tools/generation/generate.py
python -B tools/generation/generate.py --bindings Templates/Sales/overview.bindings.json --plan "$env:TEMP/topevo-sales-generation-plan.json"
```

Default mode writes nothing into the repository. The optional external plan contains complete candidate JSON for changed files, explicit removals, input hashes, limitations and the review fingerprint. It is a reviewable change set, not a standalone PBIP or a Power BI deployment package. Do not put a plan containing a local review snapshot into Git.

Validate the candidate with the existing pinned Microsoft TOM runtime and schema cache:

```powershell
./tools/generation/Validate-Plan.ps1 `
  -Plan "$env:TEMP/topevo-sales-generation-plan.json" `
  -TomLibraryPath <TOM-library-directory> `
  -SchemaDirectory <schema-cache-directory>
```

Validation dependencies are the same Microsoft TOM 19.117.0 DLLs and cached Microsoft schemas used by the localization tooling. Required schema filenames: `topevo-visual-bundle.json`, `topevo-page-bundle.json`, `topevo-report-bundle.json`, `topevo-theme-schema-2.150.json`. The unavailable declared visual 2.12 schema is checked against published 2.9 compatibility without rewriting declarations. This is explicitly not full 2.12 validation or Desktop rendering. No runtime/library/font binaries or machine paths are committed.

After the current Golden Sample implementation has actually been rendered and approved, record `review.status=APPROVED`, the tested Desktop build, review evidence and the exact printed fingerprint in the central layout. The fingerprint covers layout, Golden Sample source definitions, canonical theme and design-system document. Changes invalidate approval. There is no force/skip-review CLI switch. Do not mark a candidate approved merely to make apply run.

```powershell
python -B tools/generation/generate.py `
  --bindings Templates/Sales/overview.bindings.json `
  --apply --tom-library <TOM-library-directory> --schemas <schema-cache-directory>
```

Apply requires PowerShell 7 (`pwsh`) and runs TOM/schema validation before any report writes. It recomputes the plan afterward to reject concurrent edits. Writes are limited to the managed Overview page, its visual files, COMPONENTS.json and GENERATION.json. The report identity, shared-model reference, global settings, page order, other pages and semantic model are not rewritten. Existing visual IDs remain; new IDs are deterministically derived from the target report identity, page and component role, never copied from Golden Sample. Removals delete only explicitly owned `visual.json` files and rebuild interactions. Bookmarked visual removals are refused for explicit migration. On a normal write exception, prior file bytes are restored; this is not a crash-proof filesystem transaction. Review Git diff and render the Sales report after applying.

## Component behavior

- Header, navigation, Branch, date range, granularity and business filter are required.
- Render 0–4 curated existing KPI measures. Zero omits the row; 1–4 use 1232/608/400/296 px widths with 16 px gutters. More than four is refused.
- Omit optional trend, ranking or summary by omitting its binding. An invalid field is an error, not a reason to generate an empty component.
- The first optional-slot variant omits without reflow: remaining components keep their approved positions. More compact variants require an explicit central layout and render review.
- Date range uses only Date[Date]; the trend uses the shared Time Granularity parameter. Grain selection is separate from business filtering. All incoming interactions to the granularity selector are disabled; it filters only the trend.
- Layout files contain no translated titles. Bindings reference the canonical labels; existing TMDL metadata translations and locale filters remain. The Golden Sample date header and native navigation retain their documented English fallback.
- The generator does not copy the Receivables `_VisualCaptions` parameter into Sales, because that would select the wrong business fields. Sales currently retains its metadata-based KPI/table captions, requiring all-locale runtime verification.
- Theme copies must match the canonical theme before planning. Automatic report-wide theme replacement is intentionally refused, as it could alter a protected CUSTOM page.

## Validation evidence and current gate

The first Sales candidate was generated and passed Microsoft TOM deserialization, alias-aware field/measure reference checks, report/page/visual schema compatibility and canonical theme validation. Static geometry checks cover canvas bounds, overlap, header clearance, primary filter ordering and TimeControl adjacency/width. The binding manifest preserves Sales query/sort expressions. These checks do not prove text fit, filter usability, translated runtime captions or correct monetary totals.

Behavioral tests run entirely in temporary definition-only fixtures:

```powershell
python -B -m unittest discover -s tools/generation -p test_generation.py -v
```

Tests cover CUSTOM/unclassified protection; unknown visuals; missing measures and labels; unsafe targets; ID preservation/collisions; 0–4 KPI layouts and unique new IDs; optional-component removal and dependency repair; layout overlap; stale plans/approval; preservation of model, report identity and protected page bytes; and a second apply plan with no changes. Test-only approval fixtures are not Desktop evidence. The separate PowerShell integration check validates the real candidate.

**Current status:** the latest Golden Sample dynamic textbox/date-slicer repair remains pending Desktop verification in the repository. The layout review therefore stays PENDING, and live Sales PBIR has not been synchronized. This follows AGENTS.md: “Components must be implemented, rendered and approved in the Golden Sample before generation” and “Do not propagate unrendered component changes as approved.” Creating a candidate for inspection does not approve or deploy it. See `docs/HEADER_DATE_SLICER_REPAIR.md` for the exact remaining render checks.

No Purchases, Inventory, semantic-model, Golden Sample or customer-specific report files were modified. No generator operation publishes or pushes Git changes.
## Files added or changed in this implementation

Created:

- `Templates/PageTemplates/overview.layout.json`
- `Templates/Sales/overview.bindings.json`
- `tools/generation/generate.py`
- `tools/generation/Validate-Plan.ps1`
- `tools/generation/test_generation.py`
- `docs/GENERATION.md`

Changed:

- `Templates/Theme/DESIGN_SYSTEM.md`
- `Templates/Theme/CHANGELOG.md`
- `Templates/Sales/Sales.Report/SALES_OVERVIEW.md`
