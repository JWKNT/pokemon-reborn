"""Reviewed ordinary route back to Neoteric; stop before further story triggers."""
import os,subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[('fly_to',232,'--carrier','Rayquaza')]+[('city_enter',a,b)for a,b in [(232,231),(231,244),(244,261),(261,247),(247,259),(259,511)]]+[('field_repel','Super Repel'),('q','511,36,55,left'),('eventq',511,45,'enter'),('eventq',511,42,'enter'),('eventq',511,103,'enter'),('eventq',895,106,'enter'),('checkpoint','Neoteric379-Returned')]
p=R/'work/neoteric379-return.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review prior interrupted step first'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('RETURN',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
