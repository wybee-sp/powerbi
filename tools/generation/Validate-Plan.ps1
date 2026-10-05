param(
 [Parameter(Mandatory=$true)][string]$Plan,
 [Parameter(Mandatory=$true)][string]$TomLibraryPath,
 [Parameter(Mandatory=$true)][string]$SchemaDirectory
)
$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$p=Get-Content -LiteralPath $Plan -Raw | ConvertFrom-Json -AsHashtable
foreach($name in @('Microsoft.AnalysisServices.Core.dll','Microsoft.AnalysisServices.Tabular.Json.dll','Microsoft.AnalysisServices.Tabular.dll')) {
 Add-Type -Path (Join-Path $TomLibraryPath $name)
}
$model=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeModelFromFolder((Join-Path $root 'Templates/TopEvoAnalytics.SemanticModel/definition'))
function Check-References($node, $aliases) {
 if($node -is [System.Collections.IDictionary]) {
  $scope=@{};foreach($key in $aliases.Keys){$scope[$key]=$aliases[$key]}
  if($node.Contains('From')) {foreach($source in $node.From){if($source.Entity){$scope[$source.Name]=$source.Entity}}}
  foreach($kind in @('Measure','Column')) {
   if($node.Contains($kind)) {
    $ref=$node[$kind];$source=$ref.Expression.SourceRef
    $entity=$source.Entity
    if(!$entity -and $source.Source){$entity=$scope[$source.Source];if(!$entity){throw "Unresolved alias $($source.Source)"}}
    if($entity) {
     $table=$model.Tables[$entity];if(!$table){throw "Missing table $entity"}
     $object=if($kind -eq 'Measure'){$table.Measures[$ref.Property]}else{$table.Columns[$ref.Property]}
     if(!$object){throw "Missing $kind $entity.$($ref.Property)"}
    }
   }
  }
  foreach($value in $node.Values){Check-References $value $scope}
 } elseif($node -is [System.Collections.IList]) {foreach($value in $node){Check-References $value $aliases}}
}
foreach($entry in $p.inputs.GetEnumerator()) {
 $path=[IO.Path]::GetFullPath((Join-Path $root $entry.Key))
 if(!$path.StartsWith($root+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Input path escapes repository'}
 if((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.Value){throw "Stale plan: $($entry.Key)"}
}
$candidates=@{}
$pageRoot=Join-Path $root ($p.report+'/definition/pages/'+$p.page)
foreach($file in Get-ChildItem -LiteralPath $pageRoot -Recurse -Filter '*.json') {
 $relative=[IO.Path]::GetRelativePath($root,$file.FullName).Replace('\','/')
 if($relative -notin $p.deletes){$candidates[$relative]=Get-Content -LiteralPath $file.FullName -Raw|ConvertFrom-Json -AsHashtable}
}
foreach($entry in $p.writes.GetEnumerator()) {$candidates[$entry.Key]=$entry.Value}
foreach($entry in $candidates.GetEnumerator()) {
 $value=$entry.Value
 Check-References $value @{}
 if($entry.Key.EndsWith('/visual.json')) {
  # Declared 2.12 is unavailable in the existing schema cache. Compatibility check only.
  $schema='topevo-visual-bundle.json'
  $copy=$value|ConvertTo-Json -Depth 100|ConvertFrom-Json -AsHashtable
  $copy['$schema']='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json'
 } elseif($entry.Key.EndsWith('/page.json')) {
  $schema='topevo-page-bundle.json';$copy=$value
 } else {continue} # External manifests are not PBIR.
 if(!(Test-Json -Json ($copy|ConvertTo-Json -Depth 100) -SchemaFile (Join-Path $SchemaDirectory $schema))){throw "Invalid PBIR: $($entry.Key)"}
}
$report=Get-Content (Join-Path $root ($p.report+'/definition/report.json')) -Raw
if(!(Test-Json -Json $report -SchemaFile (Join-Path $SchemaDirectory 'topevo-report-bundle.json'))){throw 'Invalid report definition'}
if(!(Test-Json -Json (Get-Content (Join-Path $root 'Templates/Theme/TopEvo.json') -Raw) -SchemaFile (Join-Path $SchemaDirectory 'topevo-theme-schema-2.150.json'))){throw 'Invalid canonical theme'}
'PASS: Microsoft TOM parsing, candidate model references, report/page/visual compatibility schemas, canonical theme and unchanged input hashes. Desktop rendering not tested.'
