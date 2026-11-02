"""Normal approach to Umbral Fern; stop at prebattle checkpoint."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('city_enter',38,519),('fly_to',232,'--carrier','Rayquaza')]
steps += [('city_enter',a,b) for a,b in [(232,231),(231,244),(244,261),(261,247),(247,259),(259,511)]]
steps += [('q','511,36,55,left:.12,wait:2'),('eventq',511,45,'enter'),('eventq',511,42,'enter'),('eventq',511,103,'enter'),('eventq',895,106,'enter'),('q','895,54,24'),('checkpoint','Fern390-Ready')]
p=Path('work/390-fern-route-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
