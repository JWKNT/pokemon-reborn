"""Reviewed normal quest continuation after observed Kai victory."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if s in ['eventq','q','battle_batch']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=e)
def clear_turbo():
 from play import act,read
 p=R/'notes/current-run-control.json';c=json.loads(p.read_text());t=read().lower();assert 'fight' not in t
 if c.get('battle_turbo_enabled'):
  act('m:.12','wait:.35','m:.12','wait:.35');c.update(battle_turbo_enabled=False,battle_turbo=False);p.write_text(json.dumps(c,indent=2))
if '--purchase-complete' not in sys.argv:
 for m,e in [(324,1),(168,12)]:run('eventq',m,e,'enter')
 run('eventq',168,18,'talk');run('choose_dialog','7th Street|Lapis Ward','Lapis Ward');run('dialog','--limit=5')
 run('checkpoint','Magikarp179-elevator-exit')
 for m,e in [(168,11),(168,2)]:run('eventq',m,e,'enter')
 run('fly_to',519,'--carrier','Tranquill')
 run('eventq',519,116,'enter');run('eventq',38,5,'talk');run('mart_open')
 run('shop_buy','Super Repel',20,700)
run('mart_exit')
run('party_take_named','Sylveon')
run('teach_machine','TMX3 Surf','Swampert','Surf',3,'--single-step')
run('checkpoint','Magikarp179-travel-prepared')
run('eventq',38,6,'enter')
run('fly_to',523,'--carrier','Tranquill')
run('eventq',523,112,'enter');run('eventq',133,1,'talk')
run('linear_dialog',133,1,'--source-page',12,'--burst')
run('checkpoint','Magikarp179-decoys-start')
run('eventq',133,4,'enter')
print('DECOYS READY JASPER',flush=True)
