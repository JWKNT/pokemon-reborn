"""Normal travel and checkpoint before reviewed Friday training."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('checkpoint','Postgame259-CastleQuest')
run('city_enter',827,826);run('city_enter',826,527)
run('fly_to',519,'--carrier','Zapdos');run('eventq',519,116,'enter')
run('checkpoint','Postgame259-GrandHall')
