"""Normal controls from Grand Stairway lobby to final Route4 shard and Seventh Street."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
run('eventq',178,11,'smash');run('eventq',178,1,'enter');run('eventq',177,1,'enter');run('eventq',588,1,'enter');run('fly_to',413);run('eventq',413,21,'enter');run('eventq',418,2,'enter')
run('eventq',412,32,'item');run('checkpoint','League219-AllShards');run('fly_to',524)
run('eventq',524,30,'enter');run('eventq',168,8,'enter');run('eventq',168,18,'talk')
from play import act,read
s=read().lower();assert '7th street' in s and 'lapis ward' in s,s
act('c','wait:2');s=read();print(s,flush=True);assert '7th Street Level' in s,s
act('c','wait:1')
f=R/'notes/navigation-state.json';v=json.loads(f.read_text());v['variables']['79']=1;f.write_text(json.dumps(v))
run('eventq',168,11,'enter');run('eventq',168,15,'enter')
