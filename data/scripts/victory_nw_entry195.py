"""Normal northwest hub cart and Strength activation, with entry guards."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
run('overworld.py');run('eventq.py',788,52,'talk');run('play.py','wait:10');run('checkpoint.py','NW195-entry');run('party_open.py')
s=json.loads((R/'notes/NW195-entry-status.json').read_text());n=json.loads((R/'notes/navigation-state.json').read_text())
assert s['map']==784 and s['position']==[85,22],s['position']
assert not n['switches']['1119']
assert n['positions']['784']['77']==[81,24]
assert n['positions']['784']['76']==[79,34]
run('party_pick.py','Mienshao','--single');run('play.py','down','c','wait:2');run('dialog.py','--limit=6');run('party_open.py')
print('NW MAIN ENTRY VERIFIED; STRENGTH USED',flush=True)
