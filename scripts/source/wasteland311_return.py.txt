"""Return with the prepared travel team, checking ordinary saved room state."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('RETURN',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
def checkpoint(label):run('checkpoint',label)
def positions(mid):return json.loads((R/'notes/navigation-state.json').read_text())['positions'][str(mid)]
run('city_enter',38,519);run('fly_to',232,'--carrier','Zapdos')
run('surface_walk',232,18,67);run('eventq',232,1,'enter');run('city_enter',231,272);run('city_enter',272,273)
checkpoint('Mewtwo311-CrystalReturn')
world=json.loads(subprocess.check_output(['ruby',str(R/'scripts/map_state.rb')],stderr=subprocess.DEVNULL));assert world['map']==273
if world['events']['7']['character']:
 p=R/'notes/navigation-overrides.json';over=json.loads(p.read_text());over['273']=[k for k in over.get('273',[]) if int(k)!=7];p.write_text(json.dumps(over,indent=2)+'\n')
 run('eventq',273,7,'smash');checkpoint('Mewtwo311-CrystalPassage')
run('city_enter',273,274);run('connected_walk',274,230);run('connected_walk',230,249);run('city_enter',249,275)
checkpoint('Mewtwo311-Room275Entry')
p=positions(275)['2'];assert p in [[14,9],[16,9]],p
if p==[14,9]:run('wall309_strength','Mienshao');run('wasteland309_push',275,2,'right',2,'Mewtwo311-Room275Clear')
run('city_enter',275,276);checkpoint('Mewtwo311-Room276Entry')
p=positions(276);assert p['1'] in [[11,10],[12,10]] and p['2'] in [[13,12],[14,12]],p
if p['1']==[11,10] or p['2']==[13,12]:run('wall309_strength','Mienshao')
if p['1']==[11,10]:run('wasteland309_push',276,1,'right',1,'Mewtwo311-Room276A')
if p['2']==[13,12]:run('wasteland309_push',276,2,'right',1,'Mewtwo311-Room276B')
run('city_enter',276,277);checkpoint('Mewtwo311-WallReturn')
print('WALL RETURN CHECKPOINT; review route through solved canisters',flush=True)
