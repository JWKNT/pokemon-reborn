"""Collect installed TM16 via reviewed Surf/Dive routes, normal controls only."""
from play import *
def run(s,*a):
 print('LIGHT SCREEN',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((ROOT/'notes/Aegir369-RayTrained-status.json').read_text())
assert s['map']==232 and next(p for p in s['party']if p['name']=='Rayquaza')['ev'][:2]==[252,252]
run('teach_machine','HM03','Rayquaza','Surf',2)
run('teach_machine','HM06','Rayquaza','Dive',0)
run('fly_to',522,'--carrier','Zapdos')
run('eventq',522,1,'enter')
run('field_repel','Super Repel')
run('surface_event',538,12,'enter')
run('lake_route_follow',ROOT/'work/aegir369-light-screen-out-route.json')
run('eventq',553,14,'item')
run('q','553,41,45')
run('lake_route_follow',ROOT/'work/aegir369-light-screen-return-route.json')
run('surface_event',567,28,'enter')
run('surface_event',538,18,'enter')
run('teach_machine','TM16','Cresselia','Light Screen',0)
run('checkpoint','Aegir369-LightScreen')
