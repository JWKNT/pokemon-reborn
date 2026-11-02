"""Normal EV training, Roost teaching, Silva rewards and Mew's cap150 finish."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('mew390_ev','hp'),('mew390_ev','speed'),('take_held','Mew','Power Anklet'),('fly_to',519,'--carrier','Rayquaza'),('eventq',519,116,'enter'),('eventq',38,3,'talk'),('heal',),('teach_machine','TM19','Mew','Roost',0),('checkpoint','Mew390-Trained')]
steps += [('silva367_round','Postgame390-Silva'+str(i)) for i in range(1,4)]
steps += [('candy_target_one','Postgame390-Silva3','Mew',150),('eventq',38,3,'talk'),('heal',),('party_front','Mew'),('checkpoint','Mew390-Ready')]
p=Path('work/390-mew-training-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
