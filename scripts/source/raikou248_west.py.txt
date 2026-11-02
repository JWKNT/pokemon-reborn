"""Finish the two reviewed north-woods openings with normal controls."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('NORTH ROUTE',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
assert json.loads((R/'notes/navigation-state.json').read_text())['switches'].get('339')
run('city_enter',289,287,'--arrival',69,13)
run('eventq',287,25,'talk')
run('forest_mount245','Postgame248-Tauros')
run('connected_walk',287,285,66,9)
run('eventq',285,3,'enter')
run('forest_honey245',289,40,42,'Postgame248-NorthWeb328','Pinsir')
run('q','289,57,10')
run('checkpoint','Postgame248-RaikouGate')
