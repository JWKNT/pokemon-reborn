import json
import unittest

from mime_fairy_review import ROOT, aroma_incoming, build_report, moonblast


class MimeFairyReviewTests(unittest.TestCase):
    def test_compiled_owned_tm99_incompatibility(self):
        compiled = json.loads((ROOT / "work/mime-owned-compiled-compatibility.json").read_text())
        for species in ("SWOOBAT", "AMPHAROS", "LUDICOLO"):
            self.assertNotIn("DAZZLINGGLEAM", compiled[species]["compatiblemoves"])
            self.assertNotIn("DAZZLINGGLEAM", [m for _, m in compiled[species]["Moveset"]])
            self.assertNotIn("DAZZLINGGLEAM", compiled[species].get("EggMoves") or [])
            self.assertNotIn("DAZZLINGGLEAM", compiled[species].get("RelearnerMoves") or [])
        for preevolution in ("WOOBAT", "MAREEP", "FLAAFFY", "LOTAD", "LOMBRE"):
            self.assertNotIn("DAZZLINGGLEAM", compiled[preevolution].get("EggMoves") or [])

    def test_gift_does_not_require_mime_victory(self):
        source = json.loads((ROOT / "work/mime-sylveon-order-static-774.json").read_text())
        page = source["events"]["128"]["pages"][0]
        self.assertFalse(page["condition"]["variable_valid"])
        self.assertEqual(page["condition"]["switch2_id"], 1064)
        self.assertNotIn("475", str(page["list"]))

    def test_one_boost_ohko_requires_measured_spa(self):
        self.assertLess(moonblast(193, 526)[0], 704)
        self.assertGreaterEqual(moonblast(195, 526)[0], 704)
        self.assertGreaterEqual(moonblast(193, 526, boost=4)[0], 704)
        self.assertLess(moonblast(214, 526, drop=0, boost=6)[0], 704)

    def test_midturn_special_defense_drop_is_material(self):
        first = aroma_incoming(279)["FLASHCANNON"]["critical"][1]
        lowered = aroma_incoming(279, stage=-1)["FLASHCANNON"]["critical"][1]
        self.assertLess(first * 2, 345)
        self.assertGreater(first + lowered, 345)

    def test_crit_bypasses_positive_stage_but_keeps_misty(self):
        self.assertEqual(aroma_incoming(342, stage=2)["FLASHCANNON"]["critical"],
                         aroma_incoming(342)["FLASHCANNON"]["critical"])
        self.assertEqual(build_report()["trainer_stats"]["MRMIME"], [704, 38, 420, 34, 526, 540])


if __name__ == "__main__":
    unittest.main()
