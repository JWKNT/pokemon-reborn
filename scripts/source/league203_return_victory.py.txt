"""Reviewed ordinary return to Florinia; stop on any unexpected battle/state."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
label=sys.argv[1];s=json.loads((R/'notes'/f'{label}-status.json').read_text())
assert all(any(move['move']==need for mon in s['party']for move in mon['moves'])for need in ['FLY','STRENGTH','ROCKCLIMB','ROCKSMASH'])
def run(script,*args):
 print('RETURN',script,*args,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1');env.pop('REBORN_FAST_KEYS',None)
 if script in ['q','eventq']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{script}.py'),*map(str,args)],check=True,env=env)
run('fly_to',781,'--carrier','Tranquill')
run('eventq',781,45,'enter');run('eventq',783,4,'enter')
run('victory_gem_cliff_event',812,101,'approach')
run('eventq',812,101,'talk');run('dialog','--yes','--limit=12')
run('checkpoint','Return203-Strength')
run('league203_return_boulder',101,'right',1,'Return203-Boulder101')
run('league203_return_boulder',96,'right',1,'Return203-Boulder96')
run('victory_gem_cliff_event',812,14,'enter')
run('victory_gem_cliff_event',813,7,'enter')
run('victory_gem_cliff_event',794,7,'enter')
run('q','796,25,17')
run('checkpoint','Return203-Florinia')
