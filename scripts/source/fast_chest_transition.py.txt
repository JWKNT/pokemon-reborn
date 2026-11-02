"""After a publicly observed wild faint, intercept from recorded map pixels.
No game process/save/battle internals are accessed. Only the active capture
preview, installed map art and explicitly reviewed navigation inputs are used.
"""
import json,os,time,sys,subprocess
from pathlib import Path
import cv2,numpy as np
R=Path(__file__).resolve().parents[1]
def finish(timeout=12):
 from play import act
 sift=cv2.SIFT_create(nfeatures=4500)
 world=cv2.imread(str(R/'work/779-clean-map.png'),0);kw,dw=sift.detectAndCompute(world,None)
 deadline=time.time()+timeout
 settled_after=None
 settle_delay=float(os.environ.get("REBORN_WORLD_SETTLE",".35"));assert .05<=settle_delay<=.5
 step_wait=float(os.environ.get("REBORN_WORLD_STEP_WAIT",".10"));assert 0<=step_wait<=.2
 step_hold=float(os.environ.get("REBORN_WORLD_STEP_HOLD",".12"));assert .08<=step_hold<=.2
 while time.time()<deadline:
  h=json.loads((R/'recordings/capture-health.json').read_text())
  assert h.get('active') and time.time()-h['epoch']<2,'Fresh active capture required'
  frame=cv2.imread(str(R/'recordings/capture-preview.png'))
  if frame is None:time.sleep(.05);continue
  # Battle and story text windows are predominantly white inside this patch.
  patch=frame[480:565,70:770]
  white=np.mean((patch.min(2)>235)&((patch.max(2)-patch.min(2))<5))
  kf,df=sift.detectAndCompute(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),None)
  if df is None:time.sleep(.05);continue
  pairs=cv2.BFMatcher().knnMatch(dw,df,k=2);good=[a for a,b in pairs if a.distance<.65*b.distance]
  unique={}
  for m in sorted(good,key=lambda m:m.distance):unique.setdefault(m.trainIdx,m)
  good=list(unique.values())
  if len(good)<18:continue
  M,mask=cv2.estimateAffinePartial2D(np.float32([kw[m.queryIdx].pt for m in good]),np.float32([kf[m.trainIdx].pt for m in good]),method=cv2.RANSAC,ransacReprojThreshold=2)
  if M is None or mask.sum()<18 or not 1.60<M[0,0]<1.72 or abs(M[0,1])>.02:continue
  if settled_after is None:
   settled_after=time.time()+settle_delay
  if time.time()<settled_after:time.sleep(.03);continue
  reference=cv2.warpAffine(world,M,(frame.shape[1],frame.shape[0]))
  mono=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY);valid=(reference>40)&(mono>8)
  brightness=float(np.median(mono[valid]/reference[valid]))
  gray=np.mean((patch.min(2)>110)&((patch.max(2)-patch.min(2))<25))
  if gray>.4:
   from play import read
   text=' '.join(read().lower().split())
   if 'garchomp is preparing' in text and 'rush' in text:
    act('c:.12','wait:.10');continue
   if 'repel' in text and 'wore off' in text:
    act('c:.12','wait:.18','x:.12','wait:.10');continue
   if 'use another repel' in text:
    act('x:.12','wait:.10');continue
   if len(text.replace('pokemon reborn','').strip())<10:time.sleep(.05);continue
   raise RuntimeError('Unexpected dialogue over map: '+text)
  proof={'epoch':time.time(),'matrix':M.tolist(),'inliers':int(mask.sum()),'white_fraction':float(white),'brightness_ratio':brightness,'basis':'Public recorded world pixels matched installed map art'}
  cv2.imwrite(str(R/'work/fast-chest-transition-world.png'),frame)
  checkpoint=os.environ.get('REBORN_POST_BATTLE_CHECKPOINT')
  if checkpoint:
   subprocess.run([sys.executable,str(R/'scripts/chest_prompt_checkpoint.py'),checkpoint],check=True)
   proof.update(checkpoint=checkpoint,input_end_epoch=time.time())
   (R/'work/fast-chest-transition.json').write_text(json.dumps(proof,indent=2))
   return
  route=os.environ.get('REBORN_POST_BATTLE_ROUTE');seq=[]
  goal=os.environ.get('REBORN_POST_BATTLE_GOAL')
  if goal:
   from nav import route as plan_route
   point=cv2.invertAffineTransform(M) @ np.array([426,346.7,1])
   pos=[round(point[0]/32-.5),round(point[1]/32-1)]
   target=tuple(map(int,goal.split(',')))
   assert 23<=pos[0]<=30 and 40<=pos[1]<=46 and 23<=target[0]<=30 and 40<=target[1]<=46
   v=json.loads((R/'work/170-magwin-frozen.json').read_text());v['position']=pos
   v['events']={k:e for k,e in v['events'].items() if int(k)<77}
   keys=plan_route(v,target);assert len(keys)<=12
   proof.update(position=pos,goal=target,keys=keys)
   seq=[a for k in keys for a in (k.removeprefix('jump:')+':'+str(step_hold),'wait:'+str(step_wait))]
  elif route:
   for step in json.loads(Path(route).read_text()):
    key=step['key'];assert key in ['up','down','left','right','jump:up','jump:down','jump:left','jump:right'] and not step.get('action')
    seq += [key.removeprefix('jump:')+':.12','wait:'+str(step.get('wait',.5 if key.startswith('jump:') else .10))]
  else:
   keys=os.environ.get('REBORN_POST_BATTLE_MOVES','').split(',')
   assert 0<len(keys)<=12 and all(k in ['up','down','left','right']for k in keys)
   seq=[v for k in keys for v in (k+':.12','wait:.10')]
  act(*seq)
  proof['input_end_epoch']=time.time();(R/'work/fast-chest-transition.json').write_text(json.dumps(proof,indent=2))
  with (R/'recordings/fast-world-transitions.jsonl').open('a') as stream:stream.write(json.dumps(proof)+'\n')
  print('FAST PUBLIC MAP INTERCEPTION',proof,flush=True)
  subprocess.run([sys.executable,str(R/'scripts/chest_await.py'),'--world-open'],check=True)
  return
 raise RuntimeError('No verified text-free map within 12 seconds; no route input sent')
if __name__=='__main__':finish()
