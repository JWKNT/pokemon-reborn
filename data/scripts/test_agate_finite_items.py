"""Pure synthetic receipt/source fixtures; never execute UI or a child process."""
import copy
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from agate_finite_items import (ACTOR,LOW_HP_ERROR,MAX_HP,ROOT,classify_child,
                               helper_argv,run_plan,validate_foes,validate_output,validate_plan)
from agate_finite_items import (GAME,installed_field_change_messages,pilot_receipt,
                               negative_own_stat_message)


def command(foes=('Ludicolo','Beheeyem'),actor=ACTOR):
    return [{'text':n,'x':.08,'y':.12+i*.12} for i,n in enumerate(foes)]+[
        {'text':actor,'x':.59,'y':.48},{'text':'What will','x':.09,'y':.76},
        {'text':actor+' do?','x':.09,'y':.83},{'text':'FIGHT','x':.63,'y':.76},
        {'text':'BAG','x':.81,'y':.76},{'text':'RIUN','x':.79,'y':.84}]


def child(step,*,low=False,mode='warmup',foes=None):
    foes=foes or ['Ludicolo','Beheeyem']
    args=SimpleNamespace(item=step['item'],mode=mode,move_slot=None,target=None,target_foe=None)
    r={'kind':'agate_public_one_reviewed_action','mode':mode,'expected_actor':ACTOR,
       'expected_total_hp':MAX_HP,'min_hp':step['min_hp'],'expected_foes':foes,
       'explicit_action':{'item':step['item'],'move_slot':None,'target':None,'target_foe':None},
       'pending':None,'journal_issues':[],'final_capture_epoch':99.5,
       'final_rows':command(foes),'initial_hp_proof':{'hp':100 if low else 252,'total_hp':252},
       'helpers':[],'result':'stopped_for_review' if low else 'helpers_returned',
       'final_classification':'review_required' if low else 'fresh_expected_command',
       'public_screens':[{'first_epoch':99,'text':['FIGHT','BAG','RIUN']}],
       'nonturn_ui_actions':[]}
    if low:r['error']=LOW_HP_ERROR
    else:
        r['helpers']=[{'argv':helper_argv(args,{}),'returncode':0},
                      {'argv':[sys.executable,str(ROOT/'scripts/battle_ready.py')],'returncode':0}]
        r['final_hp_proof']={'hp':200,'total_hp':252}
        r['final_guard']={'capture_epoch':99.5}
    return r


