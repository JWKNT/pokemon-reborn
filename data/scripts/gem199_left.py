"""Normal left pressure-pad route, each grouped push checked by a normal save."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=env)
steps=[('victory_gem_cliff_event.py',791,46,'item'),('victory_gem_cliff_event.py',791,31,'approach'),('party_open.py',),('party_pick.py','Mienshao','--single'),('play.py','down','c','wait:2'),('dialog.py','--limit=6'),('gem_boulder199.py',31,'down',1,'Gem199-left-d1'),('gem_boulder199.py',31,'right',2,'Gem199-left-r2'),('gem_boulder199.py',31,'up',2,'Gem199-left-u2'),('gem_boulder199.py',31,'right',3,'Gem199-left-r3'),('gem_boulder199.py',31,'up',1,'Gem199-left-u1'),('gem_boulder199.py',31,'right',2,'Gem199-left-pad')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,s in enumerate(steps,1):
 if i>=start:run(*s);print('LEFT GEM STEP',i,'DONE',flush=True)
assert json.loads((R/'notes/navigation-state.json').read_text())['switches']['1171']
