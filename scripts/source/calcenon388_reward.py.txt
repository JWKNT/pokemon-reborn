"""Normal Calcenon healing and source-reviewed Eclipse family reunion."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('eventq',413,68,'enter'),('eventq',415,4,'talk'),('heal',),('overworld',),('checkpoint','Calcenon388-Healed'),('eventq',415,8,'enter'),('eventq',413,71,'enter'),('linear_dialog',417,56,'--source-page',0,'--follow-source',413,1,'--follow-source-page',0,'--burst'),('checkpoint','Calcenon388-Mewtwonites')]
p=Path('work/calcenon388-reward-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2));print('REWARD',i,steps[i],flush=True)
 subprocess.run([sys.executable,'scripts/'+steps[i][0]+'.py',*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
