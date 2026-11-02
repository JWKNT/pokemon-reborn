"""Heal an escape-capable lead and activate Strength before the NE loop."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
s=json.loads((R/'notes/NE194-basement-entry-retry-status.json').read_text());n=json.loads((R/'notes/navigation-state.json').read_text())
assert s['map']==786 and s['position']==[104,15]
assert n['positions']['786']['100']==[108,17] and n['variables']['500']==0
run('overworld.py');run('field_medicine.py','Max Potion','Mienshao');run('overworld.py');run('party_front.py','Mienshao');run('party_open.py');run('party_pick.py','Mienshao','--single');run('play.py','down','c','wait:2');run('dialog.py','--limit=6');run('checkpoint.py','NE194-basement-ready');run('party_open.py')
s=json.loads((R/'notes/NE194-basement-ready-status.json').read_text());assert s['map']==786
print('BASEMENT PREPARATION SAVED; inspect full-health lead before loop',flush=True)
