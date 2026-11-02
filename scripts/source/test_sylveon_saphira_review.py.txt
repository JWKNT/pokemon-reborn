import unittest

from sylveon_saphira_review import (EVS, backed_up_field_after_defog,
                                   build_report, incoming)


class SylveonSourceReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_report()
        cls.worst = cls.report["builds"][0]

    def test_legal_ev_budget_and_conservative_stats(self):
        self.assertEqual(sum(EVS), 508)
        self.assertLessEqual(max(EVS), 252)
        self.assertEqual(self.worst["stats"], [345, 115, 128, 214, 342, 119])

    def test_first_terrain_survives_critical_and_burn(self):
        fields = self.worst["fields"]
        crit = fields["DRAGONSDEN"]["incoming"]["FLAMETHROWER"]["critical"]
        self.assertEqual(crit, [254, 299])
        self.assertGreater(self.worst["stats"][0], crit[1] + self.worst["burn_tick"] + 2)

    def test_misty_moonblast_ohko_but_unboosted_den_does_not(self):
        fields = self.worst["fields"]
        self.assertEqual(fields["MISTY"]["moonblast"], [339, 399])
        self.assertGreater(fields["MISTY"]["moonblast"][0], self.report["noivern"][0])
        self.assertLess(fields["DRAGONSDEN"]["moonblast"][1], self.report["noivern"][0])
        self.assertGreater(fields["DRAGONSDEN"]["moonblast_after_one_x_spatk"][0], self.report["noivern"][0])

    def test_critical_bypasses_x_spdef_but_not_field_defense(self):
        base = incoming(self.report["noivern"], self.worst["stats"], "DRAGONSDEN")
        boosted = incoming(self.report["noivern"], self.worst["stats"], "DRAGONSDEN", spdef_stage=6)
        self.assertEqual(base["FLAMETHROWER"]["critical"], boosted["FLAMETHROWER"]["critical"])
        misty = incoming(self.report["noivern"], self.worst["stats"], "MISTY")
        self.assertEqual(misty["BOOMBURST"]["critical"], [119, 140])
        self.assertLess(misty["FLAMETHROWER"]["critical"][1], base["FLAMETHROWER"]["critical"][1])

    def test_actual_backup_pop_and_installed_no_roost(self):
        self.assertEqual(backed_up_field_after_defog(["DRAGONSDEN", "MISTY"]), "DRAGONSDEN")
        self.assertEqual(backed_up_field_after_defog(["INDOOR", "MISTY"]), "INDOOR")
        self.assertFalse(self.report["noivern_has_roost"])
        self.assertEqual(set(self.report["noivern_moves"]), {"BOOMBURST", "DRAGONPULSE", "FLAMETHROWER", "DEFOG"})


if __name__ == "__main__":
    unittest.main()
