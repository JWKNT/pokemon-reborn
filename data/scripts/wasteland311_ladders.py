"""Return through the solved Wasteland ladders using normal checked inputs."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('LADDER RETURN',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
def enter(e):run('eventq',279,e,'enter')
nav=json.loads((R/'notes/navigation-state.json').read_text());assert all(nav['switches'][str(k)] for k in [383,384,385,386])
run('city_enter',277,278);run('eventq',278,2,'enter');run('checkpoint','Mewtwo311-LadderReturn')
nav=json.loads((R/'notes/navigation-state.json').read_text());p=nav['positions']['279']
assert p['31'] in [[21,60],[25,60]] and p['29'] in [[47,60],[50,60]],p
run('wall309_strength','Mienshao');enter(19);enter(21)
if p['31']==[21,60]:run('wasteland309_push',279,31,'right',4,'Mewtwo311-LadderClear1')
enter(10);enter(22)
if p['29']==[47,60]:run('wasteland309_push',279,29,'right',3,'Mewtwo311-LadderClear3')
enter(14);enter(16);enter(4)
run('city_enter',278,280);run('city_enter',280,874);run('q','874,25,13');run('checkpoint','AnomalyMewtwo311-Entry')
print('READY FOR ANOMALY184 ATTEMPT2; no fight started',flush=True)
