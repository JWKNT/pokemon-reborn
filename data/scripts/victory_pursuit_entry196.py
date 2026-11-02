"""Return from Charlotte to the normally collapsed main Victory Road room."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):subprocess.run([sys.executable,str(R/'scripts'/n),*map(str,a)],check=True,env=env)
s=json.loads((R/'notes/Charlotte195-pursuit-ready-status.json').read_text());n=json.loads((R/'notes/navigation-state.json').read_text());assert s['map']==788 and n['variables']['475']==119 and n['switches']['1154']
run('overworld.py');run('eventq.py',788,1,'enter');run('eventq.py',811,5,'enter');run('checkpoint.py','Pursuit196-main-entry');run('party_open.py')
s=json.loads((R/'notes/Pursuit196-main-entry-status.json').read_text());assert s['map']==812
print('COLLAPSED MAIN ENTRY VERIFIED',s['position'],flush=True)
