"""Normal return, healing and three verified reserve exchanges for Koko preparation."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('KOKO PREP',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('eventq',855,26,'enter');run('use_field_item','Escape Rope')
run('fly_to',519,'--carrier','Zapdos');run('city_enter',519,38)
run('eventq',38,3,'talk');run('heal')
for slot,party,inc,out in [(0,2,'Excadrill','Comfey'),(25,5,'Cresselia','Mawile'),(13,1,'Zeraora','Magearna')]:
 run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_exchange_named',slot,party,inc,out,'--box',2)
run('checkpoint','Koko306-Team')
