"""Normal exit from cleared Prisma and reviewed Scrapyard Roost/PP recovery trip."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('eventq',896,128,'enter'),('city_enter',896,185),('city_enter',185,184),('city_enter',184,551),('fly_to',693,'--carrier','Rayquaza')]
plan=json.load(open('work/389-roost-train-plan2.json'))
steps += [('eventq',s['map'],s['event'],'enter') for s in plan['transfers']]
steps += [('ride_train',663,154,370),('eventq',663,16,'item'),('eventq',663,15,'item'),('checkpoint','Scrapyard390-RoostSupplies')]
p=Path('work/390-roost-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
