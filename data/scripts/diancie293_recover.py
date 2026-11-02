"""Use owned field medicine through normal menus before the Anna-route anomaly."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*args):
 print('DIANCIE RECOVER',s,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],check=True)
for item,name in [('Revive','Volcanion'),('Revive','Cresselia'),('Full Restore','Volcanion'),('Full Restore','Cresselia'),('Full Restore','Mawile'),('Ultra Potion','Magearna')]:
 run('field_medicine',item,name);run('overworld')
run('party_lead','Magearna')
run('checkpoint','Diancie293-Recovered')
v=json.loads((R/'notes/Diancie293-Recovered-status.json').read_text())
assert all(m['hp']==m['totalhp'] for m in v['party'])
run('eventq',860,6,'enter')
run('checkpoint','Diancie293-Chamber')
