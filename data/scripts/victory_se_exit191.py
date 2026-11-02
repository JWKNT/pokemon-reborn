"""Normal route from completed SE pillar back to Charlotte's hub."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],env=env,check=True)
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['switches']['1132'] and not s['switches']['1127']
run('overworld.py');run('eventq.py',786,48,'talk');run('checkpoint.py','SE191-exit-lever')
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['switches']['1127']
run('victory_boulder_push.py',786,116,'up',1);run('checkpoint.py','SE191-exit-boulder')
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['positions']['786']['116']==[121,45]
run('eventq.py',786,66,'talk');run('dialog.py','--yes','--limit=10');run('checkpoint.py','SE191-exit-climbed')
s=json.loads((R/'notes/SE191-exit-climbed-status.json').read_text());assert s['map']==786 and s['position']==[124,46],s['position']
run('eventq.py',786,7,'enter');run('checkpoint.py','Charlotte191-first-pillar');run('party_open.py')
s=json.loads((R/'notes/Charlotte191-first-pillar-status.json').read_text());assert s['map']==788
print('FIRST PILLAR COMPLETE; HUB RETURN VERIFIED',s['position'],flush=True)
