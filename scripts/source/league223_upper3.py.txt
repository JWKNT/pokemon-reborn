"""Reach upper3F and prepare its final crystal trigger through normal controls."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('UPPER3',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84'))
run('field_medicine','Full Restore','Ampharos');run('overworld')
run('teknite_point','640,24,11');run('checkpoint','League223-Upper3FReady')
# Reviewed row11 bounded23..26, no transfer/event tiles.
run('hunt_target','Carbink,Aron,Lairon','--dense-horizontal');run('battle_ready')
