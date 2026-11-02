"""Normal owned-candy training of final team; fresh checkpoint after each target."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('candy_target_one', 'Tree391-FernSupplies', 'Cresselia', 150), ('checkpoint', 'Final392-Cresselia'), ('candy_target_one', 'Final392-Cresselia', 'Mewtwo', 150), ('checkpoint', 'Final392-Mewtwo'), ('candy_target_one', 'Final392-Mewtwo', 'Latias', 150), ('checkpoint', 'Final392-Latias'), ('candy_target_one', 'Final392-Latias', 'Rayquaza', 150), ('checkpoint', 'Final392-Rayquaza'), ('candy_target_one', 'Final392-Rayquaza', 'Kyogre', 150), ('checkpoint', 'Final392-Kyogre'), ('eventq', 889, 45, 'talk'), ('linear_dialog', 889, 45, '--source-page', 1, '--burst'), ('checkpoint', 'Final392-Level150')]
p=Path('work/392-cap-training-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
