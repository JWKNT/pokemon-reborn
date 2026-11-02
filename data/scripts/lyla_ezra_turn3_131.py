"""Finite root-reviewed turn3: Whimsicott/Kommo-o, Cryo Ice +Mien WideGuard."""
import subprocess,sys,re
from play import ROOT,read
t=read().lower();assert 'hexan' in t and 'fight'in t and 'kommo' in t and ('himsicott'in t or 'whimsicott'in t)
def run(*a):subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),*map(str,a)],check=True)
run(1,1,'--foe-names','Whimsicott,Kommo-o','--watch')
t=read().lower();assert 'mienshao'in t and 'what will'in t and 'fight'in t
run(1,'--watch')
