"""Reviewed ladder/outer route to Devin and the Cage Key."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',737,10,'enter');run('party_front','Arcanine')
run('layer_walk',732,35,19,0,0)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['switches']['946']=False;s['switches']['947']=False;p.write_text(json.dumps(s))
run('layer_walk',732,8,48,0,1,'--hold-straights');run('eventq',732,58,'enter')
run('trainer_enter',738,13,'MeteorAceM','Devin')
run('trainer_plan',ROOT/'work/glass-devin-plan.json',ROOT/'work/glass-devin-live.log','--stop-after-battle')
run('linear_dialog',738,13,'--source-page',0,'--past-battle','--after-last-battle')
run('trainer_music','finish','--world-verified')
s=json.loads(p.read_text());s.setdefault('self_switches',{})['738,13,A']=True;p.write_text(json.dumps(s))
run('eventq',738,10,'item');run('checkpoint','Glass-Cage-Key')
print('CAGE KEY OBTAINED; REJOIN GLACEON AND FREE ESPEON',flush=True)
