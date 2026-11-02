"""Normal final support swap and Light Clay transfer after Mew training."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('eventq',38,4,'talk'),('pc_open_reviewed',),('pc_select_box',4),('pc_exchange_named',3,5,'Cresselia','Zapdos','--box',4,'--stay-open'),('pc_select_box',3),('pc_take_owned_item',2,'Meowstic','Light Clay','--box',3),('give_held','Light Clay','Cresselia'),('checkpoint','Final390-Support'),('city_enter',38,519),('fly_to',521,'--carrier','Rayquaza'),('city_enter',521,116),('onyx_relearn_one','Cresselia','Lunar Dance',0,0),('checkpoint','Final390-Moves'),('city_enter',116,521),('fly_to',519,'--carrier','Rayquaza'),('eventq',519,116,'enter'),('eventq',38,3,'talk'),('heal',),('party_front','Cresselia','Mew'),('checkpoint','Final390-FernTeam')]
p=Path('work/390-support-queue.json');j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Inspect interrupted action before resuming'
for i in range(j['done'],len(steps)):
 cmd=steps[i];j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
