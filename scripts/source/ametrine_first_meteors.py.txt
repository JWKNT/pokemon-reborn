"""Collect the shack reward and begin the inspected first Meteor pair."""
from play import *
from locate import locate
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],check=True)
assert locate()[0]==439
run('checkpoint.py','Heather-rescued')
run('eventq.py',439,71,'enter')
assert locate()[0]==462
run('eventq.py',462,4,'talk')
run('choose_dialog.py','Yes|No','Yes')
run('linear_dialog.py',462,4,'--active','--past-choice')
run('eventq.py',462,1,'enter')
assert locate()[0]==439
run('party_lead.py',5) # Mienshao; full party observed in Heather checkpoint.
run('q.py','439,24,82')
run('trainer_music.py','start','MeteorAceM','Bruno & Ray')
act('up:.12','wait:1')
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['193']=21;p.write_text(json.dumps(s))
run('battle_batch.py','Mienshao',0,'--foes','Arcanine,Raticate','--double','--target',3,'--turns',1,'--watch')
print('FIRST METEOR TURN REVIEW',flush=True)
