"""Reviewed ordinary city and Grand Stairway shard pickups."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(name,*a):
 env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if name!='fly_to':env['REBORN_FAST_KEYS']='1'
 else:env.pop('REBORN_FAST_KEYS',None)
 print('STAGE',name,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,a)],env=env,check=True)
p=sys.argv[1]
if p=='beryl':
 run('fly_to',525);run('eventq',525,2,'enter');run('eventq',159,4,'talk');run('heal');run('party_front','Swampert');run('eventq',159,8,'enter');run('q','525,0,10,left,wait:2');run('eventq',544,42,'item');run('checkpoint','League218-BerylShard')
elif p=='stairway':
 run('eventq',527,55,'enter');run('eventq',588,2,'enter');run('field_repel','Max Repel')
 run('eventq',177,2,'enter');run('eventq',178,2,'enter');run('eventq',179,29,'item');run('eventq',179,30,'item');run('checkpoint','League218-StairwayShards')
else:raise SystemExit('Unknown phase')
