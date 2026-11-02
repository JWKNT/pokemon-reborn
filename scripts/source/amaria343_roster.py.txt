"""Swap in owned doubles supports through normal Grand Hall PC controls."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(s,*a):
 print('AMARIA TEAM',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',2)
run('pc_exchange_named',13,1,'Mienshao','Latias','--box',2)
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',3)
run('pc_exchange_named',2,4,'Meowstic','Mawile','--box',3)
run('checkpoint','Amaria343-Supports')
run('postgame_candy_spend','Amaria343-Supports',135)
run('teach_machine','TM62','Mienshao','Acrobatics',3)
run('take_held','Mienshao','Protective Pads')
run('checkpoint','Amaria343-Prepared')
