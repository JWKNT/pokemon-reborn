"""Decline the reviewed free switch and heal once; stop at command."""
import subprocess,sys
from play import ROOT,read,act
t=read().lower();assert 'yes' in t and 'no' in t and 'change' in t
act('x:.12','wait:.7')
subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','antoine','--foes','Liepard','--item','Ultra Potion','--min-hp','1','--output','work/antoine-liep-heal131.json'],check=True)
