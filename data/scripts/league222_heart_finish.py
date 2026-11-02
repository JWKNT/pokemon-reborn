"""Execute inspected Fiore Heart Scale route and restore cave access moves."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*a):
 print('HEART ERRAND',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True,env=dict(os.environ,REBORN_COORD_CACHE='1'))
run('fiore_route',R/'work/222-heart-plan.json')
run('surface_event',678,8,'item')
run('fiore_route',R/'work/222-heart-return.json')
run('eventq',678,1,'enter');run('eventq',508,2,'enter')
run('fly_to',355,'--carrier','Altaria')
run('circus_relearn_one','Ampharos','Power Gem',14,3)
run('teach_machine','TMX9','Swampert','Rock Climb',3,'--single-step')
run('checkpoint','League222-PowerGem')
