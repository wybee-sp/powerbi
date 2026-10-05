"""Behavioral tests in isolated fixtures; no customer data or live report writes."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from generate import GenerationError, apply_plan, build_plan, encode, digest

ROOT = Path(__file__).resolve().parents[2]
BINDINGS = 'Templates/Sales/overview.bindings.json'
LAYOUT = 'Templates/PageTemplates/overview.layout.json'
REPORT = 'Templates/Sales/Sales.Report'


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='topevo-generation-test-')
        self.root = Path(self.tmp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        # Only repository definitions; deliberately exclude local model caches and exports.
        folders = ['Templates/Theme', 'Templates/Localization', 'Templates/PageTemplates', 'Templates/TopEvoAnalytics.Report', 'Templates/Sales/Sales.Report', 'Templates/TopEvoAnalytics.SemanticModel/definition']
        for folder in folders:
            for source in (ROOT / folder).rglob('*'):
                if source.is_file() and '.pbi' not in source.parts and (source.suffix in ('.json', '.tmdl', '.pbir', '.md') or source.name == '.platform'):
                    target = self.root / source.relative_to(ROOT)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, target)
        self.write(BINDINGS, json.loads((ROOT / BINDINGS).read_text(encoding='utf-8')))

    def tearDown(self):
        self.tmp.cleanup()

    def read(self, name):
        return json.loads((self.root / name).read_text(encoding='utf-8'))

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(encode(value))

    def plan(self):
        return build_plan(self.root, BINDINGS)

    def approve_fixture(self):
        candidate = self.plan()
        layout = self.read(LAYOUT)
        layout['review'] = dict(status='APPROVED', desktopBuild='TEST FIXTURE ONLY', evidence='Synthetic approval for testing write safety, not a rendering claim', fingerprint=candidate['layoutFingerprint'])
        self.write(LAYOUT, layout)
        return self.plan()

    def test_pending_cannot_write(self):
        b = self.read(BINDINGS)
        b.pop('variant', None)
        self.write(BINDINGS, b)
        before = (self.root / REPORT / '.platform').read_bytes()
        with self.assertRaisesRegex(GenerationError, 'Desktop approval'):
            apply_plan(self.root, self.plan(), lambda p: self.fail('Validator must not run before approval'))
        self.assertEqual(before, (self.root / REPORT / '.platform').read_bytes())

    def test_equivalent_adoption_is_byte_preserving_and_idempotent(self):
        files = list((self.root / REPORT / 'definition').rglob('*.json'))
        before = {str(p): p.read_bytes() for p in files}
        plan = self.plan()
        self.assertTrue(plan['pbirEquivalent'])
        self.assertTrue(plan['applyEligible'])
        self.assertFalse(any('/definition/' in p for p in plan['writes']))
        apply_plan(self.root, plan, lambda p: None)
        self.assertEqual(before, {str(p): p.read_bytes() for p in files})
        self.assertEqual({}, self.plan()['writes'])

    def test_schema_rejects_unknown_properties_and_wrong_types(self):
        original = self.read(LAYOUT)
        for edit in ({'extends': 'unsupported'}, {'version': '1'}):
            layout = copy.deepcopy(original)
            layout.update(edit)
            self.write(LAYOUT, layout)
            with self.assertRaisesRegex(GenerationError, 'Invalid layout schema'):
                self.plan()

    def test_central_change_propagates_after_review_preserving_bindings(self):
        layout = self.read(LAYOUT)
        layout['slots']['chart.trend']['position']['height'] = 216
        self.write(LAYOUT, layout)
        self.assertFalse(self.plan()['applyEligible'])
        plan = self.approve_fixture()
        b = self.read(BINDINGS)['components']['chart.trend']
        path = REPORT + '/definition/pages/ReportSection/visuals/' + b['id'] + '/visual.json'
        self.assertEqual(216, plan['writes'][path]['position']['height'])
        self.assertEqual(b['query'], plan['writes'][path]['visual']['query'])
        apply_plan(self.root, plan, lambda p: None)
        self.assertEqual({}, self.plan()['writes'])

    def test_custom_and_unclassified_are_protected(self):
        original = self.read(BINDINGS)
        for level in ('report', 'page'):
            for classification in ('CUSTOM', None):
                b = copy.deepcopy(original)
                target = b if level == 'report' else b['page']
                target['classification'] = classification
                self.write(BINDINGS, b)
                with self.assertRaisesRegex(GenerationError, 'CUSTOM or unclassified'):
                    self.plan()

    def test_missing_measure_is_error_not_placeholder(self):
        b = self.read(BINDINGS)
        b['components']['chart.trend']['query']['queryState']['Y']['projections'][0]['field']['Measure']['Property'] = 'Invented revenue'
        self.write(BINDINGS, b)
        with self.assertRaisesRegex(GenerationError, 'Missing Measure'):
            self.plan()

    def test_kpi_counts_zero_to_four_and_stable_new_ids(self):
        original = self.read(BINDINGS)
        for count in range(5):
            b = copy.deepcopy(original)
            exemplar = b['components']['kpi.invoiceCount']
            b['components'] = {k: v for k, v in b['components'].items() if not k.startswith('kpi.')}
            for i in range(count):
                binding = copy.deepcopy(exemplar)
                binding.pop('id')
                b['components']['kpi.test' + str(i)] = binding
            self.write(BINDINGS, b)
            p = self.plan()
            cards = [v for name, v in p['writes'].items() if name.endswith('/visual.json') and v['visual']['visualType'] == 'cardVisual']
            self.assertEqual(count, len(cards))
            if count:
                width = (1232 - 16 * (count - 1)) / count
                self.assertTrue(all(v['position']['width'] == width for v in cards))
                self.assertEqual(count, len({v['name'] for v in cards}))
            self.assertEqual(p, self.plan())

    def test_optional_component_removal_repairs_interactions(self):
        b = self.read(BINDINGS)
        removed = b['components'].pop('chart.ranking')['id']
        self.write(BINDINGS, b)
        p = self.plan()
        self.assertTrue(any(removed in path for path in p['deletes']))
        page = p['writes'][REPORT + '/definition/pages/ReportSection/page.json']
        self.assertFalse(any(removed in (i['source'], i['target']) for i in page['visualInteractions']))

    def test_apply_idempotent_preserves_identity_model_custom_and_bindings(self):
        protected = [REPORT + '/.platform', REPORT + '/definition.pbir', REPORT + '/definition/pages/pages.json', REPORT + '/definition/pages/cc2566e279b27d3608e1/page.json']
        protected += [p.relative_to(self.root).as_posix() for p in (self.root / 'Templates/TopEvoAnalytics.SemanticModel').rglob('*.tmdl')]
        before = {p: digest((self.root / p).read_bytes()) for p in protected}
        b = self.read(BINDINGS)
        p = self.approve_fixture()
        apply_plan(self.root, p, lambda candidate: None)  # Schema/TOM integration is tested separately.
        for role, binding in b['components'].items():
            visual = self.read(REPORT + '/definition/pages/ReportSection/visuals/' + binding['id'] + '/visual.json')
            if binding['query']:
                self.assertEqual(binding['query'], visual['visual']['query'])
        after = {p: digest((self.root / p).read_bytes()) for p in protected}
        self.assertEqual(before, after)
        second = self.plan()
        self.assertEqual({}, second['writes'])
        self.assertEqual([], second['deletes'])

    def test_custom_visual_and_id_reuse_are_rejected(self):
        b = self.read(BINDINGS)
        b['components']['chart.trend']['id'] = b['components']['chart.ranking']['id']
        self.write(BINDINGS, b)
        with self.assertRaisesRegex(GenerationError, 'identity'):
            self.plan()
        self.write(BINDINGS, json.loads((ROOT / BINDINGS).read_text(encoding='utf-8')))
        self.write(REPORT + '/definition/pages/ReportSection/visuals/abcdef1234567890abcd/visual.json', {'name': 'abcdef1234567890abcd'})
        with self.assertRaisesRegex(GenerationError, 'Unmanaged'):
            self.plan()

    def test_overlaps_and_stale_review(self):
        self.approve_fixture()
        layout = self.read(LAYOUT)
        layout['slots']['chart.trend']['position']['height'] -= 8
        self.write(LAYOUT, layout)
        self.assertFalse(self.plan()['applyEligible'])
        layout['slots']['chart.ranking']['position']['x'] = 24
        self.write(LAYOUT, layout)
        with self.assertRaisesRegex(GenerationError, 'Overlap'):
            self.plan()

    def test_stale_plan_cannot_write(self):
        plan = self.approve_fixture()
        b = self.read(BINDINGS)
        b['limitations'].append('Concurrent change')
        self.write(BINDINGS, b)
        with self.assertRaisesRegex(GenerationError, 'Inputs changed'):
            apply_plan(self.root, plan, lambda p: None)

    def test_unsafe_target_and_missing_label(self):
        b = self.read(BINDINGS)
        b['report'] = 'Customers/example/overrides/Example.Report'
        self.write(BINDINGS, b)
        with self.assertRaisesRegex(GenerationError, 'Only explicit module'):
            self.plan()
        b = json.loads((ROOT / BINDINGS).read_text(encoding='utf-8'))
        b['components']['header.title']['labels']['HeaderReceivablesOverview'] = 'MissingKey'
        self.write(BINDINGS, b)
        with self.assertRaisesRegex(GenerationError, 'Missing label'):
            self.plan()


if __name__ == '__main__':
    unittest.main()
