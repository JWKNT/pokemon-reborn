"""Reviewed post-paired-fight route to Devon's PC; ordinary UI inputs only."""
from play import ROOT,read,act
from locate import locate
import subprocess,sys,json

def run(s,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
def observed_state(phase,**switches):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['339']=phase
 v.setdefault('switches',{}).update(switches);p.write_text(json.dumps(v))
if '--from-paired-checkpoint' not in sys.argv:
 run('victory_outro.py')
 run('linear_dialog.py',624,71,'--active','--past-battle','--burst')
 run('trainer_music.py','finish','--world-verified')
 observed_state(16)
else:
 assert not (ROOT/'work/active-trainer-music.json').exists()
 assert json.loads((ROOT/'notes/navigation-state.json').read_text())['variables']['339']==16
run('eventq.py',624,2,'enter')
# Phase16 starts this scene automatically on entering the fourth floor.
run('linear_dialog.py',625,3,'--burst')
assert locate(626)[0]==626,'Devon collapse transfer review'
observed_state(25) # The inspected floor626 radio conversation also completes.
run('devon_walk.py',626,2,4,'--go')
run('eventq.py',626,3,'enter')
run('q.py','627,5,8')
act('right:.12','wait:3');print(read(),flush=True)
assert locate(628)==(628,30,8),'Devon trap transfer review'
observed_state(28,**{'777':False})
run('checkpoint.py','Devon-PC-before-Victoria')
print('DEVON PC CHECKPOINT VERIFIED',flush=True)
