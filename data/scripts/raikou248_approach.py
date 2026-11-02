"""Enter Raikou's island and checkpoint immediately before the reviewed touch event."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('RAIKOU APPROACH',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('party_lead','Sylveon')
run('eventq',289,91,'enter')
run('q','834,92,31')
run('checkpoint','Postgame248-RaikouReady')
s=json.loads((R/'notes/Postgame248-RaikouReady-status.json').read_text())
assert s['party'][0]['name']=='Sylveon' and all(p['hp']==p['totalhp'] for p in s['party'])
print('RAIKOU READY; battle not triggered',flush=True)
