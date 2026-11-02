"""Reviewed normal-menu final Rayquaza preparation after Silva candy training."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=json.loads((R/'notes/Postgame367-Silva6-Cap145-status.json').read_text())
assert all(m['level']==145 and m['hp']==m['totalhp'] for m in s['party'])
assert s['trainer']['money']>=8500
assert s['bag']['contents']['TM17']==1 and s['bag']['contents']['AMPLIFIELDROCK']>=1
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(name,*args):
 print('RAYQUAZA PREP',name,args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],env=env,check=True)
run('teach_machine','TM17','Magearna','Protect',0)
run('give_held','Amplifield Rock','Magearna')
run('eventq',38,5,'talk');run('mart_open')
run('shop_buy','Max Potion',2,2500)
run('shop_buy','Super Repel',5,700)
run('mart_exit')
run('party_front','Mienshao','Magearna')
run('checkpoint','Rayquaza367-Prepared')
run('eventq',38,6,'enter')
run('fly_to',814,'--carrier','Zapdos')
run('q','814,34,52')
run('checkpoint','Rayquaza367-Ready')
