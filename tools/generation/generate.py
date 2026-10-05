"""TopEvo Overview synchronization. Default: read-only candidate plan, never deployment."""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import tempfile
import uuid
from functools import lru_cache
from pathlib import Path


class GenerationError(ValueError):
    pass


def check(condition, message):
    if not condition:
        raise GenerationError(message)


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe(root, name):
    path = (root / name).resolve()
    check(not Path(name).is_absolute() and path.is_relative_to(root.resolve()), f'Unsafe path: {name}')
    return path


def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def literal(value):
    return {'expr': {'Literal': {'Value': value}}}


@lru_cache(maxsize=32)
def validate_layout_schema(document, schema):
    # PowerShell's standards-based JSON Schema validator; no network resolution.
    with tempfile.TemporaryDirectory(prefix='topevo-layout-schema-') as tmp:
        path = Path(tmp) / 'schema.json'
        path.write_bytes(schema)
        result = subprocess.run(['pwsh', '-NoProfile', '-Command',
            "$ErrorActionPreference='Stop'; $json=[Console]::In.ReadToEnd(); "
            "if (!(Test-Json -Json $json -SchemaFile '" + str(path).replace("'", "''") + "')) { exit 1 }"], input=document, capture_output=True)
        check(result.returncode == 0, 'Invalid layout schema: ' + result.stderr.decode('utf-8', errors='replace'))


def format_variant(visual, spec):
    for patch in spec.get('formatPatches', []):
        path = patch['path']
        check(path[0] in ('visualType', 'objects', 'visualContainerObjects'), 'Variant may only change visual formatting')
        parent = visual['visual']
        for key in path[:-1]:
            parent = parent[key]
        if patch.get('remove'):
            parent.pop(path[-1], None)
        else:
            parent[path[-1]] = copy.deepcopy(patch['value'])


class Reader:
    def __init__(self, root):
        self.root, self.inputs = root.resolve(), {}

    def data(self, name):
        data = safe(self.root, name).read_bytes()
        self.inputs[name] = digest(data)
        return data

    def json(self, name):
        return json.loads(self.data(name).decode('utf-8-sig'))


def symbols(reader, model):
    # Symbol inventory only: Microsoft TOM performs full TMDL parsing before apply.
    result = set()
    for path in sorted(safe(reader.root, model + '/definition').rglob('*.tmdl')):
        text = reader.data(path.relative_to(reader.root).as_posix()).decode('utf-8-sig')
        table = re.search(r'^table (.+)$', text, re.M)
        if table:
            unquote = lambda s: s.strip().strip("'").replace("''", "'")
            for kind, name in re.findall(r'^\t(column|measure) (.+?)(?: =.*)?$', text, re.M):
                result.add((kind.capitalize(), unquote(table[1]), unquote(name)))
    return result


def validate_refs(value, known):
    for node in nodes(value):
        for kind in ('Column', 'Measure'):
            ref = node.get(kind, {})
            table = ref.get('Expression', {}).get('SourceRef', {}).get('Entity') if isinstance(ref, dict) else None
            if table:
                check((kind, table, ref['Property']) in known, f'Missing {kind}: {table}[{ref["Property"]}]')


def relabel(value, mapping):
    if isinstance(value, str):
        for old, new in mapping.items():
            if value == old:
                return new
            if value == '_ReportLabels.' + old:
                return '_ReportLabels.' + new
        return value
    if isinstance(value, list):
        return [relabel(v, mapping) for v in value]
    if isinstance(value, dict):
        return {k: relabel(v, mapping) for k, v in value.items()}
    return value


