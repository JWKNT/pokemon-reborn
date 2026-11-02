"""Small meaningful pure fixtures for the relevant installed damage mechanics."""
import unittest
from fractions import Fraction as F
from nonmega_saphira_review import calc, stage, build_report


class Mechanics(unittest.TestCase):
    def test_critical_keeps_attack_boost_but_drops_defense_boost(self):
        self.assertEqual(stage(278,1,critical=True),417)
        self.assertEqual(stage(243,6,critical=True,defensive=True),243)

    def test_av_remains_fractional_and_survives_critical(self):
        plain=calc(95,85,278,243,attack_stage=1,field_multiplier=F(3,2),stab=F(3,2),critical=True)
        vest=calc(95,85,278,243,attack_stage=1,defense_multiplier=F(3,2),field_multiplier=F(3,2),stab=F(3,2),critical=True)
        self.assertGreater(plain[1],363)
        self.assertLess(vest[1],363)

    def test_field_type_boost_is_after_core_plus_two(self):
        self.assertEqual(calc(95,85,417,F(729,2),field_multiplier=F(3,2),stab=F(3,2)),[151,178])

    def test_sash_and_scarf_branches(self):
        r=build_report()
        self.assertTrue(r['outgoing_plus6']['SALAMENCE']['sash'])
        self.assertGreater(r['outgoing_plus6']['GARCHOMP']['damage'][0],r['foes']['GARCHOMP'][0])
        self.assertGreater(r['speed_plus6'],r['foes']['CHARIZARD'][5]*2)
        self.assertGreater(r['physical_incoming']['HAXORUS:DRAGONCLAW']['2']['critical_bypasses_def'][0],r['proposed_swamp'][0])

    def test_impish_survives_base_sash_crit_but_not_prior_dd(self):
        r=build_report(nature='IMPISH',ev=[252,0,100,0,52,104])
        self.assertEqual(r['proposed_swamp'],[363,242,232,155,197,160])
        self.assertEqual(r['noivern_incoming']['DRAGONPULSE']['critical_even_at_plus6_spdef'],[278,327])
        for species in ('SALAMENCE','HAXORUS'):
            rows=r['physical_incoming'][species+':DRAGONCLAW']
            self.assertLess(rows['0']['critical_bypasses_def'][1],363)
            self.assertGreater(rows['2']['critical_bypasses_def'][0],363)


if __name__ == '__main__':
    unittest.main()
