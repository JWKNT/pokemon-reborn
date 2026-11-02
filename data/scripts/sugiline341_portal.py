"""Reviewed installed cave transfers to Sugiline's western statue, normal UI only."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('SUGILINE PORTAL',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for m,e,d in [(654,4,660),(660,2,661),(661,57,883)]:
 run('eventq',m,e,'enter');run('settle_arrival',d)
run('checkpoint','Aegir341-NewWorld')
