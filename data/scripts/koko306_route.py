"""Replenish Timer Balls and travel to the installed Electric Terrain gate."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='112')
def run(n,*a):
 print('KOKO ROUTE',n,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('fly_to',520,'--carrier','Zapdos')
run('eventq',520,67,'enter');run('eventq',369,1,'talk');run('mart_open')
run('shop_buy','Timer Ball',20,1000);run('mart_exit');run('city_enter',369,520)
run('fly_to',814,'--carrier','Zapdos');run('eventq',814,16,'enter')
run('city_enter',798,796);run('city_enter',796,791);run('eventq',791,55,'enter')
run('eventq',807,9,'talk');run('overworld');run('eventq',807,16,'enter');run('linear_dialog',855,10,'--source-page',0,'--burst')
run('party_front','Zeraora');run('checkpoint','Koko306-Gate')
