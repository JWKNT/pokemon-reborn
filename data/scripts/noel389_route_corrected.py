"""Advance Heather's inspected scene and normal fast route to Noel."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('city_enter',826,527),('fly_to',525,'--carrier','Rayquaza'),('connected_walk',525,551,15,12),('connected_walk',551,552,20,8),('connected_walk',552,544),('eventq',544,12,'enter'),('eventq',150,314,'enter'),('eventq',886,10,'enter'),('eventq',889,5,'talk'),('linear_dialog',889,5,'--source-page',7,'--burst'),('checkpoint','Tree389-NoelRequest')]
p=Path('work/389-noel-corrected-queue.json');assert not p.exists();j=dict(done=0,steps=steps)
for i,cmd in enumerate(steps):
 j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
