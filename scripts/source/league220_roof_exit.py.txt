"""Normal-controls Mega Ring errands, ending before any unreviewed battle."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
assert json.loads((R/'notes/navigation-state.json').read_text())['switches']['714'] is True
run('eventq',573,1,'enter');run('eventq',129,3,'talk');run('choose_dialog','1F|Rooftop','1F','--source',129,3)
run('dialog','--limit=5');run('checkpoint','League220-GroundFloor')
run('eventq',129,2,'enter');run('eventq',118,2,'enter');run('eventq',521,26,'enter')
run('league220_vanillite_return')
