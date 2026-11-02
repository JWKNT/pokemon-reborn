"""Reviewed installed cave transfers to Sugiline's western statue, normal UI only."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('SUGILINE LEFT',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for m,e,d in [(651,16,657),(657,4,652),(652,6,657),(657,1,653),(653,24,658),(658,1,653),(653,47,654)]:
 run('eventq',m,e,'enter');run('settle_arrival',d)
run('eventq',654,56,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',654,56,'--active','--past-choice');run('checkpoint','Aegir341-LeftStatue')
