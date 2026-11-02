"""Return from the second demolished pillar by the normal Rock Climb exit."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],env=env,check=True)
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['switches']['1133']
run('overworld.py');run('eventq.py',786,68,'talk');run('dialog.py','--yes','--limit=10');run('checkpoint.py','SW193-exit-climbed')
s=json.loads((R/'notes/SW193-exit-climbed-status.json').read_text());assert s['map']==786 and s['position']==[77,48],s['position']
run('eventq.py',786,7,'enter');run('checkpoint.py','Charlotte193-second-pillar');run('party_open.py')
s=json.loads((R/'notes/Charlotte193-second-pillar-status.json').read_text());assert s['map']==788
print('SECOND PILLAR COMPLETE; HUB RETURN VERIFIED',s['position'],flush=True)
