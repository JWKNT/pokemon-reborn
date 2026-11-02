"""Pure/source Agate assembly fixtures; no actual UI or native claims."""
import copy
import unittest
from agate_party_assemble import (START,FINAL,CF_EV,CF_MOVES,card_slot,final_proof,
                                  preflight,source_proof,trainer_hazards)


def frozen_fixture(stage=51):
    names=['Cofagrigus','Tranquill','Swampert','Mienshao','Arcanine','Excadrill']
    party=[]
    for species,name in zip(START,names):
        party.append({'species':species,'name':name,'level':90,'hp':252,'totalhp':252,
                      'status':None,'item':None,'nature':'TIMID','ev':[0]*6,
                      'attack':93,'defense':333,'spatk':210,'spdef':218,'speed':68,
                      'moves':[{'move':m,'pp':10,'ppup':0} for m in CF_MOVES]})
    party[0]['ev']=list(CF_EV)
    party[1]['moves'][0]['move']='FLY'
    return ({'map':355,'position':[30,13],'party':party,'trainer':{'money':2000},
             'bag':{'contents':{'ULTRAPOTION':40,'FOCUSSASH':0,'POWERLENS':1}}},
            {'variables':{'391':stage},'switches':{'5':False,'989':False,'990':True,'259':True},
             'self_switches':{}})


