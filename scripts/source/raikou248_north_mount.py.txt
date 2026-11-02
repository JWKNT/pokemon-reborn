"""Use the north Route1 pair after the isolated southern mount."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('NORTH MOUNT',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('checkpoint','Postgame248-Dismounted')
run('eventq',287,27,'talk')
run('forest_mount245','Postgame248-NorthTauros')
run('connected_walk',287,285,66,9)
run('eventq',285,3,'enter')
run('forest_honey245',289,40,42,'Postgame248-NorthWeb328','Pinsir')
run('q','289,57,10')
run('checkpoint','Postgame248-RaikouGate')
