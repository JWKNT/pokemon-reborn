"""Collect inspected Grand Hall basement resources through normal UI."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*a):
 print('BASEMENT PREP',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Postgame288-MagearnaEV-status.json').read_text())
m=next(m for m in s['party'] if m['species']=='MAGEARNA');assert m['ev']==[252,0,0,252,0,0]
if '--employee-ready' not in sys.argv:
 run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal')
 run('eventq',38,18,'talk');run('linear_dialog',38,18,'--active','--burst');run('checkpoint','Postgame288-EmployeeAccess')
run('eventq',38,63,'enter');run('eventq',764,59,'enter')
run('eventq',764,153,'item');run('eventq',764,151,'item');run('eventq',764,152,'item')
run('checkpoint','Postgame288-BasementItems')
s=json.loads((R/'notes/Postgame288-BasementItems-status.json').read_text());assert s['bag']['contents']['MODESTMINT']>=1
run('field_medicine','Modest Mint','Magearna');run('overworld')
run('eventq',764,68,'enter');run('eventq',764,48,'enter')
run('checkpoint','Postgame288-MagearnaModest')
s=json.loads((R/'notes/Postgame288-MagearnaModest-status.json').read_text());m=next(m for m in s['party'] if m['species']=='MAGEARNA');assert m['nature']=='MODEST';print('MAGEARNA MODEST VERIFIED',m['nature'],m['ev'],flush=True)
