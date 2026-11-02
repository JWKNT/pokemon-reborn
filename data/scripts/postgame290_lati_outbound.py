"""Normal travel to the reviewed Ametrine ice boulder; stop before pushing."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('LATI OUTBOUND',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
if '--mountain' not in sys.argv:
 if '--from-zapdos-menu' in sys.argv:
  run('fly_to',413,'--carrier','Zapdos','--menu-open','--origin',527)
 else:
  run('city_enter',827,826);run('city_enter',826,527);run('fly_to',413,'--carrier','Zapdos')
 run('eventq',413,62,'enter');run('eventq',418,5,'enter');run('eventq',361,1,'enter')
 run('use_field_item','Super Repel')
run('surface_walk',364,82,60)
run('play','down:.12','c','wait:.8');run('choose_dialog','Yes|No','Yes');run('dialog','--limit=12')
run('checkpoint','Postgame290-Ametrine1F')
s=json.loads((R/'notes/Postgame290-Ametrine1F-status.json').read_text());assert s['map']==375 and s['position']==[44,12]
run('surface_walk',375,40,23);run('waterfall_step',375,40,23,'down',375,40,33)
run('surface_walk',375,16,32);run('checkpoint','Postgame290-IceBoulder')
print('AT RIGHT SIDE OF ICE BOULDER; PUSH NOT EXECUTED',flush=True)
