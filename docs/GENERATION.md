# TopEvo Overview generation and synchronization

## Scope and ownership

`Templates/PageTemplates/overview.layout.json` is the shared, language-neutral geometry contract. It references existing Golden Sample visual implementations instead of copying their formatting into a second hand-maintained component library. It contains the canvas, fixed slots, adaptive KPI row, summary-column width variants and optional-slot/interaction policies.

`Templates/Sales/overview.bindings.json` supplies Sales fields, existing measure queries, label keys, numeric display units/precision and stable target IDs. Its complete query fragments preserve parameter/sort behavior from the current Sales Overview. It does not contain geometry or business calculations. Net Revenue and Invoice Count remain on `a42001`, with a documented legacy exception; this task does not migrate the shared model.

`tools/generation/generate.py` compiles these inputs into PBIR candidates. It replaces Golden Sample business queries and labels rather than transferring Receivables semantics. The first implementation supports synchronization of an existing module Overview and adding/removing its managed visual components. It does not create entire new reports or pages, deploy reports, or discover and update every module automatically. Run it explicitly for each registered STANDARD binding manifest.

The Sales report and Overview are classified STANDARD in the binding manifest. The pre-existing hidden Receivables page is explicitly protected from this workflow. It is not adopted as generated content. CUSTOM or unclassified report/page targets, unknown visuals, changes of existing IDs, unsafe paths and customer override paths are refused. After the first successful apply, the external `Sales.Report/GENERATION.json` records visual ownership and template fingerprint. No TopEvo metadata is added to schema-controlled PBIR.

## Commands

Python 3.11+ and PowerShell 7 (`pwsh`) are required for planning and tests. No third-party Python package is required. Every plan validates the layout against the closed JSON Schema `Templates/PageTemplates/overview.layout.schema.json` (Draft 2020-12) using `Test-Json`. Unknown properties, malformed positions, invalid width variants and unsupported policies are rejected. Execute from the repository root:

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

For a change that alters PBIR, after the selected component variant has actually been rendered and approved, record `review.status=APPROVED`, the tested Desktop build, review evidence and the exact printed fingerprint in the central layout. The fingerprint covers layout, Golden Sample source definitions, canonical theme and design-system document. Changes invalidate approval. A content-equivalent synchronization (`pbirEquivalent=true`) needs no new rendering approval because it cannot change any PBIR content. The comparison includes the complete page, every visual and removals; unchanged files are not rewritten. There is no force/skip-review CLI switch. Do not mark a candidate approved merely to make apply run.

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

**Current status:** Sales Overview has been adopted with the central `existing-overview` variant. Its PBIR is byte-for-byte unchanged. The variant records only the shared geometry/format differences from the latest Golden Sample: existing title card, navigation geometry, date-slicer appearance, KPI insets and table auto-sizing. Sales queries and label bindings remain in the Sales manifest. No language-specific layout or Receivables business query is introduced. Existing non-template interaction pairs are retained; template-controlled pairs take precedence and removed visuals lose their interaction references.

The latest Golden Sample repairs still have PENDING rendering evidence. Adoption does not approve or propagate those repairs. A later migration to the default variant must be explicit and rendered. Existing limitations of the Sales rendering/localization remain; preserving the report does not fix or independently validate them.

## Propagating a central layout change

1. Edit shared geometry or component formatting in `overview.layout.json`; edit `variants.existing-overview.slots` only for properties that this compatibility variant overrides. Other geometry is inherited from the base slots. Do not edit generated PBIR to implement shared changes.
2. Run a plan for each explicitly registered STANDARD manifest, starting with `Templates/Sales/overview.bindings.json`. CUSTOM and unclassified targets are refused; there is no wildcard overwrite or automatic customer migration.
3. Review the candidate and run `Validate-Plan.ps1`. It validates the entire target page, including unchanged visuals, not only the write set. Queries, labels, existing IDs and protected pages must remain intact.
4. When PBIR changes, verify the candidate variant in Power BI Desktop and record the build, evidence and current fingerprint in `review`. The selected variant participates in that fingerprint. This first workflow records one approval fingerprint at a time; validate/apply each variant explicitly. No-PBIR-change adoption is allowed without marking the newer component approved.
5. Run `--apply` with the TOM/schema dependencies. Run another plan; its write/remove set must be empty. Review Git diff and perform the documented Desktop/embedded checks for visible changes before release.

Validation in this implementation: 13 behavioral tests, complete Sales page/model-reference/schema compatibility checks, and a post-apply no-op plan. All Sales PBIR files remain byte-identical to the pre-adoption state. No new Desktop rendering was performed.

No Purchases, Inventory, semantic-model, Golden Sample or customer-specific report files were modified. No generator operation publishes or pushes Git changes.
## Files added or changed in this implementation

Created:

- `Templates/PageTemplates/overview.layout.schema.json`
- `Templates/Sales/Sales.Report/GENERATION.json`

Changed:

- `Templates/PageTemplates/overview.layout.json`
- `Templates/Sales/overview.bindings.json`
- `Templates/Sales/Sales.Report/COMPONENTS.json`
- `Templates/Sales/Sales.Report/SALES_OVERVIEW.md`
- `Templates/Theme/DESIGN_SYSTEM.md`
- `Templates/Theme/CHANGELOG.md`
- `tools/generation/generate.py`
- `tools/generation/Validate-Plan.ps1`
- `tools/generation/test_generation.py`
- `docs/GENERATION.md`

COMPONENTS.json and GENERATION.json are external metadata. No schema-controlled Power BI definition changed.
