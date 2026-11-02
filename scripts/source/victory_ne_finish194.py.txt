"""Detonate the reviewed NE cart after the plate, then return to Charlotte."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['positions']['786']['100']==[108,27] and s['switches']['1152'] and s['variables']['500']==0
run('overworld.py');run('eventq.py',786,101,'talk');run('play.py','wait:12');run('checkpoint.py','NE194-third-pillar');run('party_open.py')
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['switches']['1135'] and s['variables']['500']==2 and s['variables']['475']==117
run('overworld.py');run('eventq.py',786,7,'enter');run('checkpoint.py','Charlotte194-third-pillar');run('party_open.py')
s=json.loads((R/'notes/Charlotte194-third-pillar-status.json').read_text());assert s['map']==788
print('THIRD PILLAR COMPLETE; HUB RETURN VERIFIED',s['position'],flush=True)