def geometry(visuals, layout):
    check(layout['canvas'] == {'width': 1280, 'height': 720}, 'Overview canvas must be 1280 x 720')
    positions = {role: v['position'] for role, v in visuals.items()}
    for role, p in positions.items():
        check(all(isinstance(p[k], (int, float)) for k in ('x', 'y', 'width', 'height')), 'Invalid geometry')
        check(0 <= p['x'] and 0 <= p['y'] and p['width'] > 0 and p['height'] > 0 and p['x'] + p['width'] <= 1280 and p['y'] + p['height'] <= 720, f'Out of bounds: {role}')
    for role, p in positions.items():
        check(p['y'] % 8 == 0 and p['height'] % 8 == 0, f'Off vertical grid: {role}')
        if role not in ('header.title', 'filter.period', 'control.granularity'):
            check((p['x'] - 24) % 104 == 0 and (p['width'] + 16) % 104 == 0, f'Off column grid: {role}')
    items = list(positions.items())
    for i, (role, a) in enumerate(items):
        for other, b in items[i + 1:]:
            overlap = max(a['x'], b['x']) < min(a['x'] + a['width'], b['x'] + b['width']) and max(a['y'], b['y']) < min(a['y'] + a['height'], b['y'] + b['height'])
            check(not overlap, f'Overlap: {role}, {other}')
            if max(a['x'], b['x']) < min(a['x'] + a['width'], b['x'] + b['width']):
                gap = max(a['y'], b['y']) - min(a['y'] + a['height'], b['y'] + b['height'])
                minimum = 8 if {role, other} & {'header.title', 'navigation.pages'} else 16
                check(gap >= minimum, f'Insufficient vertical gutter: {role}, {other}')
            if max(a['y'], b['y']) < min(a['y'] + a['height'], b['y'] + b['height']):
                gap = max(a['x'], b['x']) - min(a['x'] + a['width'], b['x'] + b['width'])
                minimum = 0 if {role, other} == {'filter.period', 'control.granularity'} else 16
                check(gap >= minimum, f'Insufficient horizontal gutter: {role}, {other}')
    order = [positions[k] for k in ('filter.branch', 'filter.period', 'control.granularity', 'filter.customer')]
    check(all(p['y'] == 72 and p['height'] == 56 for p in order), 'Primary filters must retain y72/h56')
    check(all(a['x'] + a['width'] <= b['x'] for a, b in zip(order, order[1:])), 'Invalid primary filter order')
    check(order[1]['x'] + order[1]['width'] == order[2]['x'] and order[2]['width'] >= 536, 'TimeControl must remain adjacent with five visible grains')
    h = positions['header.title']
    check(h['y'] + h['height'] + 8 <= 72, 'Header/filter clearance below 8 px')


