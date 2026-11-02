"""Prepare Power Gem and find Carbink on the reviewed lower 3F strip."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('FIELD3',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84'))
run('field_medicine','Hyper Potion','Ampharos');run('overworld')
run('q','640,23,28');run('checkpoint','League223-3FReady')
run('hunt_target','Carbink,Aron,Lairon','--dense-horizontal');run('battle_ready')
