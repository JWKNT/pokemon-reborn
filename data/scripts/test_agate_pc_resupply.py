"""Synthetic/source supply-trip checks only; never call public controls."""
import copy
import json
from pathlib import Path
import subprocess
import unittest
from agate_pc_resupply import (CART,COST,FINAL,clear_completed_street_rays,
                              final_proof,preflight,source_proof)

ROOT=Path(__file__).resolve().parents[1]


def fixture():
    # Explicit closed pre-street snapshot, cloned only in memory. The victory
    # flags below are synthetic future fixtures, not saved/native evidence.
    status=json.loads((ROOT/'notes/Agate-final-six-south-ready130-status.json').read_text())
    nav=json.loads((ROOT/'notes/Agate-final-six-south-ready130-navigation.json').read_text())
    for e in [45,46,49]:nav.setdefault('self_switches',{})[f'763,{e},A']=True
    return status,nav


class Tests(unittest.TestCase):
    def test_installed_cart_shop_and_safe_geometry(self):
        p=source_proof()
        self.assertEqual(COST,4350)
        self.assertEqual(p['shop'],[4,4]);self.assertEqual(p['stop'],[763,46,70])
        self.assertEqual((p['box1_slot'],p['party_slot']),(11,5))

    def test_completed_streets_stage_membership_and_sash_required(self):
        s,n=fixture();self.assertEqual(preflight(s,n)['total_cost'],4350)
        for key in ['stage','street','membership','money','sash','north']:
            a,b=copy.deepcopy((s,n))
            if key=='stage':b['variables']['391']=53
            elif key=='street':b['self_switches']['763,45,A']=False
            elif key=='membership':b['variables']['175']=6
            elif key=='money':a['trainer']['money']=4349
            elif key=='sash':next(m for m in a['party'] if m['species']=='CRYOGONAL')['item']=None
            else:a['position']=[45,52]
            with self.assertRaises(ValueError):preflight(a,b)

    def test_normal_nurse_allows_injuries_and_any_reviewed_six_order(self):
        s,n=fixture();s['party'][0]['hp']=0;s['party'][0]['status']='BURN'
        s['party'][0],s['party'][5]=s['party'][5],s['party'][0]
        preflight(s,n)

    def test_completed_ray_cleanup_is_narrow_and_preserves_actual_npcs(self):
        _,nav=fixture()
        original={(37,y)for y in range(59,64)}|{(42,y)for y in range(55,61)}
        other={(45,52),(70,44),(20,72)}
        nav.setdefault('avoid',{})['763']=list(map(list,original|other))
        # Hypothetical post-victory approached NPC coordinates, fixture only.
        nav['positions']['763']['49']=[37,62]
        nav['positions']['763']['45']=[42,58]
        nav['positions']['763']['46']=[42,55]
        before=copy.deepcopy(nav)
        cleaned,proof=clear_completed_street_rays(nav)
        self.assertEqual(nav,before,'Pure review must not mutate supplied evidence')
        retained=set(map(tuple,cleaned['avoid']['763']))
        self.assertTrue(other<=retained)
        self.assertTrue({(37,62),(42,58),(42,55)}<=retained)
        self.assertTrue({(37,63),(42,60)}<=retained,'Original NPC origin guards are preserved')
        self.assertNotIn((37,59),retained);self.assertNotIn((42,56),retained)
        self.assertTrue(set(map(tuple,proof['removed']))<=original)
        bad=copy.deepcopy(nav);bad['self_switches']['763,46,A']=False
        with self.assertRaises(ValueError):clear_completed_street_rays(bad)
        bad=copy.deepcopy(nav);del bad['positions']['763']['45']
        with self.assertRaises(ValueError):clear_completed_street_rays(bad)

    def test_final_exact_purchases_identity_and_hp_pp(self):
        before,nav=fixture();after=copy.deepcopy(before)
        after['position']=[46,70];after['trainer']['money']-=COST
        for k,_,q,_ in CART:after['bag']['contents'][k]=after['bag']['contents'].get(k,0)+q
        code="require_relative 'scripts/read_rgss'; h=load_rgss('/Applications/Reborn.app/Contents/Game/Data/moves.dat'); puts JSON.generate(h.transform_values{|m|m.instance_variable_get(:@maxpp)})"
        maxima=json.loads(subprocess.check_output(['ruby','-e',code],cwd=ROOT,stderr=subprocess.DEVNULL))
        for mon in after['party']:
            for m in mon['moves']:m['pp']=maxima[m['move']]*(5+m.get('ppup',0))//5
        final_proof(before,after,nav,maxima)
        for key in ['money','bag','held','hp','pp','move','order','north']:
            a,b=copy.deepcopy((after,nav))
            if key=='money':a['trainer']['money']+=1
            elif key=='bag':a['bag']['contents']['XSPEED']-=1
            elif key=='held':a['party'][5]['item']=None
            elif key=='hp':a['party'][3]['hp']-=1
            elif key=='pp':a['party'][3]['moves'][0]['pp']-=1
            elif key=='move':a['party'][3]['moves'][0]['move']='FLY'
            elif key=='order':a['party'][0],a['party'][1]=a['party'][1],a['party'][0]
            else:a['position']=[45,53]
            with self.assertRaises(ValueError):final_proof(before,a,b,maxima)


if __name__=='__main__':unittest.main()
