"""Reviewed Ray/Espeon room and Sanchez supplies, through normal controls."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def mirror(**a):
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text())
 for k,v in a.items():
  d,key=k.split(':',1);s.setdefault(d,{})[key]=v
 p.write_text(json.dumps(s))
run('party_front','Mienshao')
run('eventq',732,55,'smash');run('eventq',732,55,'enter')
run('trainer_enter',737,21,'MeteorAceM','Ray')
run('trainer_plan',ROOT/'work/glass-ray-plan.json',ROOT/'work/glass-ray-live.log','--stop-after-battle')
run('linear_dialog',737,21,'--source-page',0,'--past-battle','--after-last-battle')
run('trainer_music','finish','--world-verified');mirror(**{'self_switches:737,21,A':True})
run('eventq',737,13,'talk');run('linear_dialog',737,13,'--active');mirror(**{'switches:949':True})
run('eventq',737,20,'talk');run('linear_dialog',737,20,'--source-page',0,'--burst','--world-settle',15)
mirror(**{'self_switches:737,20,A':True})
run('eventq',737,11,'enter');run('party_front','Arcanine')
run('eventq',732,54,'smash');run('eventq',732,54,'enter')
run('trainer_enter',737,66,'MeteorAceM','Sanchez')
run('trainer_plan',ROOT/'work/glass-sanchez-plan.json',ROOT/'work/glass-sanchez-live.log','--stop-after-battle')
run('linear_dialog',737,66,'--source-page',0,'--past-battle','--after-last-battle')
run('trainer_music','finish','--world-verified');mirror(**{'self_switches:737,66,A':True})
for e in[22,67,68]:run('eventq',737,e,'item')
run('checkpoint','Glass-Ray-Sanchez-supplies')
print('RAY/SANCHEZ COMPLETE; CAGE KEY NEXT',flush=True)
