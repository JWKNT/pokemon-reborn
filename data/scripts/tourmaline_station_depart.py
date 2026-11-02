"""Heal after badge14, then walk the reviewed restored-city transfers to the station."""
from play import *
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
r('overworld.py');r('city_enter.py',613,526);r('city_enter.py',526,100);r('eventq.py',100,4,'talk');r('heal.py');r('party_front.py','Arcanine','Klinklang')
r('city_enter.py',100,526);r('city_enter.py',526,559);r('city_enter.py',559,528);r('city_enter.py',528,520);r('city_enter.py',520,519);r('city_enter.py',519,530);r('city_enter.py',530,591)
r('checkpoint.py','Tourmaline-station-ready')
s=json.loads((ROOT/'notes/Tourmaline-station-ready-status.json').read_text());assert sum(s['trainer']['badges'])==14 and all(m['hp']==m['totalhp'] for m in s['party'])
act('x','wait:.5');print(read(),flush=True)
