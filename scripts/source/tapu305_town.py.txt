"""Normal return and Bulu terrain team preparation."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('FINI PREP',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('use_field_item','Escape Rope');run('fly_to',519,'--carrier','Zapdos');run('city_enter',519,38)
run('eventq',38,3,'talk');run('heal')
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_exchange_named',26,1,'Comfey','Meowstic','--box',2)
run('checkpoint','Tapu305-BuluTeam')