class Guards(unittest.TestCase):
    def test_installed_pc_south_setter_commitment_and_fresh_cursor(self):
        p=source_proof()
        self.assertEqual(p['normal_setter'],[763,30,62])
        self.assertEqual(p['stop'],[355,38,25])
        self.assertEqual(p['approach_stop'],[763,45,53])
        self.assertEqual(p['assembly_pc'],[355,5,38,25,'Up'])
        self.assertFalse(p['fly_to_agate'])
        self.assertEqual(p['west_entry_stop'],[763,13,54])
        self.assertEqual(p['west_entry_requires_stage'],52)
        self.assertEqual(p['agate_assembly_pc'],[752,7])
        self.assertEqual(p['agate_assembly_stop'],[763,46,70])
        self.assertEqual(p['fresh_box_cursor'],0)
        self.assertEqual(p['swap1'],[1,11,1,'Kricketune','Tranquill'])
        self.assertEqual(p['swap2'],[1,6,1,'Hexan','Kricketune'])
        self.assertEqual(p['commitment'],[[x,52] for x in range(43,49)])

    def test_only_finished_build_known_stage_and_carrier_allowed(self):
        s,n=frozen_fixture();self.assertEqual(preflight(s,n)['initial_stage'],51)
        for mutation in ['stage','moves','carrier','order']:
            a,b=copy.deepcopy((s,n))
            if mutation=='stage':b['variables']['391']=53
            elif mutation=='moves':a['party'][0]['moves'][1]['move']='SHADOWBALL'
            elif mutation=='carrier':a['party'][1]['hp']=0
            else:a['party'][1],a['party'][2]=a['party'][2],a['party'][1]
            with self.assertRaises(ValueError):preflight(a,b)

    def test_normal_mint_override_is_effective_nature(self):
        s,n=frozen_fixture();s['party'][0].update(nature='CALM',natureflag='TIMID')
        preflight(s,n)
        s['party'][0]['natureflag']='CALM'
        with self.assertRaises(ValueError):preflight(s,n)
        s['party'][0]['natureflag']=None
        with self.assertRaises(ValueError):preflight(s,n)

    def test_active_ricardo_cannot_be_walked_through_to_set_stage(self):
        s,n=frozen_fixture();n['switches']['989']=True
        self.assertIn((30,62),trainer_hazards(n))
        self.assertTrue(preflight(s,n)['optional_setter_blocked'])
        indexed={m['species']:m for m in s['party']}
        cryo=copy.deepcopy(indexed['COFAGRIGUS']);cryo.update(species='CRYOGONAL',name='Hexan',item='FOCUSSASH')
        assembled=copy.deepcopy(s);assembled.update(map=763,position=[46,70])
        assembled['party']=[copy.deepcopy(indexed[v]) if v!='CRYOGONAL' else cryo for v in FINAL]
        with self.assertRaises(ValueError):preflight(assembled,n,phase='approach')
        n['self_switches']['763,48,A']=True
        self.assertNotIn((30,62),trainer_hazards(n))
        preflight(assembled,n,phase='approach')

    def test_party_card_geometry_rejects_missing_duplicate_or_wrong_name(self):
        rows=[{'text':'Cofagrigus','x':.1,'y':.15},{'text':'Arcanine','x':.6,'y':.195}]
        self.assertEqual(card_slot(rows,'Cofagrigus'),0)
        self.assertEqual(card_slot(rows,'Arcanine'),1)
        with self.assertRaises(ValueError):card_slot(rows,'Hexan')
        with self.assertRaises(ValueError):card_slot(rows+[dict(rows[0])],'Cofagrigus')
        with self.assertRaises(ValueError):card_slot([{'text':'Arcanine','x':.1,'y':.9}],'Arcanine')

    def test_final_proof_checks_sash_full_pp_order_stage_and_consumption(self):
        before,nav=frozen_fixture()
        indexed={m['species']:m for m in before['party']}
        after=copy.deepcopy(before);after.update(map=355,position=[38,25])
        cryo=copy.deepcopy(before['party'][0]);cryo.update(species='CRYOGONAL',name='Hexan',item='FOCUSSASH')
        after['party']=[copy.deepcopy(indexed[s]) if s!='CRYOGONAL' else cryo for s in FINAL]
        maxima={m:10 for m in CF_MOVES}
        final_proof(before,after,nav,maxima,phase='assemble',initial_stage=51)
        for mutation in ['sash','hp','pp','stage','medicine','order']:
            a,b=copy.deepcopy((after,nav))
            if mutation=='sash':a['party'][5]['item']=None
            elif mutation=='hp':a['party'][0]['hp']-=1
            elif mutation=='pp':a['party'][2]['moves'][0]['pp']=9
            elif mutation=='stage':b['variables']['391']=53
            elif mutation=='medicine':a['bag']['contents']['ULTRAPOTION']=39
            else:a['party'][1],a['party'][2]=a['party'][2],a['party'][1]
            with self.assertRaises(ValueError):final_proof(before,a,b,maxima,phase='assemble',initial_stage=51)
        approach_before=copy.deepcopy(after);approach_before.update(map=763,position=[30,62])
        approach_after=copy.deepcopy(after)
        approach_after.update(map=763,position=[45,53]);nav['variables']['391']=52
        final_proof(approach_before,approach_after,nav,maxima,phase='approach')

    def test_west_entry_requires_fixed_six_and_registered_restoration_page(self):
        before,nav=frozen_fixture()
        indexed={m['species']:m for m in before['party']}
        cryo=copy.deepcopy(indexed['COFAGRIGUS']);cryo.update(species='CRYOGONAL',name='Hexan',item='FOCUSSASH')
        before['party']=[copy.deepcopy(indexed[s]) if s!='CRYOGONAL' else cryo for s in FINAL]
        with self.assertRaises(ValueError):preflight(before,nav,phase='west-entry')
        nav['switches']['988']=True
        with self.assertRaises(ValueError):preflight(before,nav,phase='west-entry')
        nav['variables']['391']=52
        self.assertEqual(preflight(before,nav,phase='west-entry')['phase'],'west-entry')
        before['party'][5]['item']=None
        with self.assertRaises(ValueError):preflight(before,nav,phase='west-entry')

    def test_agate_assembly_requires52_conscious_travel_party_and_explicit_lead(self):
        s,n=frozen_fixture();s.update(map=763,position=[31,61])
        with self.assertRaises(ValueError):preflight(s,n,phase='agate-assemble')
        n['variables']['391']=52
        preflight(s,n,phase='agate-assemble')
        s['party'][0],s['party'][2]=s['party'][2],s['party'][0]
        with self.assertRaises(ValueError):preflight(s,n,phase='agate-assemble')
        preflight(s,n,phase='agate-assemble',incoming_lead='Swampert')
        s['party'][1],s['party'][3]=s['party'][3],s['party'][1]
        with self.assertRaises(ValueError):preflight(s,n,phase='agate-assemble',incoming_lead='Swampert')

    def test_only_agate_assembly_accepts_injured_conscious_statusfree_members(self):
        s,n=frozen_fixture();s.update(map=763,position=[31,61]);n['variables']['391']=52
        s['party'][0]['hp']=1;s['party'][2]['hp']=25
        preflight(s,n,phase='agate-assemble')
        s['party'][0]['status']='POISON'
        with self.assertRaises(ValueError):preflight(s,n,phase='agate-assemble')
        s['party'][0]['status']=None;s['party'][2]['hp']=0
        with self.assertRaises(ValueError):preflight(s,n,phase='agate-assemble')
        s['party'][2]['hp']=s['party'][2]['totalhp']+1
        with self.assertRaises(ValueError):preflight(s,n,phase='agate-assemble')
        indexed={m['species']:m for m in s['party']}
        cryo=copy.deepcopy(indexed['COFAGRIGUS']);cryo.update(species='CRYOGONAL',name='Hexan',item='FOCUSSASH')
        s['party']=[copy.deepcopy(indexed[v]) if v!='CRYOGONAL' else cryo for v in FINAL]
        with self.assertRaises(ValueError):preflight(s,n,phase='approach')

    def test_agate_final_proof_handles_incoming_swamp_lead_without_inventing_party_order(self):
        before,n=frozen_fixture();before.update(map=763,position=[31,61]);n['variables']['391']=52
        before['party'][0],before['party'][2]=before['party'][2],before['party'][0]
        indexed={m['species']:m for m in before['party']}
        cryo=copy.deepcopy(indexed['COFAGRIGUS']);cryo.update(species='CRYOGONAL',name='Hexan',item='FOCUSSASH')
        after=copy.deepcopy(before);after.update(map=763,position=[46,70])
        after['party']=[copy.deepcopy(indexed[v]) if v!='CRYOGONAL' else cryo for v in FINAL]
        maxima={m:10 for m in CF_MOVES}
        final_proof(before,after,n,maxima,phase='agate-assemble',initial_stage=52)
        after['party'][0]['item']='POWERLENS'
        with self.assertRaises(ValueError):final_proof(before,after,n,maxima,phase='agate-assemble',initial_stage=52)


if __name__=='__main__':unittest.main()
