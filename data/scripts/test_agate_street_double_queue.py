"""Pure queue/receipt fixtures and installed declarations; never UI/processes."""
import copy
import json
from pathlib import Path
import unittest
from agate_street_double_queue import (ROOT,actor_context,installed_foe_proof,
    receipt_guard,returned_command_guard,step_output,validate_plan)
import agate_public_action as public


def fixture():
    roster=json.loads((ROOT/'notes/Agate-final-six-south-ready130-status.json').read_text())
    step={'actor':'Hexan','min_hp':100,'foes':['Noivern','Ditto'],'move_slot':1,'target':1,'target_foe':'Noivern'}
    return roster,step


class Tests(unittest.TestCase):
    def test_queue_scoped_evidence_basename(self):
        a=ROOT/'work/lyla-ezra-turn4-fixture'
        b=ROOT/'work/lyla-ezra-turn8-fixture'
        outputs=[step_output(a,0),step_output(b,0),step_output(a,1)]
        self.assertEqual(len({p.stem for p in outputs}),3)
        self.assertEqual(outputs[0].parent,a)
        self.assertIn(a.name,outputs[0].stem)
        # Same leaf under different parents also cannot share Runner.work.
        c=ROOT/'work/other-fixture'/a.name
        self.assertNotEqual(step_output(a,0).stem,step_output(c,0).stem)
        for index in [-1,16,True]:
            with self.assertRaises(ValueError):step_output(a,index)

    def test_source_eight_and_limits(self):
        self.assertEqual(len(installed_foe_proof()['species']),8)
        roster,s=fixture();validate_plan([s]*16,roster)
        for steps in [[],[s]*17,[dict(s,min_hp=True)],[dict(s,foes=['Noivern','Unknown'])],
                      [dict(s,target_foe='Mantine')],[dict(s,unexpected=True)]]:
            with self.assertRaises(ValueError):validate_plan(steps,roster)

    def test_fakeout_spread_and_item_cap(self):
        r,s=fixture()
        with self.assertRaises(ValueError):validate_plan([dict(s,actor='Mienshao',move_slot=2)],r)
        item={'actor':'Hexan','min_hp':100,'foes':['Wigglytuff','Bellossom'],'item':'X Sp. Atk'}
        validate_plan([item],r)
        with self.assertRaises(ValueError):validate_plan([item,item],r)
        exc=next(m for m in r['party']if m['species']=='EXCADRILL');slot=next(i for i,m in enumerate(exc['moves'])if m['move']=='EARTHQUAKE')
        spread={'actor':exc['name'],'min_hp':1,'foes':['Haxorus','Ditto'],'move_slot':slot}
        with self.assertRaises(ValueError):validate_plan([spread],r)
        validate_plan([dict(spread,reviewed_spread=True)],r)

    def test_actor_context_restores_and_literal_hp(self):
        old=public.ACTOR,public.MAX_HP
        with actor_context('Hexan',320):self.assertEqual(public.hp_pair('HP: 123/320'),(123,320))
        self.assertEqual((public.ACTOR,public.MAX_HP),old)

    def test_boundary_receipts_stop(self):
        base={'pending':None,'public_screens':[{'text':['What will Hexan do?']}],'final_rows':[]}
        receipt_guard(base)
        for text in ['The foe fainted!','Ditto transformed into Hexan!','Cofagrigus fell asleep!','The field changed!','But it failed!']:
            bad=copy.deepcopy(base);bad['public_screens']=[{'text':[text]}]
            with self.subTest(text=text),self.assertRaises(ValueError):receipt_guard(bad)
        with self.assertRaises(ValueError):receipt_guard(dict(base,pending={'unknown_action':True}))

    def test_return_actor_and_foes_must_match(self):
        r,s=fixture();names={m['name']:m for m in r['party']}
        rows=[{'text':'Noivern','x':.08,'y':.12},{'text':'Ditto','x':.08,'y':.24},
              {'text':'Mienshao','x':.59,'y':.48},{'text':'What will','x':.09,'y':.76},
              {'text':'Mienshao do?','x':.09,'y':.83},{'text':'FIGHT','x':.63,'y':.76},
              {'text':'BAG','x':.81,'y':.76},{'text':'RIUN','x':.79,'y':.84}]
        import time
        report={'final_rows':rows,'final_capture_epoch':time.time()}
        returned_command_guard(report,s['foes'],names,'Mienshao')
        alias=copy.deepcopy(report)
        for row in alias['final_rows']:
            row['text']=row['text'].replace('Mienshao','Hienshao').replace('What will','Hhat will')
        returned_command_guard(alias,s['foes'],names,'Mienshao')
        with self.assertRaises(ValueError):returned_command_guard(report,s['foes'],names,'Hexan')
        with self.assertRaises(ValueError):returned_command_guard(report,['Noivern','Mantine'],names,'Mienshao')
        kommo=copy.deepcopy(alias)
        kommo['final_rows'][0]['text']='Wigglytuft'
        kommo['final_rows'][1]['text']='Kommo-o'
        returned_command_guard(kommo,['Wigglytuff','Kommo-o'],names,'Mienshao')


if __name__=='__main__':unittest.main()
