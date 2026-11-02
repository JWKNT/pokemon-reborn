"""Source-reviewed Mega Ring introduction and first owner's return via ordinary UI."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':env['REBORN_FAST_KEYS']='1'
 else:env.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=env,check=True)
def scene(m,e):
 run('eventq',m,e,'talk');run('linear_dialog',m,e,'--active','--burst')
index=json.loads((R/'work/219-cages-owned-index.json').read_text())
def boxslot(species):
 matches=[x for x in index if x['species']==species];assert len(matches)==1 and matches[0]['box']==0;return matches[0]['slot']
scene(324,26);run('checkpoint','League219-CageArc');run('seventh219_exit')
run('eventq',524,24,'enter');run('eventq',166,7,'talk');run('pc_open_reviewed');run('pc_exchange_named',boxslot('LOUDRED'),1,'Loudred','Kricketune')
run('eventq',166,7,'talk');run('pc_open_reviewed');run('pc_exchange_named',boxslot('JIGGLYPUFF'),4,'Jigglypuff','Sylveon')
run('eventq',166,8,'enter');run('fly_to',527);run('eventq',527,87,'enter');scene(826,8);run('checkpoint','League219-RingStarted')
run('eventq',826,2,'enter');run('fly_to',523);run('eventq',523,3,'enter');scene(534,4);run('checkpoint','League219-LillinRefusal')
run('quest219_return',534,4,1,'Loudred');run('checkpoint','League219-LoudredReturned')
run('eventq',534,3,'enter');run('party_front','Swampert');run('eventq',523,2,'enter');run('eventq',539,6,'enter');run('eventq',522,22,'enter');run('checkpoint','League219-SantiagoReady')
