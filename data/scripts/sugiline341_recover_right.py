"""Reviewed installed cave transfers to Sugiline's eastern statue, normal UI only."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('SUGILINE RIGHT',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
p=R/'work/341-east-waypoint.json';p.write_text('[[651,0,0,42,36,[]]]')
run('queue_route',p)
for m,e,d in [(651,20,656),(656,1,655),(655,17,659),(659,1,654)]:
 run('eventq',m,e,'enter');run('settle_arrival',d)
run('eventq',654,57,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',654,57,'--active','--past-choice');run('checkpoint','Aegir341-RightStatue')
