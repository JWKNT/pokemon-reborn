"""Restore the trained boss team, heal normally and save its verified build."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TEAM READY',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
run('city_enter',116,521)
run('fly_to',519,'--carrier','Zapdos')
run('city_enter',519,38)
run('q','38,9,20,up:.12,c,wait:1')
run('pc_open_reviewed')
run('pc_exchange_named',23,0,'Aegislash','Arcanine')
run('party_lead','Sylveon')
run('q','38,5,22,up:.12')
run('heal')
run('checkpoint','Postgame247-TeamReady')
j=json.loads((R/'notes/Postgame247-TeamReady-status.json').read_text())
assert all(p['level']==110 and p['hp']==p['totalhp'] and p['status'] is None for p in j['party'])
assert [m['move']for m in j['party'][0]['moves']]==['DRAININGKISS','MISTYTERRAIN','CALMMIND','MOONBLAST']
print('ALL SIX FULLY TRAINED AND HEALED',flush=True)
