"""Collect the restored-city Old Rod through reviewed normal entrances."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('OLD ROD',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
run('eventq',666,7,'enter')
run('settle_arrival',693)
run('fly_to',519,'--carrier','Zapdos')
run('city_enter',519,602)
run('eventq',602,24,'item')
run('checkpoint','Postgame247-OldRod')
