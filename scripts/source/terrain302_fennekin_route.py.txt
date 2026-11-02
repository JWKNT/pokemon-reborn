"""Reviewed post-restoration 7th Street route, through normal UI only."""
import os, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
env = dict(os.environ, REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1')
steps = [
    ('city_enter', 38, 519),
    ('fly_to', 524, '--carrier', 'Zapdos'),
    ('city_enter', 524, 168),
    ('city_enter', 168, 324),
    ('city_enter', 324, 327),
    ('city_enter', 327, 478),
    ('eventq', 478, 13, 'enter'),
    ('city_enter', 478, 505),
    ('wtc_room_exit', 505, 504),
    ('wtc_room_exit', 504, 502),
]
start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
assert 0 <= start < len(steps)
for i, (name, *args) in enumerate(steps[start:], start):
    print('TERRAIN ACCESS STAGE', i, name, *args, flush=True)
    subprocess.run([sys.executable, str(R/'scripts'/f'{name}.py'),
                    *map(str, args)], env=env, check=True)
print('PERIDOT GRID ARRIVAL; review upper-plane storage button35', flush=True)
