"""Normal northeast hub cart and Strength activation, with entry guards."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112',REBORN_COORD_CACHE='1')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/name),*map(str,args)],check=True,env=env)
run('overworld.py');run('eventq.py',788,55,'talk');run('play.py','wait:10');run('checkpoint.py','NE194-entry');run('party_open.py')
s=json.loads((R/'notes/NE194-entry-status.json').read_text());n=json.loads((R/'notes/navigation-state.json').read_text())
assert s['map']==784 and s['position']==[114,32],s['position']
for var in ['493','494','495']:assert n['variables'][var]==0
for switch in ['1123','1124','1125','1126']:assert not n['switches'][switch]
assert n['positions']['784']['135']==[103,23]
run('party_pick.py','Mienshao','--single');run('play.py','down','c','wait:2');run('dialog.py','--limit=6');run('party_open.py')
print('NE MAIN ENTRY VERIFIED; STRENGTH USED',flush=True)