def build_plan(root, binding_path):
    r = Reader(root)
    b = r.json(binding_path)
    check(b.get('version') == 1, 'Unsupported bindings version')
    check(b.get('classification') == 'STANDARD' and b.get('page', {}).get('classification') == 'STANDARD', 'CUSTOM or unclassified report/page: refused')
    report, pid = b['report'], b['page']['id']
    parts = Path(report).parts
    check(len(parts) == 3 and parts[0] == 'Templates' and parts[-1].endswith('.Report'), 'Only explicit module reports under Templates are supported')
    check(re.fullmatch(r'[A-Za-z0-9_]+', pid) and pid not in b.get('protectedPages', {}), 'Unsafe or protected page')
    model = 'Templates/TopEvoAnalytics.SemanticModel'
    check(b['semanticModel'] == model, 'Shared semantic model required')
    layout = r.json(b['layout'])
    validate_layout_schema(encode(layout), r.data('Templates/PageTemplates/overview.layout.schema.json'))
    variant_name = b.get('variant')
    check(variant_name is None or variant_name in layout['variants'], 'Unknown layout variant')
    variant = layout['variants'].get(variant_name, {}).get('slots', {})
    check(layout.get('version') == 1 and layout['name'] == 'overview', 'Unsupported layout')
    check(layout['emptySlotPolicy'] == 'omit-without-reflow', 'Unsupported optional-slot policy')
    check(layout['interactionPolicy'] == 'primary-filters-all-analytics; granularity-trend-only; no-incoming-granularity', 'Unsupported interaction policy')
    check(layout['theme'] == 'Templates/Theme/TopEvo.json', 'Canonical theme required')
    check(layout['reference'] == 'Templates/TopEvoAnalytics.Report', 'Canonical Golden Sample required')
    check(r.json(report + '/.platform')['config']['logicalId'] == b['logicalId'], 'Report identity mismatch')
    reference = r.json(report + '/definition.pbir')['datasetReference']['byPath']['path']
    check((safe(r.root, report) / reference).resolve() == safe(r.root, model), 'Invalid shared model reference')
    for path in sorted(safe(r.root, report + '/definition').rglob('*.json')):
        r.data(path.relative_to(r.root).as_posix())
    settings = r.json(report + '/definition/report.json')
    locale_filters = [f for f in settings.get('filterConfig', {}).get('filters', []) if f.get('field', {}).get('Column', {}).get('Expression', {}).get('SourceRef', {}).get('Entity') == 'Time Granularity' and f['field']['Column']['Property'] == 'Locale']
    check(len(locale_filters) == 1 and locale_filters[0]['filter']['Where'][0]['Condition']['In']['Values'][0][0]['Literal']['Value'] == "'en-US'", 'A single English initial Time Granularity locale filter is required')
    themes = [i for p in settings['resourcePackages'] if p['type'] == 'RegisteredResources' for i in p['items'] if i['type'] == 'CustomTheme']
    check(len(themes) == 1, 'Expected one custom theme')
    check(r.json(report + '/StaticResources/RegisteredResources/' + themes[0]['path']) == r.json(layout['theme']), 'Theme differs; report-wide theme migration requires separate review to protect CUSTOM pages')
    known = symbols(r, model)
    labels = r.json('Templates/Localization/labels.json')['labels']
    metadata = r.json('Templates/Localization/metadata.json')['entries']
    page_path = report + '/definition/pages/' + pid
    page = r.json(page_path + '/page.json')
    check(page['name'] == pid and pid in r.json(report + '/definition/pages/pages.json')['pageOrder'], 'Page identity/order mismatch')
    manifest = r.json(report + '/COMPONENTS.json')
    check(manifest['page'] == pid, 'Only the manifest Overview is supported')
    registry_path = report + '/GENERATION.json'
    registry = r.json(registry_path) if safe(r.root, registry_path).exists() else None
    if registry:
        check(registry.get('classification') == 'STANDARD' and registry['page'] == pid, 'Registry protection mismatch')
    owned = registry['visuals'] if registry else {c['role']: c['id'] for c in manifest['components']}
    other_pages = {p.name for p in safe(r.root, report + '/definition/pages').iterdir() if p.is_dir()} - {pid}
    check(other_pages <= set(b.get('protectedPages', {})), 'Other pages need explicit protection classification')
    present = {p.parent.name for p in safe(r.root, page_path + '/visuals').glob('*/visual.json')}
    check(present == set(owned.values()), 'Unmanaged/missing visuals: preserve local customization and reconcile explicitly')
    required = set(layout['slots']) - {'kpi'} - set(layout['optionalSlots'])
    check(required <= set(b['components']), 'Missing required component')
    kpis = [k for k, v in b['components'].items() if v['slot'] == 'kpi']
    check(len(kpis) <= 4, 'More than four KPIs requires a page-design decision')
    check(layout['kpiRow']['x'] == 24 and layout['kpiRow']['width'] == 1232 and layout['kpiRow']['gutter'] == 16, 'KPI row must use TopEvo margins and 16 px gutters')
    sources = {}
    fingerprints = {'variant': variant_name, 'layout': {k: v for k, v in layout.items() if k != 'review'}, 'sources': {}, 'theme': digest(r.data(layout['theme'])), 'designSystem': digest(r.data('Templates/Theme/DESIGN_SYSTEM.md'))}
    for slot, spec in layout['slots'].items():
        check(safe(r.root, spec['source']).is_relative_to(safe(r.root, layout['reference'] + '/definition/pages')), 'Component source must be Golden Sample')
        sources[slot] = r.json(spec['source'])
        fingerprints['sources'][slot] = digest(encode(sources[slot]))
    fingerprint = digest(encode(fingerprints))
    source_ids = {r.json(p.relative_to(r.root).as_posix())['name'] for p in safe(r.root, layout['reference'] + '/definition/pages').glob('*/visuals/*/visual.json')}
    visuals = {}
    for role, binding in b['components'].items():
        slot = binding['slot']
        check(slot in sources and (slot == role or slot == 'kpi' and role.startswith('kpi.')), 'Invalid component slot')
        check(not ({'position', 'width', 'height', 'x', 'y'} & set(binding)), 'Geometry belongs in layout')
        check('query' in binding and 'labels' in binding, 'Explicit query/labels required')
        vid = binding.get('id') or uuid.uuid5(uuid.UUID(b['logicalId']), pid + ':' + role).hex[:20]
        check(re.fullmatch(r'[0-9a-f]{20}', vid) and vid not in source_ids, 'Invalid/copied Golden Sample visual ID')
        check(vid == owned[role] if role in owned else vid not in present, 'Visual identity collision/change')
        for key in binding['labels'].values():
            check(key in labels and labels[key].get('en-US') and ('Measure', '_ReportLabels', key) in known, f'Missing label/fallback: {key}')
        if slot in ('filter.period', 'control.granularity'):
            check(binding['query'] == sources[slot]['visual']['query'], 'TimeControl must retain canonical field and sort bindings')
        visual = copy.deepcopy(sources[slot])
        format_variant(visual, variant.get(slot, {}))
        visual['name'] = vid
        visual.pop('filterConfig', None)  # Do not inherit Receivables parameter selections.
        v = visual['visual']
        v.pop('query', None)
        if binding['query'] and not (slot == 'header.title' and v['visualType'] == 'textbox'):
            v['query'] = copy.deepcopy(binding['query'])
        check(slot in ('header.title', 'navigation.pages') or binding['query'], 'Missing business query')
        v = relabel(v, binding['labels'])
        visual['visual'] = v
        if slot == 'kpi':
            projections = v['query']['queryState']['Data']['projections']
            check(len(projections) == 1 and 'Measure' in projections[0]['field'], 'KPI needs one existing measure')
            ref = projections[0]['field']['Measure']
            table, name = ref['Expression']['SourceRef']['Entity'], ref['Property']
            ex = b.get('legacyMeasureException', {})
            check(table == '_Measures' or table == ex.get('table') and name in ex.get('measures', []) and ex.get('reason'), 'KPI outside _Measures needs documented existing-model exception')
            check(any(e['kind'] == 'measure' and e['table'] == table and e.get('name') == name and e['captions'].get('en-US') for e in metadata), 'Uncurated KPI measure')
            check(set(binding.get('numberFormat', {})) <= {'labelDisplayUnits', 'labelPrecision'}, 'Only numeric units/precision belong in numberFormat')
            v['objects']['value'][0]['properties'].update(binding.get('numberFormat', {}))
            row, n = layout['kpiRow'], kpis.index(role)
            width = (row['width'] - row['gutter'] * (len(kpis) - 1)) / len(kpis)
            visual['position'] = dict(x=row['x'] + n * (width + row['gutter']), y=row['y'], width=width, height=row['height'], z=6000 + n * 1000, tabOrder=6000 + n * 1000)
        else:
            visual['position'] = copy.deepcopy(variant.get(slot, {}).get('position', layout['slots'][slot]['position']))
        if slot == 'table.summary':
            projections = v['query']['queryState']['Values']['projections']
            widths = layout['summaryWidths'].get(str(len(projections)))
            check(widths is not None, 'No summary-column width variant')
            check(all(w > 0 for w in widths) and sum(widths) <= visual['position']['width'] - 32, 'Summary columns exceed available width')
            v['objects']['columnWidth'] = [{'selector': {'metadata': p['queryRef']}, 'properties': {'value': literal(str(w) + 'D')}} for p, w in zip(projections, widths)]
        validate_refs(visual, known)
        for node in nodes(v):
            ref = node.get('Measure', {})
            if ref.get('Expression', {}).get('SourceRef', {}).get('Entity') == '_ReportLabels':
                check(ref['Property'] in binding['labels'].values(), 'Unmapped source label')
        visuals[role] = visual
    check(len({v['name'] for v in visuals.values()}) == len(visuals), 'Duplicate IDs')
    other_ids = {p.parent.name for page_name in other_pages for p in safe(r.root, report + '/definition/pages/' + page_name).glob('visuals/*/visual.json')}
    check(not (other_ids & {v['name'] for v in visuals.values()}), 'Visual ID collision with protected page')
    geometry(visuals, layout)
    period = visuals['filter.period']['visual']['query']['queryState']['Values']['projections'][0]['field']
    check(period == {'Column': {'Expression': {'SourceRef': {'Entity': 'Date'}}, 'Property': 'Date'}}, 'Canonical Date[Date] required')
    if 'chart.trend' in visuals:
        axis = visuals['chart.trend']['visual']['query']['queryState']['Category']
        check(axis['fieldParameters'][0]['parameterExpr']['Column']['Expression']['SourceRef']['Entity'] == 'Time Granularity', 'Shared time parameter required')
    analytics = [k for k in visuals if k.startswith(('kpi.', 'chart.', 'table.'))]
    interactions = []
    for source in ('filter.branch', 'filter.period', 'filter.customer'):
        interactions += [{'source': visuals[source]['name'], 'target': visuals[target]['name'], 'type': 'DataFilter'} for target in analytics]
    for role in visuals:
        if role != 'control.granularity':
            interactions += [{'source': visuals[role]['name'], 'target': visuals['control.granularity']['name'], 'type': 'NoFilter'}, {'source': visuals['control.granularity']['name'], 'target': visuals[role]['name'], 'type': 'DataFilter' if role == 'chart.trend' else 'NoFilter'}]
    page.update(layout['canvas'])
    generated_pairs = {(i['source'], i['target']) for i in interactions}
    active_ids = {v['name'] for v in visuals.values()}
    interactions += [i for i in page.get('visualInteractions', [])
                     if (i['source'], i['target']) not in generated_pairs
                     and i['source'] in active_ids and i['target'] in active_ids]
    # Array order does not change interaction semantics. Preserve original order
    # when the generated interaction set is identical, avoiding needless rewrites.
    interaction_key = lambda i: (i['source'], i['target'], i['type'])
    if sorted(map(interaction_key, page.get('visualInteractions', []))) != sorted(map(interaction_key, interactions)):
        page['visualInteractions'] = interactions
    page['displayName'] = labels[b['page']['label']]['en-US']
    writes = {page_path + '/page.json': page}
    writes.update({page_path + '/visuals/' + v['name'] + '/visual.json': v for v in visuals.values()})
    deletes = [page_path + '/visuals/' + vid + '/visual.json' for vid in sorted(set(owned.values()) - {v['name'] for v in visuals.values()})]
    check(not deletes or not list(safe(r.root, report + '/definition').glob('bookmarks/**/*.json')), 'Removing bookmarked visuals requires explicit dependency migration')
    equivalent = not deletes and all(r.json(p) == v for p, v in writes.items() if safe(r.root, p).exists()) and all(safe(r.root, p).exists() for p in writes)
    manifest['status'] = 'Synchronized; rendering evidence recorded separately'
    manifest['components'] = [dict(role=role, id=v['name'], type=v['visual']['visualType'], position=v['position'], bindings=v['visual'].get('query', {}).get('queryState', {}), status='Synchronized component') for role, v in visuals.items()]
    manifest['kpiLayout'] = {'count': len(kpis), 'gutter': layout['kpiRow']['gutter']}
    for group in manifest.get('componentGroups', []):
        group['status'] = 'Synchronized component group'
    manifest['localization']['runtimeValidation'] = 'No runtime validation claimed by generation; see documented Desktop/embedded evidence'
    writes[report + '/COMPONENTS.json'] = manifest
    writes[registry_path] = {'version': 1, 'classification': 'STANDARD', 'page': pid, 'bindings': binding_path, 'variant': variant_name, 'layoutFingerprint': fingerprint, 'visuals': {k: v['name'] for k, v in visuals.items()}}
    writes = {p: v for p, v in writes.items() if not safe(r.root, p).exists() or json.loads(safe(r.root, p).read_text(encoding='utf-8-sig')) != v}
    review = layout.get('review', {})
    approved = review.get('status') == 'APPROVED' and review.get('fingerprint') == fingerprint and review.get('desktopBuild') and review.get('evidence')
    return {'version': 1, 'bindings': binding_path, 'report': report, 'page': pid, 'classification': 'STANDARD', 'layoutFingerprint': fingerprint, 'pbirEquivalent': equivalent, 'applyEligible': bool(approved or equivalent), 'blockers': [] if approved or equivalent else ['Current layout/component fingerprint needs recorded Golden Sample Desktop approval'], 'limitations': b.get('limitations', []), 'inputs': r.inputs, 'writes': writes, 'deletes': deletes}


