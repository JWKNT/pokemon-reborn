"""Enter2F and find a reviewed safe Power Gem carrier encounter through normal UI."""
import subprocess,os,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('TEKNITE FIRST',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=dict(os.environ,REBORN_COORD_CACHE='1',REBORN_REPEL_POLICY='cancel',REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84'))
run('party_front','Hexan')
run('eventq',638,2,'enter');run('settle_arrival',639)
run('q','639,17,18');run('checkpoint','League223-Teknite2F')
run('hunt_target','Carbink','--dense-horizontal','--expire-repel')
run('battle_ready')
# Stop at public command for move/health verification before changing the field.
