"""Reviewed first Glass server room: Geoff, then Glaceon follows normally."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',732,52,'enter')
run('trainer_enter',737,4,'MeteorAceM','Geoff')
run('trainer_plan',ROOT/'work/glass-geoff-plan.json',ROOT/'work/glass-geoff-live.log','--stop-after-battle')
run('linear_dialog',737,4,'--source-page',0,'--past-battle','--after-last-battle','--burst','--world-settle',15)
run('trainer_music','finish','--world-verified')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['391']=20;v['switches']['946']=True;p.write_text(json.dumps(v))
run('checkpoint','Glass-Geoff-and-Glaceon')
print('GEOFF ROOM COMPLETE; OBSERVE GLACEON PET PROMPT NEXT',flush=True)
