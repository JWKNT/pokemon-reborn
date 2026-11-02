"""Restore the healed core through named PC exchanges, then stop in Nightclub foyer."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('NEXT TIER TEAM',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for slot,party,inc,out in [(13,2,'Magearna','Zeraora')]:
 run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_exchange_named',slot,party,inc,out,'--box',2)
run('checkpoint','Postgame307-Core')
run('city_enter',38,519);run('fly_to',527,'--carrier','Zapdos');run('city_enter',527,826)
run('q','826,10,5');run('checkpoint','Postgame307-NightclubLobby')
