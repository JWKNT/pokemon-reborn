"""Prepare Amaria support with ordinary shopping, EV Tuner UI, and held-item menus."""
import os,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('AMARIA PREP',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
files=list((R/'notes').glob('Postgame343-Jace*-status.json'))
latest=max(files,key=lambda p:int(p.name.split('Jace')[1].split('-')[0]))
s=json.loads(latest.read_text())
assert s['map']==38 and s['trainer']['money']>=45000
assert all(p['hp']==p['totalhp'] and p['status'] is None for p in s['party'])
run('overworld')
run('eventq',38,5,'talk');run('mart_open')
run('shop_buy','Escape Rope',5,550);run('shop_buy','Ultra Potion',1,1200);run('mart_exit')
run('eventq',38,6,'enter');run('fly_to',530,'--carrier','Zapdos','--origin',519)
run('city_enter',530,522)
run('eventq',522,10,'talk')
run('linear_dialog',522,10,'--active','--until-choice')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',522,10,'--active','--past-choice')
run('checkpoint','Amaria343-Tuners')
s=json.loads((R/'notes/Amaria343-Tuners-status.json').read_text())
assert s['bag']['contents']['EVTUNER']==5 and s['bag']['contents']['ESCAPEROPE']==5
run('field_medicine','EV Tuner','Mienshao')
run('ev_tuner_swap',2,5)
run('overworld')
run('give_held','Amplifield Rock','Meowstic')
run('party_front','Volcanion','Mienshao')
run('checkpoint','Amaria343-EVReady')
s=json.loads((R/'notes/Amaria343-EVReady-status.json').read_text())
m=next(m for m in s['party'] if m['name']=='Mienshao')
assert m['speed']>334 and m['item'] is None
assert s['bag']['contents']['EVTUNER']==4
assert next(m for m in s['party'] if m['name']=='Meowstic')['item']=='AMPLIFIELDROCK'
print('AMARIA EV PREPARATION VERIFIED',m,flush=True)
