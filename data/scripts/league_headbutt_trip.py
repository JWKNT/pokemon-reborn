"""Normal return to the source-reviewed Seventh Street Headbutt tutor."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('TUTOR',s,*a,flush=True)
 env=dict(os.environ,REBORN_COORD_CACHE='1');env.pop('REBORN_FAST_KEYS',None)
 if s in ['q','eventq']:env.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='112')
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=env)
run('fly_to',524,'--carrier','Tranquill')
run('eventq',524,30,'enter');run('eventq',168,8,'enter');run('eventq',168,18,'talk')
run('choose_dialog','7th Street|Lapis Ward','7th Street');run('dialog','--limit=5')
run('checkpoint','League-HeadbuttElevator')
run('eventq',168,11,'enter');run('eventq',168,15,'enter');run('eventq',324,83,'talk')
run('choose_dialog','Headbutt|Bounce|Heal Bell|Bug Bite','Headbutt')
run('choose_dialog','Yes|No','Yes')
# Stop at the inspected paid tutor prompt; learning is a separate reviewed phase.
