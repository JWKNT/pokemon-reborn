"""Normal northwest descent and healthy escape lead; verify then begin rail."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
n=json.loads((R/'notes/navigation-state.json').read_text());assert n['switches']['1119']
run('hazard_retry.py','victory_hazard_interact_fast.py',126,'NW195-basement-entry')
s=json.loads((R/'notes/NW195-basement-entry-status.json').read_text());assert s['map']==786 and s['position']==[69,21]
run('overworld.py');run('field_medicine.py','Max Potion','Mienshao');run('overworld.py');run('checkpoint.py','NW195-basement-ready');run('party_open.py')
print('NW BASEMENT READY; NORMAL SAVE VERIFIED',flush=True)
