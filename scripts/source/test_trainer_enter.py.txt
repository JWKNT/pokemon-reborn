"""Installed/pure paired trainer-source fixtures; never execute game controls."""
import argparse
import copy
import subprocess
import sys
import unittest
from trainer_enter import ROOT,dry_source,installed_event,validate_pair


class Tests(unittest.TestCase):
    def setUp(self):
        self.lyla=installed_event(763,45)['pages'][0]['list']
        self.ezra=installed_event(763,46)['pages'][0]['list']

    def test_exact_installed_pair_and_reverse_source_labels(self):
        result=validate_pair(self.lyla,self.ezra,45,46,'NWCultistF','Lyla & Ezra')
        self.assertEqual(result['primary'],['NWCultistF','Lyla'])
        self.assertEqual(result['paired'],['NWCultist','Ezra'])
        self.assertTrue(result['choice_free'])
        validate_pair(self.ezra,self.lyla,46,45,'NWCultist','Ezra & Lyla')

    def test_names_classes_duplicates_and_defeated_pages_fail_closed(self):
        for args in [(45,45,'NWCultistF','Lyla & Ezra'),
                     (45,46,'NWCultist','Lyla & Ezra'),
                     (45,46,'NWCultistF','Ezra & Lyla'),
                     (45,46,'NWCultistF','Lyla'),
                     (45,46,'NWCultistF','Lyla & Lyla')]:
            with self.subTest(args=args),self.assertRaises(AssertionError):
                validate_pair(self.lyla,self.ezra,*args)
        defeated=installed_event(763,46)['pages'][1]['list']
        with self.assertRaises(AssertionError):validate_pair(self.lyla,defeated,45,46,'NWCultistF','Lyla & Ezra')

    def test_either_source_choice_is_rejected(self):
        for code in [102,103,104]:
            for first in [True,False]:
                a,b=copy.deepcopy((self.lyla,self.ezra))
                (a if first else b).append({'code':code,'parameters':[['Yes','No'],2]})
                with self.subTest(code=code,first=first),self.assertRaises(AssertionError):
                    validate_pair(a,b,45,46,'NWCultistF','Lyla & Ezra')

    def test_source_dryrun_and_module_import_do_not_load_play(self):
        args=argparse.Namespace(map=763,event=45,paired_event=46,source_page=None,
                                trainer_class='NWCultistF',name='Lyla & Ezra')
        self.assertTrue(dry_source(args)['no_UI_or_runtime_reads'])
        subprocess.run([sys.executable,'-c',
            "import sys; sys.path.insert(0,'scripts'); import trainer_enter; assert 'play' not in sys.modules"],
            cwd=ROOT,check=True,capture_output=True)

    def test_existing_intro_and_choice_refusals_are_retained(self):
        # Source invariants matter because the paired extension does not add
        # a new route for accepting an unseen intro or GUI choice.
        source=(ROOT/'scripts/trainer_enter.py').read_text()
        self.assertIn("assert intro,'Unobserved intro requires review'",source)
        self.assertIn("raise SystemExit('Unexpected intro state')",source)
        self.assertIn("else:assert not any(c['code'] in [102,103,104]for c in cs)",source)
        self.assertIn("for _ in range(a.intro_cycles):",source)


if __name__=='__main__':unittest.main()
