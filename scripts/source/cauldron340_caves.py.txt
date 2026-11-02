"""Follow the read-only validated Teknite room route with ordinary guarded movement."""
import os,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TEKNITE',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
start=int(sys.argv[sys.argv.index('--from')+1]) if '--from' in sys.argv else 0
for step in json.loads((R/'work/340-teknite-plan.json').read_text())['transfers'][start:]:
 run('eventq',step['map'],step['event'],'enter');run('settle_arrival',step['arrival'][0])
run('eventq',646,22,'talk');run('finish_rock_climb',646,19,23);run('checkpoint','Cauldron340-RidgeClimb')
