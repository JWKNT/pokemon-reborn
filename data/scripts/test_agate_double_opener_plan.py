"""Pure hypothetical staging fixtures; no game controls/native state reads."""
import copy
import json
from pathlib import Path
import unittest
from agate_double_opener_plan import source_proof,staging_proof

ROOT=Path(__file__).resolve().parents[1]


def fixture():
    s=json.loads((ROOT/'notes/Agate-final-six-south-ready130-status.json').read_text())
    n=json.loads((ROOT/'notes/Agate-final-six-south-ready130-navigation.json').read_text())
    mons={m['species']:m for m in s['party']}
    s['party']=[mons[k] for k in ['CRYOGONAL','MIENSHAO','COFAGRIGUS','ARCANINE','SWAMPERT','EXCADRILL']]
    n['self_switches']['763,49,A']=True
    return s,n


class Tests(unittest.TestCase):
    def test_installed_waiting_order_and_opposite_slot(self):
        p=source_proof();self.assertEqual(p['ditto_copies_own_slot'],0)
        self.assertEqual(p['opponents'],['Lyla:Noivern@index1','Ezra:Ditto@index3'])

    def test_reviewed_frozen_lead_and_exact_moves(self):
        s,n=fixture();self.assertEqual(staging_proof(s,n)['lead_order'],['Hexan','Mienshao'])
        for key in ['order','moves','sash','hp','ant','double']:
            a,b=copy.deepcopy((s,n))
            if key=='order':a['party'][0],a['party'][1]=a['party'][1],a['party'][0]
            elif key=='moves':a['party'][0]['moves'][0]['move']='HAZE'
            elif key=='sash':a['party'][0]['item']=None
            elif key=='hp':a['party'][1]['hp']-=1
            elif key=='ant':b['self_switches']['763,49,A']=False
            else:b['self_switches']['763,45,A']=True
            with self.subTest(key=key),self.assertRaises(ValueError):staging_proof(a,b)


if __name__=='__main__':unittest.main()
