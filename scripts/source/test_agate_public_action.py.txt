"""Synthetic public-menu fixtures; no actual UI/input/battle claims."""
import argparse
from pathlib import Path
from types import SimpleNamespace
import unittest
from agate_public_action import (command_guard,helper_argv,hp_pair,inspection_guard,
                                 inspection_context,message_candidates,source_proof,Runner,
                                 mode_is_double,mode_default_foes)


def command(foes=('Ludicolo','Beheeyem'),actor='Cofagrigus'):
    return [{'text':n,'x':.08,'y':.12+i*.12} for i,n in enumerate(foes)]+[
        {'text':actor,'x':.59,'y':.48},
        {'text':'What will','x':.09,'y':.76},
        {'text':actor+' do?','x':.09,'y':.83},
        {'text':'FIGHT','x':.63,'y':.76},
        {'text':'BAG','x':.81,'y':.76},
        {'text':'RIUN','x':.79,'y':.84}]


def inspection(hp='170/252',actor='Cofagrigus'):
    return [{'text':n,'x':.42,'y':.10+i*.065} for i,n in enumerate([
        'Type: Ghost','HP: '+hp,'Attack: 93','Defense: 333',
        'Sp.Attack: 210','Sp.Defense: 654','Speed: 68'])]+[
        {'text':'Inspecting '+actor+':','x':.08,'y':.80}]


