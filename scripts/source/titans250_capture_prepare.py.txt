"""Normal travel, healing and owned catch-support exchange before Titan captures."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CAPTURE PREP',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
if '--from-cave' not in sys.argv:
 run('eventq',825,125,'enter');run('play','wait:3')
 run('eventq',825,3,'enter');run('play','wait:3')
run('city_enter',636,360)
run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter')
run('eventq',38,3,'talk')
run('heal')
run('q','38,9,20,up:.12,c,wait:1')
run('pc_open_reviewed')
run('pc_exchange_named',18,0,'Amoonguss','Mienshao')
run('checkpoint','Postgame250-CatchParty')
