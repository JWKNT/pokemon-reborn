"""Return through the separated cliff passage and start the inspected Meteor pair."""
from play import *
from locate import locate
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
def stage(k,v):
 p=ROOT/'notes/navigation-state.json';d=json.loads(p.read_text());d['variables'][str(k)]=v;p.write_text(json.dumps(d))
if '--from-secret' not in sys.argv:
 run('surface_event.py',439,25,'enter');assert locate()[0]==440
 run('eventq.py',440,1,'enter');assert locate()[0]==374
run('surface_event.py',374,11,'enter');assert locate()[0]==457
run('eventq.py',457,5,'enter');stage(74,1)
run('eventq.py',457,7,'talk');run('choose_dialog.py','Ground Floor|Top Floor','Ground Floor');stage(74,0)
run('eventq.py',457,6,'enter');run('eventq.py',457,1,'enter');assert locate()[0]==439
run('surface_walk.py',439,24,82)
run('trainer_music.py','start','MeteorAceM','Bruno & Ray')
act('up:.12','wait:1');stage(193,21)
run('battle_batch.py','Mienshao',0,'--foes','Arcanine,Raticate','--double','--target',3,'--turns',1,'--watch')
print('FIRST METEOR TURN REVIEW',flush=True)
