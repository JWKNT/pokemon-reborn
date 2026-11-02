"""Reviewed normal doors from Belrose upstairs PC to Neoteric entrance; stop on interruption."""
from play import *
from locate import locate
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
assert locate(233)[0]==233
run('eventq',233,13,'enter')
for source,destination in [(233,232),(232,231),(231,244),(244,261),(261,247),(247,259),(259,511)]:
 run('city_enter',source,destination)
print('NEOTERIC ISLE ARRIVAL; REVIEW OUTDOOR PATH BEFORE CLONE',flush=True)
run('checkpoint','Neoteric377-Isle-entry')
