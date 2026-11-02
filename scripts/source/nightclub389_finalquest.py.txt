"""Normal final quest briefing and Giratina withdrawal; reviewed linear scenes."""
import subprocess,sys,json,time
from pathlib import Path
steps=[('eventq',827,82,'talk'),('linear_dialog',827,82,'--source-page',15,'--burst'),('eventq',827,3,'talk'),('pc_open_reviewed',),('pc_select_box',3),('pc_exchange_named',13,3,'Giratina','Darkrai','--box',3),('checkpoint','Nightclub389-Giratina'),('eventq',827,1,'enter')]
# Exit selected below by installed doorway helper, stopping to handle Heather.
steps[-1]=('city_enter',827,826)
p=Path('work/389-quest-queue.json');j=dict(done=0,steps=steps)
assert not p.exists()
for i,cmd in enumerate(steps):
 j['pending']=dict(index=i,command=cmd,epoch=time.time());p.write_text(json.dumps(j,indent=2));print(cmd,flush=True)
 subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2))
