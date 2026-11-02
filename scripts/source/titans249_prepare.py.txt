"""Recruit an owned Fighting attacker and feed earned candy through ordinary UI."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TITANS PREP',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('city_enter',98,526)
run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter')
run('q','38,9,20,up:.12,c,wait:1')
run('pc_open_reviewed')
run('pc_exchange_named',18,3,'Mienshao','Amoonguss')
run('checkpoint','Postgame249-MienshaoParty')
run('train_candy_one','Mienshao',6,'XL')
run('checkpoint','Postgame249-MienshaoTrained')
