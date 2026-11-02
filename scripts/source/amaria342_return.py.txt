"""Return through previously reviewed Sugiline transfers; stop on any battle interruption."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('AMARIA RETURN',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('settle_arrival',704)
run('city_enter',704,651)
for m,e,d in [(651,5,656),(656,2,654),(654,4,660)]:
 run('eventq',m,e,'enter');run('settle_arrival',d)
run('checkpoint','Amaria342-RuinReturn')
