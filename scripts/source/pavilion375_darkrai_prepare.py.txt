"""Normal PC withdrawal and held-item preparation from frozen owned evidence."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(s,*a):
 print('PAVILION PREP',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('checkpoint','Pavilion375-Loss')
run('eventq',827,3,'talk')
run('pc_open_reviewed')
run('pc_select_box',2)
run('pc_exchange_named',22,3,'Darkrai','Mienshao','--box',2)
run('give_held','Wise Glasses','Darkrai')
run('overworld')
run('checkpoint','Pavilion375-DarkraiReady')
