"""Normal PC and mart preparation for the reviewed Steel/Fairy cave encounters."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('CAVE PREP',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Postgame292-Town-status.json').read_text());assert s['map']==38
if '--pc-done' not in sys.argv:
 run('eventq',38,4,'talk');run('pc_open_reviewed')
 run('pc_take_owned_item',11,'Ludicolo','Wise Glasses')
run('give_held','Wise Glasses','Magearna')
run('take_held','Zapdos','Tech Glasses')
run('teach_machine','TM91','Magearna','Flash Cannon',0)
run('eventq',38,5,'talk');run('mart_open')
run('shop_buy','Super Repel',30,700)
run('shop_buy','Escape Rope',10,550)
run('mart_exit');run('checkpoint','Postgame292-CaveReady')
s=json.loads((R/'notes/Postgame292-CaveReady-status.json').read_text())
m=next(x for x in s['party']if x['species']=='MAGEARNA');assert m['item']=='WISEGLASSES' and m['moves'][0]['move']=='FLASHCANNON'
print('PC EQUIPMENT AND TRAVEL SUPPLIES VERIFIED',flush=True)
