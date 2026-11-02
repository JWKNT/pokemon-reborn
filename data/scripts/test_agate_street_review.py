"""Pure source/damage boundaries; no controls or actual battle reads."""
import unittest
from agate_street_review import report


class Tests(unittest.TestCase):
    def test_mamo_crit_and_weather_thresholds(self):
        r=report();eq=r['mamo_into_cf']['EARTHQUAKE']
        self.assertEqual(eq['critical'],[109,128])
        self.assertEqual(eq['ordinary_at_plus2_def'],[37,44])
        self.assertEqual(eq['burned_critical'],[55,64])
        self.assertEqual(r['mamo_safe_min_hp_preburn'],eq['critical'][1]+15+1)
        self.assertEqual(r['mamo_safe_min_hp_burned'],eq['burned_critical'][1]+15+1)

    def test_clean_double_crit_invalidates_cf_cryo_lead(self):
        r=report()
        self.assertGreater(r['noivern_hurricane_crit_cf'][1]+
                           r['copied_cf_ditto_hex_crit_cf'][1]+15,r['players']['CF'][0])

    def test_cryo_mien_opening_damage_boundaries(self):
        r=report()
        self.assertGreater(r['cryo_icebeam']['NOIVERN']['icebeam0'][0],r['foes']['NOIVERN'][0])
        self.assertGreater(r['mien_brickbreak_copied_cryo_ditto'][0],r['foes']['DITTO'][0])
        self.assertLess(r['whimsicott_dazzle_crit_mien'][1],r['players']['Mien'][0])
        self.assertLess(r['cryo_icebeam']['WHIMSICOTT']['icebeam0'][0],r['foes']['WHIMSICOTT'][0])
        self.assertGreater(r['cryo_icebeam']['WHIMSICOTT']['icebeam_plus2_lightscreen'][0],
                           r['foes']['WHIMSICOTT'][0])


if __name__=='__main__':unittest.main()
