"""Prepare owned field moves and Fairy spread damage, then replenish capture supplies."""
from pathlib import Path
import json,subprocess,sys,os
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
label=sys.argv[1]
s=json.loads((R/'notes'/f'{label}-status.json').read_text())
assert s['map']==38 and all(m['level']==125 and m['hp']==m['totalhp'] for m in s['party'])
assert s['trainer']['money']>=70000

def run(n,*a):
 print('LATI PREP',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
for args in [('TM99','Magearna','Dazzling Gleam',0),('TMX4','Volcanion','Strength',2),('TMX6','Swampert','Dive',0),('TMX5','Swampert','Waterfall',3)]:run('teach_machine',*args)
run('checkpoint','Postgame289-LatiBuild')
s=json.loads((R/'notes/Postgame289-LatiBuild-status.json').read_text())
for species,slot,move in [('MAGEARNA',0,'DAZZLINGGLEAM'),('VOLCANION',2,'STRENGTH'),('SWAMPERT',0,'DIVE'),('SWAMPERT',3,'WATERFALL')]:
 assert next(m for m in s['party']if m['species']==species)['moves'][slot]['move']==move
run('eventq',38,5,'talk');run('choose_dialog','Buy|Sell|Quit','Buy')
run('shop_buy','Full Restore',6,3000);run('shop_buy','Ultra Potion',10,1200);run('mart_exit')
run('eventq',38,6,'enter');run('fly_to',520,'--carrier','Zapdos')
run('eventq',520,67,'enter');run('eventq',369,1,'talk');run('mart_open')
run('shop_buy','Timer Ball',40,1000);run('mart_exit');run('checkpoint','Postgame289-LatiSupplied')
run('city_enter',369,520);run('fly_to',527,'--carrier','Zapdos')
run('city_enter',527,826);run('city_enter',826,827)
run('eventq',827,81,'talk');run('dialog','--yes','--limit=40')
run('checkpoint','Postgame289-LatiQuest')
s=json.loads((R/'notes/Postgame289-LatiQuest-navigation.json').read_text());assert s['variables']['622']==1
print('NYU L AT I QUEST ACCEPTED',flush=True)
