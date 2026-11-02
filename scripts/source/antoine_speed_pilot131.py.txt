"""Exit verified own stat popup and request one new speed boost."""
import subprocess,sys
from play import ROOT,read,act
t=read().lower();assert 'inspecting cofagrigus' in t and 'accuracy' in t
act('x:.12','wait:.6')
subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','antoine','--foes','Mamoswine','--item','X Speed','--min-hp','80','--output','work/antoine-xspeed-pilot131.json'],check=True)
