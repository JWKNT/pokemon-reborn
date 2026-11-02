"""Reviewed third/fourth room route and guarded source-solved pushes."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('TOWER',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
run('city_enter',709,671)
run('mirage_execute_solved',2)
run('city_enter',708,672)
run('mirage_execute_solved',3)
