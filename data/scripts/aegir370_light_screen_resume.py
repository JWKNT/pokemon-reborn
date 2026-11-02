"""Collect installed TM16 via reviewed Surf/Dive routes, normal controls only."""
from play import *
def run(s,*a):
 print('LIGHT SCREEN',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('fly_to',530,'--carrier','Zapdos')
run('field_repel','Super Repel')
run('surface_event',530,114,'enter')
run('lake_route_follow',ROOT/'work/aegir370-light-screen-out-route.json')
run('eventq',553,14,'item')
run('q','553,41,45')
run('lake_route_follow',ROOT/'work/aegir370-light-screen-return-route.json')
run('surface_event',567,21,'enter')
run('teach_machine','TM16','Cresselia','Light Screen',0)
run('checkpoint','Aegir369-LightScreen')
