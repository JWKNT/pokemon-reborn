"""Return through cleared tree and Beryl cave to the cleared Citae Prisma."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('eventq',889,31,'enter'),('city_enter',150,544),('connected_walk',544,552),('connected_walk',552,551,5,7),('eventq',551,16,'smash'),('eventq',551,15,'enter'),('eventq',184,2,'enter'),('eventq',185,12,'enter'),('eventq',896,124,'enter'),('eventq',896,166,'talk')]
p=Path('work/389-meteor-queue.json');assert not p.exists();j=dict(done=0,steps=steps)
for i,cmd in enumerate(steps):
 j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
print('STOP: review Giratina selection prompt.',flush=True)