def apply_plan(root, plan, validator):
    check(plan['applyEligible'], '; '.join(plan['blockers']))
    validator(plan)
    check(build_plan(root, plan['bindings']) == plan, 'Inputs changed after planning/validation')
    backups = {p: safe(root, p).read_bytes() if safe(root, p).exists() else None for p in list(plan['writes']) + plan['deletes']}
    try:
        for p, value in plan['writes'].items():
            path = safe(root, p)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(encode(value))
        for p in plan['deletes']:
            safe(root, p).unlink()  # Only explicitly owned visual.json files; never recursive deletion.
    except Exception:
        for p, previous in backups.items():
            if previous is None:
                safe(root, p).unlink(missing_ok=True)
            else:
                safe(root, p).write_bytes(previous)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bindings', default='Templates/Sales/overview.bindings.json')
    parser.add_argument('--plan', type=Path, help='External JSON file containing candidate PBIR and changes')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--tom-library', type=Path)
    parser.add_argument('--schemas', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    try:
        plan = build_plan(root, args.bindings)
        if args.plan:
            check(not args.plan.resolve().is_relative_to(root), 'Review plans must stay outside the repository')
            args.plan.write_bytes(encode(plan))
        print(json.dumps({k: plan[k] for k in ('layoutFingerprint', 'pbirEquivalent', 'applyEligible', 'blockers', 'limitations')}, indent=2))
        for p in plan['writes']:
            print('WRITE ' + p)
        for p in plan['deletes']:
            print('REMOVE ' + p)
        if args.apply:
            check(args.tom_library and args.schemas, 'Apply requires --tom-library and --schemas')
            def validate(candidate):
                with tempfile.TemporaryDirectory(prefix='topevo-plan-') as tmp:
                    path = Path(tmp) / 'plan.json'
                    path.write_bytes(encode(candidate))
                    subprocess.run(['pwsh', '-NoProfile', '-File', str(root / 'tools/generation/Validate-Plan.ps1'), '-Plan', str(path), '-TomLibraryPath', str(args.tom_library), '-SchemaDirectory', str(args.schemas)], check=True)
            apply_plan(root, plan, validate)
            print('Applied. Module Desktop/embedded validation remains required.')
    except (GenerationError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Generation refused: {error}\n')


if __name__ == '__main__':
    main()
