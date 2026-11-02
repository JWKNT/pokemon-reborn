"""Normal PC exchanges from reviewed Giratina postquest owned-box evidence."""
import os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1', REBORN_ROUTE_STEP_PAUSE='.10', REBORN_ROUTE_CHUNK='56')
def run(name,*args):
    print('NECROZMA TEAM',name,*args,flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*map(str,args)],check=True)
run('eventq',827,3,'talk')
run('pc_open_reviewed')
run('pc_select_box',1)
run('pc_exchange_named',23,1,'Mawile','Heatran','--box',1,'--stay-open')
run('pc_select_box',2)
run('pc_exchange_named',25,3,'Darkrai','Volcanion','--box',2)
run('checkpoint','Necrozma362-Roster')
