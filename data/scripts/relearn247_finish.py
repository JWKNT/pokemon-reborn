"""Spend the two earned scales on the reviewed recovery moves."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('RECOVERY BUILD',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
owned=json.loads((R/'notes/Postgame247-FarmEnd17-status.json').read_text())
assert owned['bag']['contents'].get('HEARTSCALE',0)>=2
run('fly_to',521,'--carrier','Zapdos')
run('city_enter',521,116)
run('onyx_relearn_one','Sylveon','Draining Kiss',11,0)
run('onyx_relearn_one','Amoonguss','Synthesis',9,1)
run('checkpoint','Postgame247-RecoveryMoves')
