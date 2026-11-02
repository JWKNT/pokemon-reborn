"""Bounded normal-control preparation routes; item events reviewed from installed sources."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*args):
 env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if s not in ['fly_to','dept_floor']:env['REBORN_FAST_KEYS']='1'
 else:env.pop('REBORN_FAST_KEYS',None)
 print('STAGE',s,*args,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],env=env,check=True)
p=sys.argv[1]
if p in ['circus','circus-pickups']:
 if p=='circus':
  run('q','633,1,8,left,wait:2');run('fly_to',355)
 for e in [103,96,95,99]:run('eventq',355,e,'item')
 run('eventq',355,118,'talk');run('heal');run('checkpoint','League218-CircusShards')
elif p=='onyx':
 run('fly_to',521);run('eventq',521,5,'item');run('checkpoint','League218-OnyxShard')
elif p=='clay':
 run('fly_to',520);run('eventq',520,101,'enter');run('eventq',112,6,'enter')
 run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',3)
 run('eventq',141,1,'talk');run('mart_open');run('shop_buy','Light Clay',1,200);run('mart_exit')
 run('give_held','Light Clay','Hexan','--single-step');run('checkpoint','League218-LightClay')
elif p=='depart-peridot':
 run('eventq',141,6,'enter');run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',1)
 run('eventq',112,1,'enter');run('fly_to',530);run('eventq',530,153,'enter')
 run('eventq',531,1,'item');run('checkpoint','League218-PeridotShard')
elif p in ['seventh','seventh-pickups']:
 if p=='seventh':
  run('eventq',531,7,'enter');run('fly_to',524);run('eventq',524,30,'enter');run('eventq',168,8,'enter')
  raise SystemExit('Use elevator E18: select 7th Street, confirm, then exit E11 and E15 before pickups')
 for e in [65,63,64,59,66,61,60,62]:run('eventq',324,e,'item')
 run('eventq',324,7,'enter');run('eventq',325,12,'item');run('checkpoint','League218-SeventhShards')
else:raise SystemExit('Unknown phase')
