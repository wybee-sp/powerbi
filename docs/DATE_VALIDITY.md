# ERP date validity investigation

## Evidence and current limit

The user reports Date range starting at `01.01.0106`. The current PBIR date slicer binds Date[Date] and saves no start/end bounds. The calendar takes minimum/maximum values from eleven date columns, including inactive date roles, with no business-validity constraint. A single extreme source date can therefore influence bounds.

No responsible source row has yet been identified: the configured local CSV folder is absent in this workspace, and no running Desktop/model instance is available. Do not present a parser weakness as proof of the exact displayed year. Inspect the actual refreshed Date minimum, slicer state and loaded artifact version as well as the raw records. DAX DATE adds 1900 to year arguments from 0 through 1899; therefore a source year 0106 alone does not establish why this particular DAX calendar would render 0106.

Confirmed parsing weaknesses:

- A42001's three date fields accept any eight-character value whose components form an M date. There is no business-year window.
- A8101OP's date fields are converted to integers, then left-padded to eight digits. Synthetic example: 1060101 becomes 01060101, accepted by M as 0106-01-01. This is an illustration, not an observed customer row.
- Both parsers turn parsing errors into null and remove the raw date columns later, making provenance harder to inspect.

## Source mapping to audit

| File | Raw field | Loaded date |
| --- | --- | --- |
| A42001.csv | Auftragsdatum [104] | a42001.OrderDate |
| A42001.csv | Leistungsdatum [106] | a42001.ServiceDate |
| A42001.csv | Datum [315] | a42001.InvoiceDate |
| A8101OP.csv | Rechnungsdatum [109] | InvoiceDate |
| A8101OP.csv | Fällig am [119] | DueDate |
| A8101OP.csv | Erfassungdatum [112] | EntryDate |
| A8101OP.csv | Datum (Valuta) [103] | ValueDate |

For the last four fields, lfdNr=0 loads into a8101op_invoices and lfdNr>0 into a8101op_payments, covering eight model columns. All eleven columns affect calendar bounds, not just active InvoiceDate.

## Read-only diagnostic

Paste `diagnostics/ERP_DATE_AUDIT.pq` into a new blank query in a LOCAL copy of the model, with load disabled. Inspect ColumnSummary, EarliestRows and Exceptions. The diagnostic references existing staging queries and changes neither source nor fact transformations. SourceRecord is a one-based CSV data-record index, not a physical text line (quoted fields may contain newlines). Capture source field, raw value, parser input, parsed date and record key for every offending row. For A8101OP the raw staging value has already undergone integer conversion: confirm the original text directly in CSV, especially leading zeros and type errors. Diagnostic M has been reviewed statically but cannot be executed here without the source queries/data.

Keep customer-specific results local and out of Git. Compare every column minimum to the refreshed Date[Date] minimum before attributing causality. Check the report's saved filter state if the actual Date minimum differs from the visible input.

## Proposed general policy — not implemented

1. Parse the declared ERP format explicitly: eight digits YYYYMMDD, a valid calendar day, no guessed century or left-padding of malformed values. Classify empty/zero/sentinel values separately from malformed dates.
2. Use centrally configured business bounds, not report-specific cutoffs. Suggested initial review window: 1990-01-01 through December 31 of refresh year + 2. Confirm historical migration needs and longer planned/due-date horizons per date role; these are proposed defaults, not universal facts.
3. Preserve every source record and original date value. Expose ParsedDate, DateQualityStatus and source/row provenance in a shared quality audit. Do not silently drop rows, rewrite ancient dates to a guessed year or replace errors without a status.
4. Once evidence is reviewed, compute canonical calendar bounds only from dates classified Valid. Invalid/out-of-policy dates must not extend the calendar. Retain facts in unfiltered totals and disclose records outside the valid dated analysis. Reconcile overall versus date-filtered totals explicitly.
5. Extend the valid calendar to full-year boundaries and a documented future horizon; reject pathological spans with a visible refresh diagnostic. If no valid dates remain, report the condition explicitly rather than silently returning an apparently healthy calendar.
6. Before changing transformations, record the offending source columns/rows and agree how to correct or classify them. Validate date roles, counts and monetary totals before/after. Fix the ERP source when possible.

No transformations, source records, relationships or calendar bounds are changed in this investigation.

References: [Power Query #date](https://learn.microsoft.com/en-us/powerquery-m/sharpdate), [DAX DATE](https://learn.microsoft.com/en-us/dax/date-function-dax).
