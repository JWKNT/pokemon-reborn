"""Fixture checks for inventory/log reconciliation; no game or live-log access."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from reconcile_glass_items import reconcile, native_inventory


def status(contents, held=None):
    return {'bag': {'type': 'PokemonBag', 'contents': contents},
            'party': [{'item': item} for item in (held or [None] * 6)]}


class ReconciliationTests(unittest.TestCase):
    def test_balanced_three_rounds_with_story_and_held_transfer_exclusions(self):
        before = status({'FULLHEAL': 8, 'ULTRAPOTION': 15, 'XSPECIAL': 6,
                         'SAPPHIREBRACELETS': 1, 'SPELLTAG': 1})
        after = status({'FULLHEAL': 7, 'ULTRAPOTION': 13, 'XSPECIAL': 5,
                        'SAPPHIREBRACELETS': 0, 'SPELLTAG': 0},
                       ['SPELLTAG', None, None, None, None, None])
        logs = ['Cofagrigus: use item Full Heal on Cofagrigus\n[Player used Full Heal]\n',
                '[Player used X Sp. Atk]\n[Player used Ultra Potion]\n',
                '[Player used Ultra Potion]\n']
        original = copy.deepcopy((before, after, logs))
        report = reconcile(before, after, logs)
        self.assertEqual(report['status'], 'verified_counts')
        self.assertEqual(report['per_round'][1]['item_usage'],
                         [{'name': 'Ultra Potion', 'count': 1}, {'name': 'X Sp. Atk', 'count': 1}])
        self.assertEqual({x['item_id']: x['excluded_as'] for x in report['ignored_bag_changes']},
                         {'SAPPHIREBRACELETS': 'story_key_item', 'SPELLTAG': 'held_transfer_candidate'})
        self.assertEqual((before, after, logs), original)

    def test_lemonade_matches_native_consumption_and_rejects_unlogged_use(self):
        logs=['[Player used Lemonade]\n']*5
        report=reconcile(status({'LEMONADE':6}),status({'LEMONADE':1}),[''.join(logs)],expected_rounds=1)
        self.assertEqual(report['status'],'verified_counts')
        self.assertEqual(report['per_round'][0]['item_usage'],[{'name':'Lemonade','count':5}])
        report=reconcile(status({'LEMONADE':6}),status({'LEMONADE':0}),[''.join(logs)],expected_rounds=1)
        self.assertEqual(report['status'],'mismatch')

    def test_refund_difference_fails_without_assigning_a_round(self):
        report = reconcile(status({'FULLHEAL': 8}), status({'FULLHEAL': 7}),
                           ['[Player used Full Heal]\n', '', '[Player used Full Heal]\n'])
        self.assertEqual(report['status'], 'mismatch')
        self.assertTrue(all('item_usage' not in row for row in report['per_round']))
        self.assertEqual(report['aggregate'][0]['logged_executions'], 2)
        self.assertEqual(report['aggregate'][0]['bag_decline'], 1)

    def test_unlogged_decrease_or_inflow_fails(self):
        for qty in (7, 9):
            with self.subTest(qty=qty):
                report = reconcile(status({'FULLHEAL': 8}), status({'FULLHEAL': qty}), ['', '', ''])
                self.assertEqual(report['status'], 'mismatch')

    def test_reusable_or_unknown_item_fails(self):
        report = reconcile(status({}), status({}), ['[Player used Blue Flute]\n', '', ''])
        self.assertEqual(report['status'], 'mismatch')
        self.assertEqual(report['errors'][0]['names'], ['Blue Flute'])

    def test_tracked_consumable_held_transfer_requires_review(self):
        report = reconcile(status({'FULLHEAL': 8}),
                           status({'FULLHEAL': 7}, ['FULLHEAL', None, None, None, None, None]),
                           ['[Player used Full Heal]\n', '', ''])
        self.assertEqual(report['status'], 'mismatch')
        self.assertFalse(report['aggregate'][0]['matched'])

    def test_native_shape_and_exact_three_rounds_required(self):
        with self.assertRaises(ValueError):
            native_inventory({'bag': {'contents': {}}, 'party': []})
        with self.assertRaises(ValueError):
            reconcile(status({}), status({}), ['', ''])
        with self.assertRaises(ValueError):
            native_inventory(status({'FULLHEAL': True}))

    def test_cli_exit_codes_and_stdout_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            before, after = root / 'before.json', root / 'after.json'
            before.write_text(json.dumps(status({'FULLHEAL': 8})))
            after.write_text(json.dumps(status({'FULLHEAL': 7})))
            logs = [root / f'completed-round-{i}.txt' for i in range(1, 4)]
            for i, log in enumerate(logs):
                log.write_text('[Player used Full Heal]\n' if i == 0 else '')
            cmd = [sys.executable, str(Path(__file__).with_name('reconcile_glass_items.py')),
                   str(before), str(after), *map(str, logs)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'verified_counts')
            after.write_text(json.dumps(status({'FULLHEAL': 8})))
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'mismatch')


if __name__ == '__main__':
    unittest.main()