class Tests(unittest.TestCase):
    def classify(self,r,step,returncode=2):
        return classify_child(r,mode='warmup',foes=['Ludicolo','Beheeyem'],step=step,
                              returncode=returncode,now=100)

    def test_strict_literal_plan_and_cap(self):
        good=[{'item':'X Sp.Def','min_hp':170}]
        self.assertEqual(validate_plan(good),good)
        for p in [[],good*9,[{'item':'','min_hp':1}],[{'item':'X Defend','min_hp':True}],
                  [{'item':'X Defend','min_hp':253}],[{'item':'X Defend','min_hp':1,'target':'partner'}]]:
            with self.assertRaises(ValueError):validate_plan(p)

    def test_known_exact_mode_foes_and_new_output(self):
        self.assertEqual(validate_foes('warmup',['Beheeyem','Ludicolo']),['Beheeyem','Ludicolo'])
        self.assertEqual(validate_foes('ricardo',['Blaziken']),['Blaziken'])
        self.assertEqual(validate_foes('solaris',['Garchomp']),['Garchomp'])
        self.assertEqual(validate_foes('antoine',['Tyranitar']),['Tyranitar'])
        self.assertEqual(validate_foes('lylaezra',['Mantine','Kommo-o']),['Mantine','Kommo-o'])
        for mode,foes in [('warmup',['Ludicolo']),('warmup',['Ludicolo','Ludicolo']),
                         ('warmup',['Ludicolo','Garchomp']),('solaris',['Staraptor','Scizor']),
                         ('ricardo',['Unknown']),('antoine',['Mamoswine','Lurantis']),
                         ('lylaezra',['Mamoswine','Ditto']),('lylaezra',['Ditto'])]:
            with self.assertRaises(ValueError):validate_foes(mode,foes)
        for path in [ROOT,Path('/tmp/agate-outside-workspace-fixture')]:
            with self.assertRaises(ValueError):validate_output(path)

    def test_exact_no_action_low_hp_exception(self):
        step={'item':'X Sp.Def','min_hp':170};r=child(step,low=True)
        self.assertEqual(self.classify(r,step)['outcome'],'low_hp_no_action')
        for mutate in [lambda x:x.update(pending={'dispatch':'unknown'}),
                       lambda x:x.update(helpers=[{'returncode':0}]),
                       lambda x:x.update(error=LOW_HP_ERROR+'?'),
                       lambda x:x.update(error='ValueError: Expected foe changed'),
                       lambda x:x.update(final_capture_error='Recorder restarted'),
                       lambda x:x.update(pre_action_guard={}),
                       lambda x:x.update(initial_hp_proof={'hp':170,'total_hp':252}),
                       lambda x:x.update(initial_hp_proof={'hp':100,'total_hp':270})]:
            bad=copy.deepcopy(r);mutate(bad)
            with self.assertRaises(ValueError):self.classify(bad,step)

    def test_success_requires_exact_helpers_hp_and_fresh_same_foes(self):
        step={'item':'X Sp.Def','min_hp':170};r=child(step)
        self.assertEqual(self.classify(r,step,0)['final_hp'],200)
        for mutate in [lambda x:x['helpers'][0].update(returncode=2),
                       lambda x:x.update(final_rows=command(('Ludicolo','Cryogonal'))),
                       lambda x:x.update(final_rows=command(actor='Arcanine')),
                       lambda x:x.update(final_classification='visible_victory_message'),
                       lambda x:x.update(final_guard={'capture_epoch':80}),
                       lambda x:x.update(final_hp_proof={'hp':0,'total_hp':252}),
                       lambda x:x.update(public_screens=[{'text':["Defense won't go any higher!"]}])]:
            bad=copy.deepcopy(r);mutate(bad)
            with self.assertRaises(ValueError):self.classify(bad,step,0)

    def test_one_heal_then_new_retry_and_no_second_heal(self):
        plan=[{'item':'X Sp.Def','min_hp':170}];calls=[]
        def invoke(step,index,role,n):
            calls.append((role,step,n))
            return {'outcome':'low_hp_no_action'} if role=='item' else {'outcome':'fresh_expected_command','final_hp':200}
        result=run_plan(plan,invoke)
        self.assertEqual(result['result'],'complete')
        self.assertEqual([r[0] for r in calls],['item','one-heal','retry-once'])
        self.assertEqual(calls[1][1],{'item':'Ultra Potion','min_hp':1})
        self.assertEqual(len(set(n for _,_,n in calls)),3)
        calls=[]
        def retry_low(step,index,role,n):
            calls.append(role)
            return {'outcome':'fresh_expected_command','final_hp':200} if role=='one-heal' else {'outcome':'low_hp_no_action'}
        result=run_plan(plan,retry_low)
        self.assertEqual(result['result'],'stopped_for_review')
        self.assertEqual(calls,['item','one-heal','retry-once'])

    def test_post_heal_below_threshold_or_partial_receipt_stops(self):
        plan=[{'item':'X Defend','min_hp':170}];calls=[]
        def low_heal(step,index,role,n):
            calls.append(role)
            return {'outcome':'low_hp_no_action'} if role=='item' else {'outcome':'fresh_expected_command','final_hp':169}
        result=run_plan(plan,low_heal)
        self.assertEqual(result['result'],'stopped_for_review');self.assertEqual(calls,['item','one-heal'])
        calls=[]
        def partial(step,index,role,n):
            calls.append(role);raise ValueError('Pending helper outcome unknown')
        result=run_plan(plan,partial)
        self.assertEqual(result['result'],'stopped_for_review');self.assertEqual(calls,['item'])

    def test_hard_16_invocation_cap_without_hidden_replays(self):
        calls=[]
        def invoke(step,index,role,n):
            calls.append((index,role,n))
            return {'outcome':'low_hp_no_action'} if role=='item' else {'outcome':'fresh_expected_command','final_hp':252}
        result=run_plan([{'item':'X Defend','min_hp':170}]*8,invoke)
        self.assertEqual(result['result'],'stopped_for_review')
        self.assertEqual(len(calls),16);self.assertEqual(result['completed_items'],5)
        self.assertEqual(result['automatic_heal_wrapper_invocations'],5)
        self.assertEqual(calls[-1],(5,'item',16))

    def test_completed_recent_same_mode_pilot_without_reusing_old_hp(self):
        step={'item':'X Sp.Def','min_hp':170};r=child(step);r['end_epoch']=100
        p=pilot_receipt(r,mode='warmup',foes=['Ludicolo','Beheeyem'],now=101)
        self.assertNotIn('initial_hp',p);self.assertNotIn('final_hp',p)
        self.assertEqual(pilot_receipt(r,mode='warmup',foes=['Beheeyem','Ludicolo'],now=101)['foes'],['Beheeyem','Ludicolo'])
        for mutate in [lambda x:x.update(pending={'action':'unknown'}),
                       lambda x:x.update(result='stopped_for_review'),
                       lambda x:x.update(end_epoch=-900),
                       lambda x:x.update(expected_foes=['Ludicolo','Cryogonal']),
                       lambda x:x.update(mode='solaris')]:
            bad=copy.deepcopy(r);mutate(bad)
            with self.assertRaises(ValueError):
                pilot_receipt(bad,mode='warmup',foes=['Ludicolo','Beheeyem'],now=101)

    def test_new_status_field_room_weather_stop_but_existing_hail_chip_does_not(self):
        step={'item':'X Sp.Def','min_hp':170};r=child(step)
        transitions=['Cofagrigus fell asleep!','Ludicolo was burned!',
                     'Cofagrigus was poisoned!','Cofagrigus was paralyzed!',
                     'Cofagrigus was frozen solid!','The field changed!',
                     'The terrain became misty!','Beheeyem used Trick Room!',
                     'Beheeyem twisted the dimensions!',
                     'The twisted dimensions returned to normal!',
                     'It started to rain!','The sunlight turned harsh!',
                     'The rain stopped.','The hail stopped.','A sandstorm brewed!',
                     'The terrain returned to normal.','The snow melted away!']
        for text in transitions:
            bad=copy.deepcopy(r);bad['public_screens']=[{'text':[text]}]
            with self.subTest(text=text),self.assertRaises(ValueError):self.classify(bad,step,0)
        for tag in ['SLP','FRZ','PSN','PAR','BRN','SLP Lv90']:
            bad=copy.deepcopy(r);bad['final_rows'].append({'text':tag,'x':.65,'y':.60})
            with self.subTest(tag=tag),self.assertRaises(ValueError):self.classify(bad,step,0)
        good=copy.deepcopy(r)
        good['public_screens']=[{'text':['The hail is crashing down!',
            'The Pokemon were buffeted by the hail!','The hail continues to fall.',
            'The sandstorm rages.','The rain continues to fall.']}]
        self.assertEqual(self.classify(good,step,0)['outcome'],'fresh_expected_command')
        low=child(step,low=True);low['public_screens']=[{'text':['Cofagrigus fell asleep!']}]
        with self.assertRaises(ValueError):self.classify(low,step)

    def test_negative_own_stat_changes_stop_next_item_with_ocr_name_alias(self):
        step={'item':'X Sp.Def','min_hp':170};r=child(step)
        drops=["Cofagrigue’s Defense fell!", "Cofagrigus's Defense fell!",
               "Cofagrigus's Sp. Def fell!", "Cofagrigus's Sp.Defense fell!",
               "Cofagrigus's Special Defense harshly fell!",
               "Cofagrigus's Defense dramatically fell!",
               "Cofagrigus's Accuracy fell sharply!", "Cofagrigus's Speed fell!",
               "Cofagrigus's Sp. Atk fell!", "Cofagrigus's Attack was lowered!"]
        for text in drops:
            bad=copy.deepcopy(r);bad['public_screens']=[{'text':[text]}]
            with self.subTest(text=text),self.assertRaisesRegex(ValueError,'own stat drop'):
                self.classify(bad,step,0)
        # A wrapped literal must be bound within this one screen.
        bad=copy.deepcopy(r);bad['public_screens']=[{'text':["Cofagrigue’s",'Defense','fell!']}]
        with self.assertRaisesRegex(ValueError,'own stat drop'):self.classify(bad,step,0)
        bad=copy.deepcopy(r);bad['literal_message_candidates']=[{'lines':drops[:1]}]
        with self.assertRaisesRegex(ValueError,'own stat drop'):self.classify(bad,step,0)

    def test_foe_drops_and_requested_own_boosts_do_not_stop(self):
        step={'item':'X Sp.Def','min_hp':170};r=child(step)
        messages=["Tyranitar's Defense fell!", "Ludicolo's Sp. Def sharply fell!",
                  "Cofagrigus's Defense rose sharply!", "Cofagrigus's Sp. Atk rose sharply!",
                  "Cofagrigus's Speed rose sharply!", "Cofagrigus's Accuracy rose sharply!"]
        good=copy.deepcopy(r);good['public_screens']=[{'text':messages}]
        self.assertEqual(self.classify(good,step,0)['outcome'],'fresh_expected_command')
        # The own name in the HUD must not attribute a foe's drop to ours.
        self.assertIsNone(negative_own_stat_message("Cofagrigus Lv90 Tyranitar's Defense fell!"))
        self.assertIsNone(negative_own_stat_message("The opposing Cofagrigus's Defense fell!"))
        good['public_screens']=[{'text':["Cofagrigus's Defense rose sharply!", "Tyranitar's Defense fell!"]}]
        self.assertEqual(self.classify(good,step,0)['outcome'],'fresh_expected_command')

    def test_drop_grammar_matches_installed_amount_messages(self):
        source=(GAME/'Scripts/Battle_Effects.rb').read_text()
        self.assertIn('harsh = "harshly " if increment == 2',source)
        self.assertIn('harsh = "dramatically " if increment >= 3',source)
        self.assertIn('stat_text = _INTL("{1}\'s {2} {3}fell!", pbThis, pbGetStatName(stat), harsh)',source)

    def test_swagger_move_stops_even_if_confusion_text_is_missing(self):
        step={'item':'X Sp.Def','min_hp':170};r=child(step)
        for lines in [['Liepard used Swagger!'],['Noivern used','Swagger!']]:
            bad=copy.deepcopy(r);bad['public_screens']=[{'text':lines}]
            with self.subTest(lines=lines),self.assertRaisesRegex(ValueError,'Swagger use'):
                self.classify(bad,step,0)

    def test_status_weather_field_patterns_bind_installed_static_source(self):
        source='\n'.join((GAME/'Scripts'/p).read_text() for p in ['Battle.rb','Battle_MoveEffects.rb'])
        for phrase in ['fell asleep!','was frozen solid!','was poisoned!',
                       'was paralyzed! It may be unable to move!',
                       'The sunlight turned harsh!','It started to rain!',
                       'A sandstorm brewed!','It started to hail!',
                       'The twisted dimensions returned to normal!',
                       'The terrain returned to normal.']:
            self.assertIn(phrase,source)
        self.assertIn('The snow melted away!',installed_field_change_messages())
        self.assertIn('The grassy terrain caught fire!',installed_field_change_messages())


if __name__=='__main__':unittest.main()
