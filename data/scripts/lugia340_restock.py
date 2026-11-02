"""Normal UI restock and trained Spore catcher exchange after Lugia."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('RESTOCK',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('shop_sell_one','Relic Copper',1000)
run('shop_sell_one','Relic Copper',1000)
run('mart_exit');run('eventq',38,5,'talk');run('mart_open');run('shop_buy','Max Repel',10,900);run('mart_exit')
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',3);run('pc_exchange_named',6,5,'Amoonguss','Latias','--box',3)
run('checkpoint','Lugia340-Catcher')
run('eventq',38,6,'enter');run('fly_to',520,'--carrier','Zapdos','--origin',519)
run('eventq',520,67,'enter');run('eventq',369,1,'talk');run('mart_open');run('shop_buy','Timer Ball',20,1000);run('mart_exit')
run('checkpoint','Lugia340-Restocked')
