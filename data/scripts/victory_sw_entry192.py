import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
run('overworld.py');run('eventq.py',788,56,'talk');run('play.py','wait:10');run('checkpoint.py','SW192-entry');run('party_open.py')
s=json.loads((R/'notes/SW192-entry-status.json').read_text());assert s['map']==784 and s['position']==[67,47],s['position'];print('SW MAIN ENTRY VERIFIED',flush=True)
