"""Sell one owned treasure, restock, and accept Randall's inspected Victini lead."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
s=json.loads((R/'notes/Postgame262-Will2-Cap120-status.json').read_text())
assert s['map']==38 and all(m['level']==120 and m['hp']==m['totalhp'] for m in s['party'])
assert s['bag']['contents'].get('STARPIECE',0)>=1 and s['trainer']['money']+4900>=13600
def run(n,*a):
 print('SUPPLY/QUEST',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
if '--after-sale' not in sys.argv:
 run('eventq',38,5,'talk');run('choose_dialog','Buy|Sell|Quit','Sell')
 run('shop_sell_one','Star Piece',4900)
run('mart_exit')
run('eventq',38,5,'talk');run('choose_dialog','Buy|Sell|Quit','Buy')
run('shop_buy','Ultra Potion',3,1200);run('mart_exit')
run('eventq',38,6,'enter');run('fly_to',520,'--carrier','Zapdos')
run('eventq',520,67,'enter');run('eventq',369,1,'talk');run('mart_open')
run('shop_buy','Timer Ball',10,1000);run('mart_exit')
run('checkpoint','Postgame262-Supplied')
run('city_enter',369,520);run('fly_to',527,'--carrier','Zapdos')
run('city_enter',527,826);run('city_enter',826,827)
run('eventq',827,51,'talk');run('dialog','--yes','--limit=40')
run('checkpoint','Postgame262-VictiniQuest')
assert json.loads((R/'notes/Postgame262-VictiniQuest-navigation.json').read_text())['variables']['613']==1
print('VICTINI QUEST ACCEPTED',flush=True)
