"""Verified normal route from Nightclub to the Lele terrain gate."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('LELE ROUTE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('city_enter',827,826);run('city_enter',826,527)
run('fly_to',814,'--carrier','Zapdos')
run('eventq',814,16,'enter')
run('city_enter',798,796);run('city_enter',796,791);run('city_enter',791,810)
run('eventq',810,27,'enter')
run('linear_dialog',855,10,'--source-page',1,'--burst')
run('party_front','Fennekin')
run('checkpoint','Lele303-Gate')
