"""Only after Fern224 victory and verified return to outdoors527; reach Noel, heal and collect supplies."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('fly_to', 525, '--carrier', 'Rayquaza'), ('connected_walk', 525, 551, 15, 12), ('connected_walk', 551, 552, 20, 8), ('connected_walk', 552, 544), ('eventq', 544, 12, 'enter'), ('eventq', 150, 314, 'enter'), ('eventq', 886, 10, 'enter'), ('eventq', 889, 5, 'talk'), ('linear_dialog', 889, 5, '--source-page', 8, '--burst'), ('checkpoint', 'Tree391-DoorOpen'), ('eventq', 889, 45, 'talk'), ('linear_dialog', 889, 45, '--source-page', 1, '--burst'), ('checkpoint', 'Tree391-FernSupplies')]
p=Path('work/391-noel-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
