"""Reviewed normal travel to the accessible Grand Stairway Heart Scale."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
os.environ.pop('REBORN_FAST_KEYS',None)
def run(s,*args):
 print('STAGE',s,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/(s+'.py')),*map(str,args)],check=True,cwd=R)
if '--stairs' not in sys.argv:
 run('use_field_item','Super Repel')
 run('eventq',633,3,'enter')
 run('fly_to',355,'--carrier','Tranquill')
 run('eventq',355,118,'talk');run('heal')
 run('fly_to',527,'--carrier','Tranquill')
 run('eventq',527,42,'talk');run('dialog','--limit=8')
 run('checkpoint','Saphira-GrandStair-guard-open')
 run('eventq',527,55,'enter')
run('eventq',588,2,'enter')
run('eventq',177,2,'enter')
run('eventq',178,4,'enter')
run('eventq',179,6,'enter')
run('eventq',180,3,'enter')
run('eventq',179,36,'item')
run('checkpoint','Saphira-HeartScale-one')
s=json.loads((R/'notes/Saphira-HeartScale-one-status.json').read_text())
assert s['bag']['contents']['HEARTSCALE']==1
