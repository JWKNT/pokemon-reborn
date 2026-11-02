"""Accept the two inspected Tier3 missions through normal dialogue."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('ACCEPT',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for e,name in [(82,'Weather'),(84,'Swords')]:
 run('eventq',827,e,'talk')
 run('choose_dialog','Yes|No','Yes','--source',827,e)
 run('linear_dialog',827,e,'--active','--after-last-choice','--past-choice')
 run('checkpoint','Postgame251-'+name+'Accepted')
