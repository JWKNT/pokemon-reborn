"""Normal Bulu portal entry and owned terrain setter preparation."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('BULU GATE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('eventq',809,56,'enter')
run('linear_dialog',855,10,'--source-page',2,'--burst')
run('party_front','Comfey')
run('checkpoint','Bulu305-Gate')
