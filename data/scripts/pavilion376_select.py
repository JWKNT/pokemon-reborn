"""Enter attempt3 with an explicitly reviewed facility trio; stop before Confirm."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56')
def run(s,*a):
 print('PAVILION SELECT',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',827,95,'talk')
run('choose_dialog','Yes|No','Yes')
run('choose_dialog','Singles|Doubles','Singles')
run('play','c','wait:1')
run('select_three_reviewed','Darkrai|Magearna|Cresselia','work/376-pavilion-selection.png')
