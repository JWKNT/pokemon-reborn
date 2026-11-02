"""Sequential normal-UI training and candy preparation, with resumable action receipt."""
import os,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
base=json.loads((R/'work/neoteric378-training-queue.json').read_text());assert base['done']==24 and base['pending'] is None
steps=[('kyogre378_training','hp'),('kyogre378_training','spa'),('fly_to',519,'--carrier','Rayquaza'),('eventq',519,116,'enter'),('eventq',38,3,'talk'),('heal',),('checkpoint','Neoteric378-KyogreCandyReady'),('postgame_candy_spend','Neoteric378-KyogreCandyReady',145)]
p=R/'work/neoteric378-finish-training.json';j=json.loads(p.read_text()) if p.exists() else dict(done=0,steps=steps)
assert j.get('pending') is None,'Prior outcome must be reviewed first'
for i in range(j['done'],len(steps)):
 j['pending']=dict(index=i,command=steps[i],epoch=time.time());p.write_text(json.dumps(j,indent=2)+'\n')
 print('KYOGRE TRAINING',i,*steps[i],flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{steps[i][0]}.py'),*map(str,steps[i][1:])],check=True)
 j.update(done=i+1,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
print('KYOGRE TRAINING COMPLETE',flush=True)
