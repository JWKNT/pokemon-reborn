"""Normal shop and PC preparation for the final fixed-team challenge."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('fly_to',527,'--carrier','Rayquaza'),('city_enter',527,826),('city_enter',826,827),('eventq',827,93,'talk'),('bp_store_buy',8,1,'Timid Mint'),('bp_store_exit',),('overworld',),('eventq',827,100,'talk'),('bp_store_buy',3,2,'Heart Scale'),('bp_store_exit',),('overworld',),('eventq',827,3,'talk'),('pc_open_reviewed',),('pc_select_box',3),('pc_exchange_named',18,3,'Mew','Giratina','--box',3,'--stay-open'),('pc_select_box',2),('pc_exchange_named',13,5,'Zapdos','Magearna','--box',2),('field_medicine','Timid Mint','Mew'),('overworld',),('checkpoint','Mew390-Roster'),('city_enter',827,826),('city_enter',826,527),('fly_to',521,'--carrier','Rayquaza'),('city_enter',521,116),('onyx_relearn_one','Mew','Barrier',6,3),('onyx_relearn_one','Mew','Amnesia',7,1),('teach_machine','TM35','Mewtwo','Flamethrower',2),('checkpoint','Mew390-Moves'),('city_enter',116,521),('fly_to',519,'--carrier','Rayquaza'),('eventq',519,116,'enter'),('eventq',38,3,'talk'),('heal',),('checkpoint','Mew390-EVReady')]
p=Path('work/390-mew-prep-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
