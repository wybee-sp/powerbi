param([Parameter(Mandatory=$true)][string]$TomLibraryPath,[Parameter(Mandatory=$true)][string]$SchemaDirectory)
$ErrorActionPreference='Stop'
foreach($n in @('Microsoft.AnalysisServices.Core.dll','Microsoft.AnalysisServices.Tabular.Json.dll','Microsoft.AnalysisServices.Tabular.dll')){Add-Type -Path (Join-Path $TomLibraryPath $n)}
$root=Resolve-Path (Join-Path $PSScriptRoot '../..')
$m=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeModelFromFolder((Join-Path $root 'Templates/TopEvoAnalytics.SemanticModel/definition'))
$catalog=Get-Content (Join-Path $root 'Templates/Localization/labels.json') -Raw|ConvertFrom-Json -AsHashtable
$metadata=Get-Content (Join-Path $root 'Templates/Localization/metadata.json') -Raw|ConvertFrom-Json
foreach($locale in @('en-US','de-DE','ro-RO')){
 $culture=$m.Cultures[$locale];if(!$culture){throw "Missing culture $locale"}
 foreach($e in $metadata.entries){$t=$m.Tables[$e.table];$obj=switch($e.kind){'table'{$t};'column'{$t.Columns[$e.name]};'measure'{$t.Measures[$e.name]};'hierarchy'{$t.Hierarchies[$e.name]}}
 $tr=@($culture.ObjectTranslations|Where-Object {$_.Object -eq $obj -and $_.Property -eq 'Caption'});$expected=$e.captions.$locale;if(!$expected){$expected=$e.captions.'en-US'}
 if($tr.Count -ne 1 -or $tr[0].Value -ne $expected){throw "Caption mismatch $locale/$($e.name)"}
 }
 foreach($key in $catalog.labels.Keys){if(!$catalog.labels[$key]['en-US']){throw 'English fallback missing'};$expr=$m.Tables['_ReportLabels'].Measures[$key].Expression;if(!$expr.Contains('USERCULTURE()') -or !$expr.Contains($catalog.labels[$key]['en-US'].Replace('"','""'))){throw "Invalid label $key"}}
}
$parameter=$m.Tables['Time Granularity'];$rows=[regex]::Matches($parameter.Partitions[0].Source.Expression,'\("([^"]+)", NAMEOF\(''Date''\[([^\]]+)\]\), ([0-4]), "([^"]+)"\)')
if($rows.Count -ne 15){throw 'Expected 15 parameter rows'}
$fields=@('Date','YearWeek','YearMonth','YearQuarter','Year');$keys=@('Day','Week','Month','Quarter','Year')
foreach($locale in @('en-US','de-DE','ro-RO')){for($i=0;$i -lt 5;$i++){
 $match=@($rows|Where-Object {$_.Groups[4].Value -eq $locale -and $_.Groups[3].Value -eq "$i"})
 if($match.Count -ne 1 -or $match[0].Groups[2].Value -ne $fields[$i] -or $match[0].Groups[1].Value -ne $catalog.labels[$keys[$i]][$locale]){throw 'Invalid localized grain mapping'}
 if(!$m.Tables['Date'].Columns[$fields[$i]]){throw 'Unknown axis field'}
}}
function CheckBindings($node) {
 if ($node -is [System.Collections.IDictionary]) {
  foreach ($kind in @('Measure','Column')) {
   if ($node.Contains($kind)) {
    $f=$node[$kind]; $entity=$f.Expression.SourceRef.Entity
    if ($entity) {
     $t=$m.Tables[$entity]
     if (!$t) { throw "Missing table $entity" }
     if ($kind -eq 'Measure') {
      if (!$t.Measures[$f.Property]) { throw "Missing measure $($f.Property)" }
     } else {
      if (!$t.Columns[$f.Property]) { throw "Missing column $($f.Property)" }
     }
    }
   }
  }
  foreach ($value in $node.Values) { CheckBindings $value }
 } elseif ($node -is [System.Collections.IList]) {
  foreach ($value in $node) { CheckBindings $value }
 }
}
foreach($report in @('Templates/TopEvoAnalytics.Report','Templates/Sales/Sales.Report')){
 $path=Join-Path $root $report;$manifest=Get-Content "$path/COMPONENTS.json" -Raw|ConvertFrom-Json -AsHashtable
 foreach($f in Get-ChildItem "$path/definition/pages" -Recurse -Filter visual.json){
  $v=Get-Content $f.FullName -Raw|ConvertFrom-Json -AsHashtable;CheckBindings $v
  $v['$schema']='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json'
  if(!(Test-Json -Json ($v|ConvertTo-Json -Depth 100) -SchemaFile (Join-Path $SchemaDirectory 'topevo-visual-bundle.json'))){throw "Invalid visual $($f.FullName)"}
 }
 $r=Get-Content "$path/definition/report.json" -Raw|ConvertFrom-Json -AsHashtable;CheckBindings $r
 if(!(Test-Json -Json ($r|ConvertTo-Json -Depth 100) -SchemaFile (Join-Path $SchemaDirectory 'topevo-report-bundle.json'))){throw 'Invalid report'}
 $localeFilter=@($r.filterConfig.filters|Where-Object {$_.field.Column.Property -eq 'Locale' -and $_.field.Column.Expression.SourceRef.Entity -eq 'Time Granularity'})
 if($localeFilter.Count -ne 1 -or $localeFilter[0].filter.Where[0].Condition.In.Values[0][0].Literal.Value -ne "'en-US'"){throw 'Missing English initial locale filter'}
 $grain=@($manifest.components|Where-Object {$_.role -eq 'control.granularity'})[0]
 $g=Get-Content "$path/definition/pages/ReportSection/visuals/$($grain.id)/visual.json" -Raw|ConvertFrom-Json -AsHashtable
 $selection=$g.visual.objects.general[0].properties.filter.filter.Where[0].Condition.In
 if($selection.Expressions[0].Column.Property -ne 'Order' -or $selection.Values[0][0].Literal.Value -ne '2L'){throw 'Grain default must be language-neutral Order=2'}
}
$captionConfig=Get-Content (Join-Path $root 'Templates/Localization/visual-captions.json') -Raw|ConvertFrom-Json
$captionTable=$m.Tables[$captionConfig.parameterTable]
if(!$captionTable -or !$captionTable.IsHidden){throw 'Missing hidden visual-caption parameter'}
$captionExpression=$captionTable.Partitions[0].Source.Expression
foreach($locale in @('en-US','de-DE','ro-RO')){foreach($field in $captionConfig.fields){
 $entry=@($metadata.entries|Where-Object {$_.table -eq $field.table -and $_.name -eq $field.name -and $_.kind -eq $field.kind})[0]
 $caption=$entry.captions.$locale;if(!$caption){$caption=$entry.captions.'en-US'}
 $row='("'+$caption.Replace('"','""')+'", NAMEOF('''+$field.table.Replace("'","''")+'''['+$field.name.Replace(']',']]')+']), '+$field.order+', "'+$locale+'")'
 if(!$captionExpression.Contains($row)){throw "Invalid caption mapping $locale/$($field.order)"}
}}
if($captionTable.Columns['Caption'].SortByColumn.Name -ne 'Order' -or $captionTable.Columns['Caption'].RelatedColumnDetails.GroupByColumns[0].GroupingColumn.Name -ne 'Fields'){throw 'Invalid caption parameter metadata'}
$golden=Join-Path $root 'Templates/TopEvoAnalytics.Report'
$r=Get-Content "$golden/definition/report.json" -Raw|ConvertFrom-Json -AsHashtable
$filter=@($r.filterConfig.filters|Where-Object {$_.field.Column.Expression.SourceRef.Entity -eq '_VisualCaptions'})
if($filter.Count -ne 1 -or $filter[0].filter.Where[0].Condition.In.Values[0][0].Literal.Value -ne "'en-US'"){throw 'Missing caption locale filter'}
$manifest=Get-Content "$golden/COMPONENTS.json" -Raw|ConvertFrom-Json -AsHashtable
foreach($component in $manifest.components|Where-Object {$_.role -like 'kpi.*' -or $_.role -eq 'table.summary'}){
 $v=Get-Content "$golden/definition/pages/ReportSection/visuals/$($component.id)/visual.json" -Raw|ConvertFrom-Json -AsHashtable
 $bucket=if($component.role -like 'kpi.*'){$v.visual.query.queryState.Data}else{$v.visual.query.queryState.Values}
 if($bucket.fieldParameters[0].parameterExpr.Column.Expression.SourceRef.Entity -ne '_VisualCaptions' -or $bucket.fieldParameters[0].length -ne $bucket.projections.Count){throw 'Invalid caption binding'}
 foreach($projection in $bucket.projections){
  $kind=if($projection.field.Contains('Measure')){'measure'}else{'column'};$ref=$projection.field[$kind.Substring(0,1).ToUpper()+$kind.Substring(1)]
  $entry=@($metadata.entries|Where-Object {$_.table -eq $ref.Expression.SourceRef.Entity -and $_.name -eq $ref.Property -and $_.kind -eq $kind})[0]
  if($projection.displayName -ne $entry.captions.'en-US'){throw 'Technical or incorrect initial caption'}
  if($component.role -like 'kpi.*'){
   $expected=@($captionConfig.fields|Where-Object {$_.table -eq $entry.table -and $_.name -eq $entry.name})[0].order
   $selection=@($v.filterConfig.filters|Where-Object {$_.field.Column.Expression.SourceRef.Entity -eq '_VisualCaptions'})[0]
   if($selection.field.Column.Property -ne 'Order' -or $selection.filter.Where[0].Condition.In.Values[0][0].Literal.Value -ne "$($expected)L"){throw 'KPI must retain its original measure'}
  }
 }
}
'PASS: localized visual-caption parameter, original field targets, English cached captions, stable KPI selections and caption locale filter.'
'PASS: three culture dictionaries; 15 label/axis pairs; English fallback definitions; title/field references; report schemas; stable Month key and host locale filter. Runtime rendering not tested.'
