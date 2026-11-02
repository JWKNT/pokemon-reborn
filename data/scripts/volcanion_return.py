"""Return through the reviewed spring route; verify boulders from fresh normal saves."""
import subprocess,sys,json,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
label=sys.argv[1]
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('VOLCANION RETURN',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
run('city_enter',38,519);run('fly_to',271,'--carrier','Zapdos')
run('eventq',271,12,'enter');run('eventq',234,256,'enter')
run('checkpoint',label+'-Entry')
run('surface_walk',238,33,39)
nav=json.loads((R/'notes/navigation-state.json').read_text());p=nav['positions']['238']
if p.get('14',[33,38])==[33,38]:
 run('play','up:.03','c','wait:.7');run('dialog','--yes','--limit=12')
 run('springs_boulder_push',14,label+'-Boulder14')
else:assert p['14']==[33,36],p['14']
run('q','238,35,26')
nav=json.loads((R/'notes/navigation-state.json').read_text());p=nav['positions']['238']
if p.get('6',[35,25])==[35,25]:
 run('play','up:.03','c','wait:.7');run('dialog','--yes','--limit=12')
 run('springs_boulder_push',6,label+'-Boulder6')
else:assert p['6']==[35,24],p['6']
run('eventq',238,7,'enter');run('q','545,30,19');run('checkpoint',label+'-BeforeVolcanion')
