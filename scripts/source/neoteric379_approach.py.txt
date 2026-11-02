"""Reviewed Fern scene and ordinary corridor; stop one tile before boss trigger."""
import os,subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.10')
steps=[('q','895,25,59,right'),('linear_dialog',895,117,'--source-page',1,'--burst'),('checkpoint','Neoteric379-FernScene'),('eventq',895,114,'enter'),('q','895,55,27'),('checkpoint','Neoteric379-BossEntry')]
p=R/'work/neoteric379-approach.json';j=json.loads(p.read_text())if p.exists()else dict(done=0,steps=steps)
assert not j.get('pending'),'Review prior interrupted step first'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('APPROACH',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
