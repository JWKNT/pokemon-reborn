"""Exit the fourth pillar via normal cliffs and speak to Charlotte."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):subprocess.run([sys.executable,str(R/'scripts'/n),*map(str,a)],check=True,env=env)
n=json.loads((R/'notes/navigation-state.json').read_text());assert all(n['switches'][str(i)]for i in [1132,1133,1134,1135])
assert n['switches']['1154'] and n['variables']['475']==119
run('overworld.py');run('victory_nw_cliff_event.py',811,7,'enter');run('checkpoint.py','Charlotte195-four-pillars');run('party_open.py')
s=json.loads((R/'notes/Charlotte195-four-pillars-status.json').read_text());assert s['map']==788
run('overworld.py');run('eventq.py',788,51,'talk');run('dialog.py','--limit=15');run('checkpoint.py','Charlotte195-pursuit-ready');run('party_open.py')
print('FOUR PILLARS COMPLETE; CHARLOTTE SPOKEN',flush=True)
