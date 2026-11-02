"""Pure phase fixtures using explicit historical data; never executes UI."""
import copy
import json
from pathlib import Path
import unittest

from agate_prep_phase import BASE_EV, FINAL_MOVES, PRE_EV, ROOT, plan


def snapshot(mid=355):
    s = json.loads((ROOT / "notes/Glass-post-gauntlet-attempt-1-status.json").read_text())
    s["map"] = mid
    return s


def training(spa):
    s = snapshot(519)
    cf = next(m for m in s["party"] if m["species"] == "COFAGRIGUS")
    cf.update(nature="TIMID", item="POWERLENS", ev=list(PRE_EV), hp=252, totalhp=252)
    cf["ev"][3] = spa
    cf["moves"] = [dict(move=m, pp=15) for m in FINAL_MOVES]
    return s


class AgatePrepTest(unittest.TestCase):
    def test_source_correct_shop_targets_and_budget(self):
        s = snapshot()
        s["bag"]["contents"].update(POMEGBERRY=0, POWERLENS=0)
        cmds = plan("shops", s)
        self.assertIn({"script": "eventq", "args": [355, 136, "talk"]}, cmds)
        self.assertIn({"script": "eventq", "args": [355, 83, "talk"]}, cmds)
        s["trainer"]["money"] = 16999
        with self.assertRaises(ValueError):
            plan("shops", s)

    def test_already_owned_supplies_not_purchased_twice(self):
        s = snapshot()
        s["bag"]["contents"].update(POMEGBERRY=4, POWERLENS=1)
        self.assertEqual(plan("shops", s), [])

    def test_collected_old_scale_never_used(self):
        s = snapshot(715)
        s["bag"]["contents"]["HEARTSCALE"] = 0
        cmds = plan("scale", s)
        self.assertEqual(cmds[0]["args"], [715, 64, "item"])

    def test_build_exact_replacements_and_partial_state_rejected(self):
        s = snapshot()
        s["bag"]["contents"].update(TIMIDMINT=1, POMEGBERRY=4, TM97=1,
                                       HEARTSCALE=1, POWERLENS=1)
        cmds = plan("build", s)
        self.assertIn({"internal": "hex-reminder", "index": 6}, cmds)
        self.assertIn({"script": "teach_machine", "args": ["TM97", "Cofagrigus", "Dark Pulse", 3]}, cmds)
        cf = next(m for m in s["party"] if m["species"] == "COFAGRIGUS")
        cf["ev"][0] = 232
        with self.assertRaises(ValueError):
            plan("build", s)

    def test_single_ko_pilot_before_two_ko_finish(self):
        first = plan("training-pilot", training(0))
        last = plan("training-finish", training(32))
        self.assertEqual(next(c for c in first if c["script"] == "train_wild_bulk")["args"][:3],
                         ["Cofagrigus", 3, 1])
        self.assertEqual(next(c for c in last if c["script"] == "train_wild_bulk")["args"][:3],
                         ["Cofagrigus", 3, 2])
        with self.assertRaises(ValueError):
            plan("training-finish", training(80))
        with self.assertRaises(ValueError):
            plan("training-finish", training(128))

    def test_mint_flag_overrides_original_nature(self):
        s=training(0)
        cf=next(m for m in s["party"] if m["species"]=="COFAGRIGUS")
        cf.update(nature="CALM", natureflag="TIMID")
        self.assertTrue(plan("training-pilot",s))
        cf["natureflag"]="CALM"
        with self.assertRaises(ValueError): plan("training-pilot",s)

    def test_changed_actor_slot_or_status_fails_training(self):
        s = training(0)
        cf = next(m for m in s["party"] if m["species"] == "COFAGRIGUS")
        cf["moves"][3]["move"] = "DESTINYBOND"
        with self.assertRaises(ValueError):
            plan("training-pilot", s)
        s = training(0)
        cf = next(m for m in s["party"] if m["species"] == "COFAGRIGUS")
        cf["status"] = "POISON"
        with self.assertRaises(ValueError):
            plan("training-pilot", s)


if __name__ == "__main__":
    unittest.main()
