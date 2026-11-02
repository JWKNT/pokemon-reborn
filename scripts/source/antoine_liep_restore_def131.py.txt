"""Exit own inspect and repair the publicly measured negative Defense stage."""
import subprocess,sys
from play import ROOT,read,act
t=read().lower();assert 'inspecting cofagrigus' in t and '272' in t and '222' in t
act('x:.12','wait:.6')
subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','antoine','--foes','Liepard','--item','X Defend','--min-hp','200','--output','work/antoine-liep-xdef131.json'],check=True)
