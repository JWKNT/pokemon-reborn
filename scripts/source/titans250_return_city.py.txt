"""Heal after the Titans and travel to the Nightclub lobby by ordinary controls."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CITY RETURN',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('play','wait:3');run('city_enter',636,360);run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal');run('checkpoint','Postgame250-Healed')
run('eventq',38,6,'enter');run('fly_to',527,'--carrier','Zapdos');run('eventq',527,87,'enter');run('checkpoint','Postgame250-NightclubLobby')
