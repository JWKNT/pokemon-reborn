"""Normal-control final preparation; resumed steps guarded against uncertain input."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('eventq', 898, 250, 'enter'), ('choose_dialog', 'Yes|No', 'Yes'), ('overworld',), ('eventq', 889, 4, 'enter'), ('eventq', 886, 2, 'enter'), ('city_enter', 150, 544), ('fly_to', 520, '--carrier', 'Rayquaza'), ('eventq', 520, 101, 'enter'), ('eventq', 112, 6, 'enter'), ('eventq', 113, 1, 'talk'), ('dept_greet',), ('dept_floor', 8), ('eventq', 4, 4, 'talk'), ('mart_open',), ('shop_buy', 'X Speed', 6, 350), ('mart_exit',), ('eventq', 4, 6, 'enter'), ('eventq', 113, 1, 'talk'), ('dept_greet',), ('dept_floor', 1), ('eventq', 112, 1, 'enter'), ('fly_to', 519, '--carrier', 'Rayquaza'), ('eventq', 519, 116, 'enter'), ('eventq', 38, 5, 'talk'), ('mart_open',), ('shop_buy', 'Max Potion', 10, 2500), ('mart_exit',), ('eventq', 38, 3, 'talk'), ('heal',), ('party_front', 'Mewtwo'), ('checkpoint', 'Final392-Supplies'), ('city_enter', 38, 519), ('fly_to', 525, '--carrier', 'Rayquaza'), ('connected_walk', 525, 551, 15, 12), ('connected_walk', 551, 552, 20, 8), ('connected_walk', 552, 544), ('eventq', 544, 12, 'enter'), ('eventq', 150, 314, 'enter'), ('eventq', 886, 10, 'enter'), ('eventq', 889, 46, 'enter'), ('checkpoint', 'Final392-AsylumReturn')]
p=Path('work/392-final-resupply-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
