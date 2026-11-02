"""Normal-controls Mega Ring errands, ending before any unreviewed battle."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
assert json.loads((R/'notes/League220-EustaceMotherConfirmed-navigation.json').read_text())['switches']['2154']
run('eventq',612,2,'enter');run('fly_to',523)
run('eventq',523,2,'enter');run('eventq',539,6,'enter');run('eventq',522,22,'enter')
run('checkpoint','League220-SantiagoRevisit')
run('league220_santiago_guide')
run('league220_rooftop_prep')
