"""Normal right pressure-pad pushes; each group verified from a normal save."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(*a):subprocess.run([sys.executable,str(R/'scripts'/a[0]),*map(str,a[1:])],check=True,env=env)
steps=[('victory_gem_cliff_event.py',791,32,'approach'),('party_open.py',),('party_pick.py','Mienshao','--single'),('play.py','down','c','wait:2'),('dialog.py','--limit=6'),('gem_boulder199.py',32,'left',3,'Gem199-right-l3'),('gem_boulder199.py',32,'up',2,'Gem199-right-u2'),('gem_boulder199.py',32,'left',1,'Gem199-right-pad'),('victory_gem_cliff_event.py',791,45,'item')]
start=int(sys.argv[1])if len(sys.argv)>1 else 1
for i,s in enumerate(steps,1):
 if i>=start:run(*s);print('RIGHT GEM PAD STEP',i,'DONE',flush=True)
assert json.loads((R/'notes/navigation-state.json').read_text())['switches']['1170']
