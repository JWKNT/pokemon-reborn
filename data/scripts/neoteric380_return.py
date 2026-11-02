"""Return after both saved captures using normal menus; accept the desert follow-up."""
import os,subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[('use_field_item','Escape Rope'),('fly_to',527,'--carrier','Rayquaza'),('eventq',527,87,'enter'),('eventq',826,6,'enter'),('eventq',827,2,'talk'),('overworld',),('eventq',827,57,'talk'),('linear_dialog',827,57,'--source-page',2,'--burst'),('checkpoint','Neoteric380-Complete')]
p=R/'work/neoteric380-return.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review interrupted step'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('RETURN380',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