class Tests(unittest.TestCase):
    def test_source_contract(self):
        self.assertEqual(set(source_proof()),{'Battle_Inspect.rb','Controls.rb','Battle_Scene.rb','SW Subclasses.rb'})

    def test_exact_fresh_double_actor_and_foe_guard(self):
        rows=command();g=command_guard(rows,['Beheeyem','Ludicolo'],'warmup',captured_at=100,now=101)
        self.assertEqual(g['ordered_visible_foes'],['Ludicolo','Beheeyem'])
        for rows in [command(actor='Arcanine'),command(('Ludicolo','Cryogonal')),
                     command()+[{'text':'PP: 10/10','x':.7,'y':.86}],
                     command()+[{'text':'Choose a Pokemon','x':.2,'y':.8}]]:
            with self.assertRaises(ValueError):command_guard(rows,['Ludicolo','Beheeyem'],'warmup',captured_at=100,now=101)
        rows=command();rows[4]['text']='Arcanine do?'
        with self.assertRaises(ValueError):command_guard(rows,['Ludicolo','Beheeyem'],'warmup',captured_at=100,now=101)
        with self.assertRaises(ValueError):command_guard(command(),['Ludicolo','Beheeyem'],'warmup',captured_at=100,now=116)

    def test_singles_own_numeric_context(self):
        rows=command(('Staraptor',));rows.insert(2,{'text':'181/252','x':.8,'y':.64})
        self.assertEqual(command_guard(rows,['Staraptor'],'solaris',captured_at=100,now=101)['actor'],'Cofagrigus')
        self.assertEqual(hp_pair('Cofagrigus Lv90 HP 181/252'),(181,252))
        for text in ['HP 181 252','181/270','0/252','2o1/252','181/252 182/252']:
            with self.assertRaises(ValueError):hp_pair(text)

    def test_street_exact_modes_preserve_actor_foe_and_double_target_guards(self):
        self.assertFalse(mode_is_double('antoine'))
        self.assertTrue(mode_is_double('lylaezra'))
        self.assertEqual(mode_default_foes('antoine'),['Mamoswine'])
        self.assertEqual(mode_default_foes('lylaezra'),['Noivern','Ditto'])
        command_guard(command(('Mamoswine',)),['Mamoswine'],'antoine',captured_at=100,now=101)
        g=command_guard(command(('Noivern','Ditto')),['Ditto','Noivern'],'lylaezra',captured_at=100,now=101)
        self.assertEqual(g['ordered_visible_foes'],['Noivern','Ditto'])
        args=argparse.Namespace(item=None,move_slot=3,target=3,target_foe='Ditto',mode='lylaezra')
        self.assertEqual(helper_argv(args,g,Path('/synthetic'))[1:],
                         ['/synthetic/scripts/battle_move.py','3','3','--foe-names','Noivern,Ditto','--watch'])
        for rows,foes,mode in [(command(('Mamoswine','Lurantis')),['Mamoswine','Lurantis'],'antoine'),
                (command(('Mamoswine',)),['Mamoswine'],'lylaezra'),
                (command(('Noivern','Mamoswine')),['Noivern','Mamoswine'],'lylaezra'),
                (command(('Noivern','Ditto'),actor='Cryogonal'),['Noivern','Ditto'],'lylaezra')]:
            with self.assertRaises(ValueError):command_guard(rows,foes,mode,captured_at=100,now=101)

    def test_street_doubles_uses_same_bounded_own_inspection(self):
        runner=Runner.__new__(Runner);runner.args=SimpleNamespace(mode='lylaezra')
        runner.report={};runner.write=lambda:None;calls=[]
        runner.keys=lambda *keys:calls.append(keys)
        runner.snap=lambda:(100,inspection())
        runner.crop_ocr=lambda *args:{'rows':inspection()}
        runner.guarded_command=lambda:(command(('Noivern','Ditto')),{'actor':'Cofagrigus'})
        proof,_,_=runner.own_hp(command(('Noivern','Ditto')),stem='before')
        self.assertEqual(proof['hp'],170)
        self.assertEqual(calls,[('q:.12','wait:.6'),('x:.12','wait:.6')])

    def test_own_inspection_numeric_and_no_stage_inference(self):
        proof=inspection_guard(inspection())
        self.assertEqual((proof['hp'],proof['total_hp']),(170,252))
        self.assertEqual(proof['explicit_displayed_stages'],{})
        self.assertIn('Sp.Defense: 654',proof['literal_own_stat_lines'])
        explicit=inspection();explicit[5]['text']='Sp.Defense: 654 +4'
        self.assertEqual(inspection_guard(explicit)['explicit_displayed_stages'],{'Sp.Defense':4})
        for rows in [inspection(actor='Beheeyem'),inspection('170/270'),inspection('???/252')]:
            with self.assertRaises(ValueError):inspection_guard(rows)

    def test_owned_excadrill_is_not_rejected_as_historical_solaris_foe(self):
        from agate_street_double_queue import actor_context
        with actor_context('Excadrill',379):
            self.assertEqual(inspection_guard(inspection('379/379',actor='Excadrill'))['hp'],379)
            bad=inspection('379/379',actor='Excadrill')
            bad[-1]['text']='Inspecting Excadrill and Lycanroc:'
            with self.assertRaises(ValueError):inspection_guard(bad)

    def test_positioned_split_own_hp_and_stats(self):
        # Synthetic OCR geometry reproduces separate label/right-value rows.
        rows=[{'text':'Inspecting Cofagrigus:','x':.08,'y':.80}]
        for i,(label,value) in enumerate([('HP:','170 / 252'),('Attack:','93'),
                ('Defense:','333'),('Sp.Attack:','840'),('Sp.Defense:','218'),('Speed:','272')]):
            y=.13+i*.06
            rows.extend([{'text':label,'x':.43,'y':y,'h':.02},
                         {'text':value,'x':.74,'y':y+.004,'h':.02}])
        proof=inspection_guard(rows)
        self.assertEqual((proof['hp'],proof['total_hp']),(170,252))
        self.assertIn('Sp.Attack: 840',proof['literal_own_stat_lines'])
        self.assertEqual(proof['explicit_displayed_stages'],{})
        bad=[dict(r) for r in rows];bad[2]['y']+=.05
        with self.assertRaises(ValueError):inspection_guard(bad)
        bad=[dict(r) for r in rows];bad[2]['text']='17o/252'
        with self.assertRaises(ValueError):inspection_guard(bad)
        bad=rows+[{'text':'171/252','x':.9,'y':.134}]
        with self.assertRaises(ValueError):inspection_guard(bad)

    def test_reported_single_inspection_has_no_hp_by_source(self):
        # Root-reported Ricardo own-popup labels/values, synthetic positions.
        # No claim that these are a newly captured screen or a doubles popup.
        rows=[{'text':s,'x':.43,'y':.04+i*.075} for i,s in enumerate([
            'Type: Ghost','Attack: 93','Defense: 333','Sp.Attack: 840',
            'Sp.Defense: 218','Speed: 272','Accuracy: 100%','Evasion: 100%'])]
        rows.append({'text':'Inspecting Cofagrigus:','x':.08,'y':.80})
        self.assertEqual([k for k,_,_ in inspection_context(rows)[1]][:2],['attack','defense'])
        with self.assertRaises(ValueError):inspection_guard(rows)
        # A visible battle HUD fraction below the stat panel is not popup HP.
        with self.assertRaises(ValueError):
            inspection_guard(rows+[{'text':'HP: 153/252','x':.74,'y':.68}])

    def test_bounded_own_focus_requires_numeric_proof_and_never_changes_inspectee(self):
        def fake(observations):
            runner=Runner.__new__(Runner);runner.args=SimpleNamespace(mode='warmup')
            runner.report={};runner.write=lambda:None;calls=[];it=iter(observations)
            runner.keys=lambda *keys:calls.append(keys)
            current=[]
            def snap():
                current[:]=[next(it)]
                return 100,current[0]
            runner.snap=snap
            runner.crop_ocr=lambda *args:{'rows':current[0]}
            runner.guarded_command=lambda:(command(),{'actor':'Cofagrigus'})
            return runner,calls
        no_hp=[r for r in inspection() if not r['text'].startswith('HP:')]
        runner,calls=fake([no_hp,inspection()])
        proof,_,_=runner.own_hp(command(),stem='before')
        self.assertEqual(proof['hp'],170)
        self.assertEqual(calls,[('q:.12','wait:.6'),('down:.12','wait:.25'),('x:.12','wait:.6')])
        runner,calls=fake([no_hp,no_hp])
        with self.assertRaises(ValueError):runner.own_hp(command(),stem='before')
        self.assertEqual(calls,[('q:.12','wait:.6'),('down:.12','wait:.25')])
        runner,calls=fake([inspection('17o/252')])
        with self.assertRaises(ValueError):runner.own_hp(command(),stem='before')
        self.assertEqual(calls,[('q:.12','wait:.6')])
        runner,calls=fake([inspection(actor='Beheeyem')])
        with self.assertRaises(ValueError):runner.own_hp(command(),stem='before')
        self.assertEqual(calls,[('q:.12','wait:.6')])

    def test_exact_requested_action_and_physical_target(self):
        root=Path('/synthetic');proof={'ordered_visible_foes':['Ludicolo','Beheeyem']}
        args=argparse.Namespace(item='X Sp.Def',move_slot=None,target=None,target_foe=None,mode='warmup')
        self.assertEqual(helper_argv(args,proof,root)[1:],['/synthetic/scripts/battle_item.py','X Sp.Def','Cofagrigus','--active'])
        args.item='Ultra Potion'
        self.assertEqual(helper_argv(args,proof,root)[-1],'Cofagrigus')
        args.item=None;args.move_slot=1;args.target=3;args.target_foe='Beheeyem'
        self.assertEqual(helper_argv(args,proof,root)[1:],['/synthetic/scripts/battle_move.py','1','3','--foe-names','Ludicolo,Beheeyem','--watch'])
        for bad in [None,'Ludicolo']:
            args.target_foe=bad
            with self.assertRaises(ValueError):helper_argv(args,proof,root)

    def test_literal_messages_not_unseen_outcomes(self):
        s=[{'first_epoch':1,'text':['Cofagrigus used Trick Room!','The dimensions twisted!']},
           {'first_epoch':2,'text':['A critical hit!']},
           {'first_epoch':3,'text':['FIGHT','BAG','RUN']}]
        self.assertEqual(len(message_candidates(s)),2)
        self.assertEqual(message_candidates(s)[1]['lines'],['A critical hit!'])


if __name__=='__main__':unittest.main()
