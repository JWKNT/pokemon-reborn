"""Legitimate shopping and return through already-completed Route4 climbs."""
from play import *
from locate import locate

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
import argparse
p=argparse.ArgumentParser();p.add_argument('--phase',type=int,choices=range(7),default=0);p.add_argument('--purchase-index',type=int,default=0);p.add_argument('--climb-index',type=int,choices=range(5),default=0);a=p.parse_args()
if a.phase<=0:
 run('fly_to',520);run('eventq',520,101,'enter');run('eventq',112,6,'enter');run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',8)
 run('eventq',4,4,'talk');run('mart_open')
if a.phase<=1:
 for name,count,price in [('X Attack',4,500),('X Sp. Def',10,350),('X Defend',4,550),('X Accuracy',3,950)][a.purchase_index if a.phase==1 else 0:]:run('shop_buy',name,count,price)
if a.phase<=2:
 run('mart_exit');run('eventq',4,6,'enter');run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',1);run('eventq',112,1,'enter')
 run('fly_to',519);run('eventq',519,116,'enter');run('eventq',38,5,'talk');run('mart_open')
if a.phase<=3:
 for name,count,price in [('Ultra Potion',20,1200),('Full Heal',10,600),('Super Repel',15,700)][a.purchase_index if a.phase==3 else 0:]:run('shop_buy',name,count,price)
if a.phase<=4:
 if not(a.phase==4 and a.climb_index):
  run('mart_exit');run('eventq',38,6,'enter');run('fly_to',413)
  run('eventq',413,21,'enter');run('eventq',418,2,'enter');run('use_field_item','Super Repel')
 for mid,eid,nextmap in [(412,1,710),(710,2,711),(711,3,713),(713,5,714),(714,3,715)][a.climb_index if a.phase==4 else 0:]:
  if mid==713:
   g=int(bool(json.loads((ROOT/'notes/navigation-state.json').read_text())['switches']['410']))
   run('layer_walk',713,48,36,g)
  run('eventq',mid,eid,'talk');run('dialog','--limit=10');assert locate(nextmap)[0]==nextmap
 run('eventq',715,63,'enter');run('eventq',733,20,'enter');run('eventq',733,22,'enter');run('checkpoint','Glass-returned-from-resupply')
if a.phase<=5:
 # Return to the local PC and restore the fixed six before committing to Glass.
 g=int(bool(json.loads((ROOT/'notes/navigation-state.json').read_text())['switches']['410']))
 run('layer_walk',732,70,48,g);run('eventq',732,56,'enter');run('eventq',738,3,'talk');run('pc_open_reviewed');run('pc_exchange_named',12,5,'Klinklang','Tranquill')
 run('eventq',738,1,'talk');run('dialog','--limit=10');run('eventq',738,4,'enter')
 run('party_front','Arcanine','Klinklang');run('give_held','Wave Incense','Swampert');run('checkpoint','Glass-restocked-fixed-six')
if a.phase<=6:
 # Ground exit previously unlocked the normal front door (native921True).
 run('layer_walk',732,70,24,1,1);run('eventq',732,68,'enter');run('eventq',733,7,'enter');run('eventq',733,18,'enter')
 run('eventq',715,60,'enter');run('eventq',730,5,'enter');run('eventq',733,66,'talk')
 run('choose_dialog','Ground Floor|B1F|B2F','B2F');run('linear_dialog',733,66,'--active','--past-choice')
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['432']=1;p.write_text(json.dumps(v))
 run('eventq',733,67,'enter');run('checkpoint','Glass-west-door-approach')
 run('layer_walk',732,38,9,1,1)
print('RESTOCKED, HEALED AND FIXED SIX RESTORED; CHECK BEFORE DOOR',flush=True)
