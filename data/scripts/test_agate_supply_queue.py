"""Pure frozen/proposed fixtures and installed source reads; never controls game."""
import copy
import json
import unittest

from agate_supply_queue import (ROOT, ITEMS, FINAL_EV, FINAL_MOVES, plan,
                                final_proof, overworld_guard, source_proof,
                                vendor_guard)


def fixture(mid=519):
    status = json.loads((ROOT / "notes/Void-Hypno-won-128-status.json").read_text())
    navigation = json.loads((ROOT / "notes/Void-Hypno-won-128-navigation.json").read_text())
    # Hypothetical future build/training fixture, never native accomplishment.
    status["map"] = mid
    status["trainer"]["money"] -= 17000
    cf = next(m for m in status["party"] if m["species"] == "COFAGRIGUS")
    cf.update(nature="TIMID", ev=list(FINAL_EV), item="POWERLENS", hp=240,
              totalhp=252, attack=93, defense=333, spatk=210, spdef=218, speed=68)
    cf["moves"] = [dict(move=m, pp=10, ppup=0) for m in FINAL_MOVES]
    # Normal carrier-for-KG exchange is hypothetical for this test fixture only.
    kg = next(m for m in status["party"] if m["species"] == "KLINKLANG")
    kg.update(species="TRANQUILL", name="Tranquill", hp=100,
              moves=[dict(move="FLY", pp=10, ppup=0)])
    return status, navigation


def after_shopping(status, proposal):
    after = copy.deepcopy(status)
    after["map"] = 355
    after["trainer"]["money"] = proposal["expected_money"]
    for row in proposal["cart"]:
        bag = after["bag"]["contents"]
        bag[row["item"]] = bag.get(row["item"], 0) + row["quantity"]
    return after


class AgateSupplyQueueTest(unittest.TestCase):
    def test_frozen_deficits_and_no_double_reserve(self):
        status, navigation = fixture()
        proposal = plan(status, navigation)
        self.assertEqual(proposal["total_cost"], 23050)
        self.assertEqual(proposal["expected_money"], 34130)
        self.assertEqual([(r["item"], r["quantity"]) for r in proposal["cart"]],
                         [("XSPECIAL", 5), ("XSPEED", 3), ("XDEFEND", 3),
                          ("XATTACK", 2), ("REVIVALHERB", 2), ("ULTRAPOTION", 10)])
        self.assertEqual(list(proposal["commands"]),
                         ["dept", "herbs", "ultra", "return-circus"])
        checkpoints = [c for cmds in proposal["commands"].values() for c in cmds
                       if c["script"] == "checkpoint"]
        self.assertEqual(checkpoints, [dict(script="checkpoint", args=["Circus-restocked129"])])

    def test_training_consumed_ultra_recomputed(self):
        status, navigation = fixture()
        status["bag"]["contents"]["ULTRAPOTION"] = 28
        proposal = plan(status, navigation)
        self.assertEqual(next(c["quantity"] for c in proposal["cart"]
                              if c["item"] == "ULTRAPOTION"), 12)
        status["trainer"]["money"] = proposal["total_cost"] - 1
        with self.assertRaises(ValueError):
            plan(status, navigation)

    def test_partial_training_or_wrong_carrier_fails(self):
        for mutation in ("ev", "item", "fly"):
            status, navigation = fixture()
            cf = next(m for m in status["party"] if m["species"] == "COFAGRIGUS")
            if mutation == "ev":
                cf["ev"][3] = 32
            elif mutation == "item":
                cf["item"] = None
            else:
                next(m for m in status["party"] if m["species"] == "TRANQUILL")["moves"] = []
            with self.assertRaises(ValueError):
                plan(status, navigation)

    def test_wrong_floor_or_herb_page_fails(self):
        for key, value, field in [("719", True, "switches"), ("719", None, "switches"),
                                  ("175", 6, "variables")]:
            status, navigation = fixture()
            navigation[field][key] = value
            with self.assertRaises(ValueError):
                plan(status, navigation)

    def test_resume_requires_earlier_targets_complete(self):
        status, navigation = fixture(520)
        with self.assertRaises(ValueError):
            plan(status, navigation, "herbs")
        for key, (phase, _, target, _) in ITEMS.items():
            if phase == "dept":
                status["bag"]["contents"][key] = target
        proposal = plan(status, navigation, "herbs")
        self.assertEqual(list(proposal["commands"]), ["herbs", "ultra", "return-circus"])
        self.assertEqual(proposal["total_cost"], 17600)
        with self.assertRaises(ValueError):
            plan(status, navigation, "ultra")

    def test_final_bag_money_and_party_reconciled(self):
        status, navigation = fixture()
        proposal = plan(status, navigation)
        good = after_shopping(status, proposal)
        final_proof(status, good, proposal)
        for mutation in ("money", "bag", "held"):
            bad = copy.deepcopy(good)
            if mutation == "money":
                bad["trainer"]["money"] -= 350
            elif mutation == "bag":
                bad["bag"]["contents"]["XSPECIAL"] -= 1
            else:
                next(m for m in bad["party"] if m["species"] == "COFAGRIGUS")["item"] = None
            with self.assertRaises(ValueError):
                final_proof(status, bad, proposal)

    def test_public_screen_guards(self):
        overworld_guard("Pokemon Reborn")
        vendor_guard("Pokemon Reborn\nWelcome!\nHow may I serve you?\nBuy\nSell\nQuit")
        for text in ("Buy\nSell\nQuit", "Would you like to save the game?\nYes\nNo",
                     "Cofagrigus HP\nFight\nBag"):
            with self.assertRaises(ValueError):
                overworld_guard(text)
        with self.assertRaises(ValueError):
            vendor_guard("BREAK: Hello there, stranger!\nBuy\nSell\nQuit")

    def test_installed_source_stock_price_and_pages(self):
        _, navigation = fixture()
        facts = source_proof(navigation)
        self.assertEqual([(f["map"], f["event"], f["page"]) for f in facts],
                         [(4, 4, 0), (38, 5, 0), (611, 2, 0)])


if __name__ == "__main__":
    unittest.main()
