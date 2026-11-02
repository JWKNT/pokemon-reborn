"""Run a reviewed weather-puzzle route, using existing guarded UI helpers."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
start=tuple(map(int,sys.argv[1:4]));orb=int(sys.argv[4]);lookup={17:(837,25,58),131:(837,39,61),132:(837,57,58)}
v=json.loads((R/'work/252-weather-route-proposals.json').read_text());p=next(x for x in v if tuple(x['start'])==start and tuple(x['goal'])==lookup[orb])
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for step in p['solution'][1]:
 if 'event' in step:run('eventq',step['map'],step['event'],'enter')
 else:run('eventq',837,orb,'talk')
run('checkpoint',f'Postgame253-WeatherOrb{orb}')
print('ORB ROUTE COMPLETE',orb,flush=True)
