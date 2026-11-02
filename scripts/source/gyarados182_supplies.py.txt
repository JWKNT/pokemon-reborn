"""Normal fixed-budget shopping after the verified Outrage checkpoint."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=json.loads((R/'notes/Gyarados182-Outrage-trained-status.json').read_text())
assert s['map']==522 and s['trainer']['money']>=25000

def run(n,*args):
 print('STAGE',n,*args,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1')
 if n=='eventq':e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,args)],check=True,env=e)

if '--after-held' not in sys.argv:
 if '--after-berries' not in sys.argv:
  run('fly_to',520,'--carrier','Tranquill');run('eventq',520,101,'enter');run('eventq',112,6,'enter')
  run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',2)
  run('eventq',114,2,'talk');run('mart_open');run('shop_buy','Persim Berry',4,400)
 run('mart_exit')
 run('give_held','Persim Berry','Gyarados','--pocket','Berries')
run('eventq',114,6,'enter');run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',8)
run('eventq',4,4,'talk');run('mart_open')
run('shop_buy','X Sp. Def',4,350);run('shop_buy','X Defend',3,550);run('mart_exit')
run('eventq',4,6,'enter');run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',1)
run('eventq',112,1,'enter');run('fly_to',519,'--carrier','Tranquill');run('eventq',519,116,'enter')
run('eventq',38,5,'talk');run('mart_open');run('shop_buy','Max Potion',6,2500);run('mart_exit')
run('eventq',38,3,'talk');run('heal');run('checkpoint','Gyarados182-Supplies-ready')
s=json.loads((R/'notes/Gyarados182-Supplies-ready-status.json').read_text())
g=next(m for m in s['party']if m['species']=='GYARADOS')
assert g['item']=='PERSIMBERRY' and g['ev']==[0,252,0,0,0,252]
assert s['bag']['contents'].get('XSPDEF',0)>=4 and s['bag']['contents'].get('MAXPOTION',0)>=9
print('SUPPLIES VERIFIED THROUGH NORMAL SAVE',flush=True)
