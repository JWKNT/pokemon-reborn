"""Leave Seventh Street normally and resume the reviewed Victory Road return."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('RETURN',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1');env.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
run('eventq',324,1,'enter');run('eventq',168,12,'enter');run('eventq',168,18,'talk')
run('choose_dialog','7th Street|Lapis Ward','Lapis Ward');run('dialog','--limit=5')
run('checkpoint','Prep204-Seventh-exit')
try:run('eventq',168,11,'enter')
except subprocess.CalledProcessError:
 from locate import locate
 assert locate(168)==(168,30,6),'Unexpected elevator exit state'
run('eventq',168,2,'enter')
run('checkpoint','Prep204-Lapis-return')
run('league203_return_victory','Prep204-Lapis-return')
