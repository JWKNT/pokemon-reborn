"""Reviewed installed cave transfers to Sugiline's western statue, normal UI only."""
import os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('AEGIR INTRO',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
p=R/'work/341-florinia-approach.json';p.write_text('[[883,0,0,31,69,[]]]')
run('queue_route',p);run('checkpoint','Aegir342-FloriniaApproach')
run('eventq',883,6,'talk');run('linear_dialog',883,6,'--active','--burst');run('checkpoint','Aegir342-Florinia')
run('eventq',883,9,'enter');run('settle_arrival',850);run('checkpoint','Aegir342-AegirEntrance')
