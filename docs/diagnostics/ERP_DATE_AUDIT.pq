// Read-only diagnostic: paste as a new blank Power Query in a LOCAL copy.
// Disable load. References existing staging queries; changes no source/fact query.
// Result is a record: inspect ColumnSummary and Exceptions separately.
let
    ProposedMin = #date(1990, 1, 1),
    ProposedMax = #date(Date.Year(DateTime.FixedLocalNow()) + 2, 12, 31),
    HeaderMap = {{"Auftragsdatum [104]", "OrderDate"}, {"Leistungsdatum [106]", "ServiceDate"}, {"Datum [315]", "InvoiceDate"}},
    OpenItemMap = {{"Datum (Valuta) [103]", "ValueDate"}, {"Rechnungsdatum [109]", "InvoiceDate"}, {"Erfassungdatum [112]", "EntryDate"}, {"Fällig am [119]", "DueDate"}},
    Inspect = (source as table, file as text, mapping as list, numericParser as logical) as table =>
        let
            Indexed = Table.AddIndexColumn(source, "AuditRecord", 1, 1, Int64.Type),
            Rows = List.Combine(List.Transform(Table.ToRecords(Indexed), (r) =>
                List.Transform(mapping, (pair) =>
                    let
                        RawAttempt = try Record.Field(r, pair{0}),
                        Raw = if RawAttempt[HasError] then null else RawAttempt[Value],
                        TextValue = if Raw = null then "" else Text.Trim(Text.From(Raw, "en-US")),
                        // Match existing parsers, including open-item left-padding.
                        ParseText = if numericParser and Raw <> null then Text.PadStart(TextValue, 8, "0") else TextValue,
                        Parsed = if Text.Length(ParseText) <> 8 or (numericParser and Raw = 0) then null else
                            try #date(Number.FromText(Text.Start(ParseText, 4)), Number.FromText(Text.Range(ParseText, 4, 2)), Number.FromText(Text.End(ParseText, 2))) otherwise null,
                        Role = if not numericParser then "a42001" else if Record.FieldOrDefault(r, "lfdNr") = 0 then "a8101op_invoices" else if Record.FieldOrDefault(r, "lfdNr", -1) > 0 then "a8101op_payments" else "not loaded into these facts",
                        Issue = if RawAttempt[HasError] then "Staging type error" else if TextValue = "" then "Missing" else if Parsed = null then "Unparseable or zero sentinel" else if Text.Length(TextValue) <> 8 then "Short value accepted by padding" else if Parsed < ProposedMin then "Before proposed minimum" else if Parsed > ProposedMax then "After proposed maximum" else "Within proposed bounds"
                    in [File=file, SourceRecord=r[AuditRecord], SourceColumn=pair{0}, ModelTable=Role, ModelColumn=pair{1}, Key=Record.FieldOrDefault(r, "%Keys"), Firma=Record.FieldOrDefault(r, "Firma"), Betrieb=Record.FieldOrDefault(r, "Betrieb"), Auftrag=Record.FieldOrDefault(r, "Auftrag"), Rechnung=Record.FieldOrDefault(r, "Rechnung"), lfdNr=Record.FieldOrDefault(r, "lfdNr"), RawValue=Raw, ParserInput=ParseText, ParsedDate=Parsed, Issue=Issue]))),
            Result = Table.FromRecords(Rows, type table [File=text, SourceRecord=Int64.Type, SourceColumn=text, ModelTable=text, ModelColumn=text, Key=any, Firma=any, Betrieb=any, Auftrag=any, Rechnung=any, lfdNr=any, RawValue=any, ParserInput=text, ParsedDate=nullable date, Issue=text])
        in Result,
    Dates = Table.Combine({Inspect(a42001_raw, "A42001.csv", HeaderMap, false), Inspect(a8101op_raw, "A8101OP.csv", OpenItemMap, true)}),
    Loaded = Table.SelectRows(Dates, each [ModelTable] <> "not loaded into these facts"),
    ColumnSummary = Table.Group(Loaded, {"File", "ModelTable", "SourceColumn", "ModelColumn"}, {
        {"Minimum", each List.Min(List.RemoveNulls([ParsedDate]), null), type nullable date},
        {"Maximum", each List.Max(List.RemoveNulls([ParsedDate]), null), type nullable date},
        {"Records", each Table.RowCount(_), Int64.Type}}),
    Exceptions = Table.SelectRows(Dates, each [Issue] <> "Within proposed bounds"),
    Earliest = List.Min(List.RemoveNulls(Loaded[ParsedDate]), null),
    EarliestRows = Table.SelectRows(Loaded, each [ParsedDate] <> null and [ParsedDate] = Earliest)
in
    [ColumnSummary=ColumnSummary, EarliestRows=EarliestRows, Exceptions=Exceptions]
