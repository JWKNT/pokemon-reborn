"""Normal menu preparation after Core puzzles; does not approach/start battle."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(n,*a):
 print('HEATRAN PREP',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('teach_machine','TM78','Swampert','Bulldoze',1,'--single-step')
run('give_held','Safety Goggles','Volcanion','--single-step')
run('party_swap',0,2)
run('checkpoint','Heatran295-BossPrepared')
