"""Reviewed installed cave transfers to Sugiline's western statue, normal UI only."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('SUGILINE GATE',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for m,e,d in [(654,1,659),(659,32,651),(651,5,656),(656,2,654)]:
 run('eventq',m,e,'enter');run('settle_arrival',d)
run('checkpoint','Aegir341-Gate')
