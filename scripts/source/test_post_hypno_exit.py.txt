"""Pure guard tests; no UI, controls, native reads/writes or ongoing logs."""
import hashlib
import json
import pathlib
import tempfile
import unittest

from post_hypno_exit import ROOT, frozen_post_gate, no_battle_or_choice, prefix_at_first_touch


def event(eid, xy, command=101):
    return str(eid), {"x": xy[0], "y": xy[1], "trigger": 1,
                      "list": [{"code": command, "parameters": ["source"], "indent": 0}]}


class ExitGuards(unittest.TestCase):
    def test_first_meaningful_touch_truncates_before_later_inputs(self):
        value = {"map": 758, "events": dict([event(62, (1, 0)), event(89, (3, 0))])}
        keys, nodes, stop = prefix_at_first_touch(value, [(x, 0) for x in range(5)], ["right"] * 4, 56, "zel")
        self.assertEqual((keys, nodes, stop[0]), (["right"], [(0, 0), (1, 0)], 62))
        value["events"] = dict([event(999, (2, 0))])
        with self.assertRaises(ValueError):
            prefix_at_first_touch(value, [(x, 0) for x in range(5)], ["right"] * 4, 56, "zel")
        value["events"] = dict([event(35, (2, 0))])
        with self.assertRaises(ValueError):
            prefix_at_first_touch(value, [(x, 0) for x in range(5)], ["right"] * 4, 56, "shade")

    def test_only_inspected_anna_choice_and_no_future_battle(self):
        anna = [{"code": 102, "parameters": [["Yes", "No"], 2], "indent": 0}]
        no_battle_or_choice(anna, anna_choice=True)
        with self.assertRaises(ValueError):
            no_battle_or_choice(anna)
        with self.assertRaises(ValueError):
            no_battle_or_choice([{"code": 111, "parameters": [12, "pbTrainerBattle(:Solaris)"]}])

    def test_frozen_postbag_is_required_and_bound(self):
        with tempfile.TemporaryDirectory(prefix="post-hypno-proof-", dir=ROOT / "work") as directory:
            directory = pathlib.Path(directory)
            status_path, report_path = directory / "status.json", directory / "report.json"
            # Match status_full.rb's actual schema:1874 is deliberately absent
            # here; execute() separately checks the full navigation snapshot.
            status_path.write_text(json.dumps({"map": 758, "switches": {"183": True},
                                               "bag": {"type": "PokemonBag", "contents": {"ULTRAPOTION": 3}}}))
            report = {"status": "verified_counts", "errors": [], "native_save_inventories_verified": True,
                      "per_round": [{"major_id": 125}], "evidence": {"after": {"sha256": hashlib.sha256(status_path.read_bytes()).hexdigest()}}}
            report_path.write_text(json.dumps(report))
            self.assertEqual(frozen_post_gate(status_path, report_path)["map"], 758)
            status_path.write_text(status_path.read_text() + "\n")
            with self.assertRaises(ValueError):
                frozen_post_gate(status_path, report_path)


if __name__ == "__main__":
    unittest.main()
