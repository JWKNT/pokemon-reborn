"""Clear the observed blocking rocks, then resume the reviewed meteor route."""
import subprocess,sys,json,time
from pathlib import Path
old=json.load(open('work/389-meteor-corrected-queue.json'));assert old['done']==4
steps=[('eventq',552,29,'smash'),('eventq',552,30,'smash')]+old['steps'][4:]
p=Path('work/389-meteor-cave-queue.json');j=json.loads(p.read_text()) if p.exists() else dict(done=0,steps=steps);assert not j.get('pending')
for i in range(j['done'],len(steps)):
 cmd=steps[i]
 j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
