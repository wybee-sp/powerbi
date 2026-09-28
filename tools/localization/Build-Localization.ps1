param([Parameter(Mandatory=$true)][string]$TomLibraryPath)
$ErrorActionPreference='Stop'
foreach($n in @('Microsoft.AnalysisServices.Core.dll','Microsoft.AnalysisServices.Tabular.Json.dll','Microsoft.AnalysisServices.Tabular.dll')){Add-Type -Path (Join-Path $TomLibraryPath $n)}
$root=Resolve-Path (Join-Path $PSScriptRoot '../..')
$definition=Join-Path $root 'Templates/TopEvoAnalytics.SemanticModel/definition'
$m=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeModelFromFolder($definition)
$metadata=Get-Content (Join-Path $root 'Templates/Localization/metadata.json') -Raw | ConvertFrom-Json
$catalog=Get-Content (Join-Path $root 'Templates/Localization/labels.json') -Raw | ConvertFrom-Json -AsHashtable
function AddTranslation($culture,$obj,$property,$value){
 $old=@($culture.ObjectTranslations|Where-Object {$_.Object -eq $obj -and $_.Property.ToString() -eq $property})
 foreach($x in $old){$null=$culture.ObjectTranslations.Remove($x)}
 $tr=[Microsoft.AnalysisServices.Tabular.ObjectTranslation]::new();$tr.Object=$obj;$tr.Property=$property;$tr.Value=$value;$culture.ObjectTranslations.Add($tr)
}
foreach($locale in @('en-US','de-DE','ro-RO')){
 $culture=$m.Cultures.Find($locale)
 if(!$culture){$culture=[Microsoft.AnalysisServices.Tabular.Culture]::new();$culture.Name=$locale;$m.Cultures.Add($culture)}
 foreach($entry in $metadata.entries){
  $table=$m.Tables[$entry.table]
  $obj=switch($entry.kind){'table'{$table};'column'{$table.Columns[$entry.name]};'measure'{$table.Measures[$entry.name]};'hierarchy'{$table.Hierarchies[$entry.name]}}
  if(!$obj){throw "Missing metadata object $($entry.table).$($entry.name)"}
  $caption=$entry.captions.$locale;if(!$caption){$caption=$entry.captions.'en-US'}
  if(!$caption){throw 'English fallback required'}
  AddTranslation $culture $obj 'Caption' $caption
  # Explicit descriptions can be supplied separately; never manufacture a business definition.
  if($entry.descriptions){$description=$entry.descriptions.$locale;if(!$description){$description=$entry.descriptions.'en-US'};if($description){AddTranslation $culture $obj 'Description' $description}}
 }
 foreach($hierarchy in $m.Tables['Date'].Hierarchies){foreach($level in $hierarchy.Levels){
  $key=$level.Name;$en=$key;$translated=$null;if($catalog.labels.Contains($key)){$translated=$catalog.labels[$key][$locale]};if(!$translated){$translated=$en};AddTranslation $culture $level 'Caption' $translated
 }}
 [Microsoft.AnalysisServices.Tabular.TmdlSerializer]::SerializeObject($culture) | Set-Content (Join-Path $definition "cultures/$locale.tmdl") -Encoding utf8
}
$t=$m.Tables.Find('_ReportLabels')
if(!$t){$t=[Microsoft.AnalysisServices.Tabular.Table]::new();$t.Name='_ReportLabels';$t.IsHidden=$true;$t.LineageTag=[guid]::NewGuid().ToString();$m.Tables.Add($t)
 $col=[Microsoft.AnalysisServices.Tabular.CalculatedTableColumn]::new();$col.Name='Value';$col.DataType='Int64';$col.SourceColumn='[Value]';$col.IsHidden=$true;$col.SummarizeBy='None';$col.LineageTag=[guid]::NewGuid().ToString();$t.Columns.Add($col)
 $p=[Microsoft.AnalysisServices.Tabular.Partition]::new();$p.Name='_ReportLabels';$p.Mode='Import';$p.Source=[Microsoft.AnalysisServices.Tabular.CalculatedPartitionSource]::new();$p.Source.Expression='{ 1 }';$t.Partitions.Add($p)
}
foreach($key in $catalog.labels.Keys){
 $me=$t.Measures.Find($key);if(!$me){$me=[Microsoft.AnalysisServices.Tabular.Measure]::new();$me.Name=$key;$me.LineageTag=[guid]::NewGuid().ToString();$t.Measures.Add($me)}
 $values=$catalog.labels[$key];$en=$values['en-US'];if(!$en){throw "No fallback for $key"}
 $de=$values['de-DE'];if(!$de){$de=$en};$ro=$values['ro-RO'];if(!$ro){$ro=$en}
 $me.Expression='SWITCH ( LOWER ( USERCULTURE() ), "de-de", "'+$de.Replace('"','""')+'", "ro-ro", "'+$ro.Replace('"','""')+'", "'+$en.Replace('"','""')+'" )'
 $me.Description='Localized presentation label; not a business calculation.';$me.DisplayFolder='Report labels'
}
[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::SerializeObject($t) | Set-Content (Join-Path $definition 'tables/_ReportLabels.tmdl') -Encoding utf8
$parameter=$m.Tables['Time Granularity'];$localeCol=$parameter.Columns.Find('Locale')
if(!$localeCol){$localeCol=[Microsoft.AnalysisServices.Tabular.CalculatedTableColumn]::new();$localeCol.Name='Locale';$localeCol.DataType='String';$localeCol.SourceColumn='[Value4]';$localeCol.IsHidden=$true;$localeCol.SummarizeBy='None';$localeCol.LineageTag=[guid]::NewGuid().ToString();$parameter.Columns.Add($localeCol)}
$rows=@();$keys=@('Day','Week','Month','Quarter','Year');$fields=@('Date','YearWeek','YearMonth','YearQuarter','Year')
foreach($locale in @('en-US','de-DE','ro-RO')){for($i=0;$i -lt 5;$i++){$label=$catalog.labels[$keys[$i]][$locale];if(!$label){$label=$catalog.labels[$keys[$i]]['en-US']};$rows+='("'+$label+'", NAMEOF(''Date''['+$fields[$i]+']), '+$i+', "'+$locale+'")'}}
$parameter.Partitions[0].Source.Expression="{`n"+($rows -join ",`n")+"`n}"
[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::SerializeObject($parameter) | Set-Content (Join-Path $definition 'tables/Time Granularity.tmdl') -Encoding utf8
$modelFile=Join-Path $definition 'model.tmdl';$text=Get-Content $modelFile -Raw
foreach($line in @('ref table _ReportLabels','ref cultureInfo de-DE','ref cultureInfo ro-RO')){if(!$text.Contains($line)){$text+="`n$line`n"}}
Set-Content $modelFile $text -Encoding utf8
foreach($file in @((Join-Path $definition 'model.tmdl'),(Join-Path $definition 'tables/_ReportLabels.tmdl'),(Join-Path $definition 'tables/Time Granularity.tmdl')) + @(Get-ChildItem (Join-Path $definition 'cultures') -Filter '*.tmdl' | ForEach-Object FullName)) {
 [System.IO.File]::WriteAllText($file, (Get-Content $file -Raw).TrimEnd()+"`n", [System.Text.UTF8Encoding]::new($false))
}
'Generated cultures, presentation measures and localized grain rows; existing business objects unchanged.'
