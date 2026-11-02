"""Normal-controls Mega Ring errands, ending before any unreviewed battle."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 e=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 if n!='fly_to':e['REBORN_FAST_KEYS']='1'
 else:e.pop('REBORN_FAST_KEYS',None)
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],env=e,check=True)
# Start in Onyx School120 with rooftop victory714 already saved.
assert json.loads((R/'notes/navigation-state.json').read_text())['switches']['714'] is True
party=json.loads((R/'notes/League220-GroundFloor-status.json').read_text())['party']
exca=next(i for i,m in enumerate(party)if m['name']=='Excadrill');mien=next(i for i,m in enumerate(party)if m['name']=='Mienshao')
run('eventq',120,12,'talk');run('pc_open_reviewed');run('pc_exchange_named',5,exca,'Tranquill','Excadrill')
run('eventq',120,12,'talk');run('pc_open_reviewed');run('pc_exchange_named',18,mien,'Vanillite','Mienshao')
run('eventq',120,8,'talk');run('heal');run('checkpoint','League220-VanilliteReturnParty')
run('eventq',120,1,'enter');run('fly_to',524);run('eventq',524,48,'enter');run('eventq',612,3,'enter')
run('eventq',612,7,'talk');run('linear_dialog',612,7,'--source-page',0,'--burst');run('checkpoint','League220-EustaceHome')
run('quest219_return',612,7,1,'Vanillite');run('checkpoint','League220-VanilliteReturned')
assert json.loads((R/'notes/navigation-state.json').read_text())['switches']['1723'] is True
run('eventq',612,4,'enter');run('eventq',612,2,'enter');run('fly_to',527);run('eventq',527,87,'enter')
run('eventq',826,8,'talk');run('linear_dialog',826,8,'--source-page',4,'--burst');run('checkpoint','League220-MegaRing')
assert json.loads((R/'notes/League220-MegaRing-status.json').read_text())['bag']['contents'].get('MEGARING',0)==1
