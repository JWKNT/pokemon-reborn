"""Temporary one/two-major evidence fixtures; native extraction is mocked."""
import contextlib
import copy
from datetime import datetime,timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import prepare_major_append as staging
import reconcile_major_items as producer


class MajorEvidenceTests(unittest.TestCase):
    def test_vs_entry_can_precede_log_only_with_bound_public_challenge(self):
        row=copy.deepcopy(self.attempts[0]);row.update(battle_start_epoch=1079,opponent='Test')
        with self.assertRaises(ValueError):producer.completed_log_identity(self.logs[0],producer.attempt_identity(row),self.pre['save_mtime'])
        row.update(battle_challenge_epoch=1081,battle_challenge_evidence={'epoch':1081,'text':['Test would like to battle!']})
        identity=producer.attempt_identity(row)
        self.assertEqual(producer.completed_log_identity(self.logs[0],identity,self.pre['save_mtime'])['created_epoch'],1080)
        row['battle_challenge_evidence']['text']=['Another trainer would like to battle!']
        with self.assertRaises(ValueError):producer.attempt_identity(row)
        row['battle_challenge_evidence']={'epoch':1140,'text':['Test would like to battle!']};row['battle_challenge_epoch']=1140
        with self.assertRaises(ValueError):producer.attempt_identity(row)

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name).resolve()
        self.pre={'bag':{'type':'PokemonBag','contents':{'FULLHEAL':8,'ULTRAPOTION':15}},
                  'party':[{'item':None}for _ in range(6)],
                  'save_mtime':datetime.fromtimestamp(1000,timezone.utc).isoformat()}
        self.post=copy.deepcopy(self.pre);self.post['bag']['contents']['FULLHEAL']=7
        self.post['save_mtime']=datetime.fromtimestamp(1500,timezone.utc).isoformat()
        self.status_paths=[self.write_json('before.json',self.pre),self.write_json('after.json',self.post)]
        self.saves=[self.root/'before.rxdata',self.root/'after.rxdata']
        for p,obj in zip(self.saves,[self.pre,self.post]):p.write_text(json.dumps(obj))
        self.logs=[self.root/(datetime.fromtimestamp(1080+i*200,timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')+' - Aster vs. Test Singles.txt')for i in range(2)]
        for p,text in zip(self.logs,['[Player used Full Heal]\n','[Player used Ultra Potion]\n[Player used Ultra Potion]\n']):self.write_log(p,text)
        self.attempts=[{'id':125+i,'session':127+i,'attempt':1,'battle_start_epoch':1100+i*200,
                        'interaction_start_epoch':1070+i*200,
                        'battle_end_epoch':1200+i*200,'victory_epoch':1190+i*200,'result':'victory'}for i in range(2)]
        self.records=self.write_json('public-attempts.json',self.attempts)
        self.report_path=self.root/'report.json'

    def tearDown(self):self.temp.cleanup()
    def write_json(self,name,obj):
        p=self.root/name;p.write_text(json.dumps(obj));return p
    def write_log(self,path,text):path.write_text('Pokemon Reborn Fixture - '+path.stem+'\n'+text)
    def native(self,path):return copy.deepcopy(self.pre if Path(path)==self.saves[0]else self.post)
    def produce(self,count=1):
        self.post['bag']['contents']['ULTRAPOTION']=13 if count==2 else 15
        self.write_json('after.json',self.post);self.saves[1].write_text(json.dumps(self.post))
        with patch('reconcile_glass_items.read_saved_inventory',side_effect=self.native):
            report=producer.build_report(*self.status_paths,self.logs[:count],self.saves,[self.records]*count,[125+i for i in range(count)])
        self.write_json('report.json',report);return report
    def gate(self,number=1,config=None,attempt=None):
        config=config or {'id':124+number,'item_usage_reconciliation':'report.json','item_usage_reconciliation_round':number}
        attempt=attempt or self.attempts[number-1]
        with patch('prepare_major_append.read_saved_inventory',side_effect=self.native):
            return staging.verified_item_usage(config,attempt,self.logs[number-1],self.root)

    def test_single_victory_consumption_and_no_mutation(self):
        self.produce();before={str(p):p.read_bytes()for p in self.root.iterdir()}
        usage,evidence=self.gate()
        self.assertEqual(usage,[{'name':'Full Heal','count':1}])
        self.assertIn('retained_attempt_identity_sha256',evidence)
        self.assertEqual(before,{str(p):p.read_bytes()for p in self.root.iterdir()})

    def test_two_retained_victories_use_their_own_count_lists(self):
        report=self.produce(2)
        self.assertEqual(report['status'],'verified_counts')
        self.assertEqual(self.gate(1)[0],[{'name':'Full Heal','count':1}])
        self.assertEqual(self.gate(2)[0],[{'name':'Ultra Potion','count':2}])

    def test_refund_mismatch_blocks_single_publication(self):
        self.post['bag']['contents']['FULLHEAL']=8
        report=self.produce()
        self.assertEqual(report['status'],'mismatch')
        self.assertNotIn('item_usage',report['per_round'][0])
        with self.assertRaises(AssertionError):self.gate()

    def test_failed_or_unfinished_attempt_has_no_report(self):
        for result in ['loss',None]:
            rows=copy.deepcopy(self.attempts);rows[0]['result']=result;self.write_json('public-attempts.json',rows)
            with patch('reconcile_glass_items.read_saved_inventory',side_effect=self.native):
                with self.subTest(result=result),self.assertRaises(ValueError):producer.build_report(*self.status_paths,self.logs[:1],self.saves,[self.records],[125])

    def test_later_journal_append_preserves_retained_identity(self):
        self.produce();rows=copy.deepcopy(self.attempts)
        rows.append({'id':999,'session':130,'attempt':1,'result':'loss'})
        self.write_json('public-attempts.json',rows)
        self.assertEqual(self.gate()[0],[{'name':'Full Heal','count':1}])

    def test_changed_retained_identity_or_log_is_rejected(self):
        self.produce();rows=copy.deepcopy(self.attempts);rows[0]['battle_end_epoch']+=1
        self.write_json('public-attempts.json',rows)
        with self.assertRaises(AssertionError):self.gate()
        self.write_json('public-attempts.json',self.attempts)
        self.write_log(self.logs[0],'[Player used Full Heal]\n[Player used Full Heal]\n')
        with self.assertRaises(AssertionError):self.gate()

    def test_wrong_target_or_checkpoint_chronology_rejected(self):
        self.produce();cfg={'id':127,'item_usage_reconciliation':'report.json','item_usage_reconciliation_round':1}
        with self.assertRaises(AssertionError):self.gate(config=cfg)
        self.post['save_mtime']=datetime.fromtimestamp(1150,timezone.utc).isoformat()
        with self.assertRaises(ValueError):self.produce()

    def test_glass_cannot_use_single_major_path(self):
        with patch('reconcile_glass_items.read_saved_inventory',side_effect=self.native):
            with self.assertRaises(ValueError):producer.build_report(*self.status_paths,self.logs[:1],self.saves,[self.records],[122])
        self.produce();cfg={'id':122,'gauntlet_id':'glass','gauntlet_round':1,
                            'item_usage_reconciliation':'report.json','item_usage_reconciliation_round':1}
        with self.assertRaises(AssertionError):self.gate(config=cfg)

    def test_zero_item_victory_is_verified_as_empty_list(self):
        self.post['bag']['contents']['FULLHEAL']=8;self.write_log(self.logs[0],'No executed bag items.\n')
        self.produce();self.assertEqual(self.gate()[0],[])

    def test_one_two_log_arity_and_unique_ids_required(self):
        with self.assertRaises(ValueError):producer.build_report(*self.status_paths,self.logs,self.saves,[self.records],[125])
        with self.assertRaises(ValueError):producer.build_report(*self.status_paths,self.logs,self.saves,[self.records]*2,[125,125])

    def test_log_creation_must_belong_to_observed_entry(self):
        rows=copy.deepcopy(self.attempts);rows[0]['interaction_start_epoch']=1090
        self.write_json('public-attempts.json',rows)
        with self.assertRaises(ValueError):self.produce()
        rows[0]['interaction_start_epoch']=1070;rows[0]['battle_start_epoch']=1075
        self.write_json('public-attempts.json',rows)
        with self.assertRaises(ValueError):self.produce()

    def test_filename_header_and_single_battle_binding(self):
        for text in ['Wrong header\n[Player used Full Heal]\n',
                     'Pokemon Reborn Fixture - '+self.logs[0].stem+'\nPokemon Reborn Fixture - '+self.logs[0].stem+'\n[Player used Full Heal]\n']:
            self.logs[0].write_text(text)
            with self.subTest(text=text),self.assertRaises(ValueError):self.produce()

    def test_log_creation_report_cannot_be_edited(self):
        report=self.produce();report['per_round'][0]['completed_log_identity']['created_epoch']+=1
        self.write_json('report.json',report)
        with self.assertRaises(AssertionError):self.gate()

    def test_missing_public_entry_or_snapshot_timezone_rejected(self):
        rows=copy.deepcopy(self.attempts);del rows[0]['interaction_start_epoch']
        self.write_json('public-attempts.json',rows)
        with self.assertRaises(KeyError):self.produce()
        self.write_json('public-attempts.json',self.attempts)
        self.pre['save_mtime']='1970-01-01T00:16:40';self.write_json('before.json',self.pre)
        with self.assertRaises(ValueError):self.produce()

    def test_cli_creates_only_new_report_with_explicit_evidence(self):
        argv=['reconcile_major_items.py',*map(str,self.status_paths),str(self.logs[0]),
              '--major-id','125','--attempts',str(self.records),'--before-save',str(self.saves[0]),
              '--after-save',str(self.saves[1]),'--output',str(self.report_path)]
        with patch.object(producer,'ROOT',self.root),patch('sys.argv',argv),patch('reconcile_glass_items.read_saved_inventory',side_effect=self.native),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(producer.main(),0)
        self.assertEqual(json.loads(self.report_path.read_text())['status'],'verified_counts')
        self.assertEqual(self.gate()[0],[{'name':'Full Heal','count':1}])


if __name__=='__main__':unittest.main()
