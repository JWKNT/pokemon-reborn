"""Restore the sixth battler through Florinia's normal remote PC."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('FLORINIA',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1');env.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
s=json.loads((R/'notes/Return203-Florinia-status.json').read_text());assert s['map']==796 and s['party'][5]['name']=='Tranquill'
run('eventq',796,28,'talk');run('choose_dialog','PC|Help','PC');run('pc_open_reviewed');run('pc_exchange_named',15,5,'Hexan','Tranquill')
run('checkpoint','Ruby204-Full-team')
run('eventq',796,71,'enter');run('victory_gem_cliff_event',791,7,'enter')
run('victory_gem_cliff_event',799,6,'enter');run('checkpoint','Ruby204-Final-chamber-entry')
