"""Return from completed Anna/Taka scene to the next tier's lobby boundary."""
import os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1', REBORN_ROUTE_STEP_PAUSE='.10', REBORN_ROUTE_CHUNK='56')
def run(name, *args):
    print('GIRATINA RETURN', name, *args, flush=True)
    subprocess.run([sys.executable, str(ROOT/'scripts'/f'{name}.py'), *map(str,args)], check=True)
run('checkpoint', 'Giratina361-Complete')
for mid, event in [(222,1),(219,1),(216,1)]:
    run('eventq', mid, event, 'enter')
run('fly_to', 527, '--carrier', 'Zapdos')
run('eventq', 527, 87, 'enter')
run('checkpoint', 'Giratina361-NightclubLobby')
