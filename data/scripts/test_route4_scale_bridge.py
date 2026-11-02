"""Pure preflight/source guard tests: no control or screenshot imports."""
import copy
import unittest
from route4_scale_bridge import preflight,proposal,source_proof


def status():
    return {'party':[{'level':90,'hp':300,'totalhp':300,'status':None,'species':'ARCANINE','moves':[]}]+[
        {'species':'SWAMPERT','moves':[{'move':'SURF'}]}]+[{}]*4,
        'bag':{'contents':{'SUPERREPEL':3,'HEARTSCALE':0}}}


class Guards(unittest.TestCase):
    def test_explicit_layer_never_assumes_surf_from_hop(self):
        p=proposal(1)
        self.assertEqual(p['steps'][0],['layer_walk',715,50,23,1,0])
        self.assertIn('715[50,24]',p['steps'][1]['require'])
        self.assertEqual(p['steps'][4],['eventq',715,64,'item'])

    def test_source_unconditional_anchor_and_correct_new_item(self):
        self.assertEqual([r['event'] for r in source_proof()],[97,64])

    def test_owned_scale_skips_duplicate_and_no_surf_is_rejected(self):
        s=status();preflight(s)
        s['bag']['contents']['HEARTSCALE']=1
        with self.assertRaises(ValueError):preflight(s)
        s=status();s['party'][1]['moves']=[]
        with self.assertRaises(ValueError):preflight(s)

    def test_weak_lead_or_no_repel_stops_before_route(self):
        s=status();s['party'][0]['hp']=50
        with self.assertRaises(ValueError):preflight(s)
        s=status();s['bag']['contents']['SUPERREPEL']=0
        with self.assertRaises(ValueError):preflight(s)


if __name__=='__main__':unittest.main()
