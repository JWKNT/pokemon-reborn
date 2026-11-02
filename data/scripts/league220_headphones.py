"""Normal-controls Mega Ring errands, ending before any unreviewed battle."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
run('eventq',534,4,'talk');run('choose_dialog','Yes|No','Yes','--source',534,4)
run('linear_dialog',534,4,'--source-page',3,'--after-last-choice','--past-choice','--burst');run('checkpoint','League220-JigglypuffReturned')
run('eventq',534,3,'enter');run('fly_to',524);run('eventq',524,48,'enter')
run('eventq',612,6,'talk');run('linear_dialog',612,6,'--source-page',1,'--burst');run('checkpoint','League220-EustaceMother')
assert json.loads((R/'notes/League220-EustaceMother-navigation.json').read_text())['switches']['2154'], 'Mother moved; return for verified dialogue before proceeding'
run('eventq',612,2,'enter');run('fly_to',523)
run('eventq',523,2,'enter');run('eventq',539,6,'enter');run('eventq',522,22,'enter')
run('checkpoint','League220-SantiagoRevisit')
