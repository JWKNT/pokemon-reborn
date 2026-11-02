"""Execute the previously solved, fresh-save verified three-boulder ridge route."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('RIDGE',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('dialog','--limit=8');run('overworld')
for i in range(3):run('teknite643_push',i,'--label-prefix','Cauldron340-RidgePush')
run('cauldron340_caves','--from',4)
