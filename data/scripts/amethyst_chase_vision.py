"""Normal-key chase driven by public capture warning and crystal-break pixels."""
from nav import *
import cv2,numpy as np
plan=json.loads((ROOT/'work/amethyst-route-plan.json').read_text());out=ROOT/'work'/f'amethyst-attempt-{int(time.time())}';out.mkdir();start=time.time();journal={'start_epoch':start,'events':[]};jp=out/'journal.json'
import atexit
session=json.loads((ROOT/'notes/current-run-control.json').read_text())['recording_session']
def retain_attempt():
 end=time.time()+20;journal['end_epoch']=end;jp.write_text(json.dumps(journal,indent=2))
 p=ROOT/'recordings'/f'session-{session:03}.json';m=json.loads(p.read_text());m.setdefault('include_intervals',[]).append([start-m['start_epoch'],end-m['start_epoch']]);p.write_text(json.dumps(m,indent=2))
 cue=next((x['epoch'] for x in journal['events'] if x['kind']=='start_warning'),None)
 if cue:
  p=ROOT/'work'/f'session-{session:03}-music-overrides.json';rows=json.loads(p.read_text()) if p.exists() else []
  rows.append({'start':cue-m['start_epoch'],'end':end-m['start_epoch'],'track':'Battle- Misc','reason':'Public Amethyst chase; endpoint to reconcile against actual recorded exit'});p.write_text(json.dumps(rows,indent=2))
atexit.register(retain_attempt)
def log(kind,**kw):
 journal['events'].append(dict(epoch=time.time(),kind=kind,**kw));jp.write_text(json.dumps(journal,indent=2));print(kind,kw,flush=True)
def frame():
 h=json.loads((ROOT/'recordings/capture-health.json').read_text());assert h['active'] and time.time()-h['epoch']<2
 return cv2.resize(cv2.imread(str(ROOT/'recordings/capture-preview.png')),(512,384))
def warning():
 im=frame()[20:125,205:307];b,g,r=cv2.split(im);return int(((r>110)&(r>g.astype(float)*1.3)&(r>b.astype(float)*1.15)).sum())>450
floor=cv2.imread(str(ROOT/'work/amethyst-floor958.png'))
mp=cv2.imread(str(ROOT/'work/installed-map-806.png'))
maps={i:json.loads((ROOT/'work'/f'amethyst-stage-{i}-map.json').read_text()) for i in range(3,9)}
def public_position(expected):
 im=frame();candidates=[]
 assert im.std()>12, 'Chase fade/death: stop input'
 for x,y,w,h in [(20,180,170,160),(315,180,170,160),(20,35,170,120)]:
  ex=int(expected[0]*32-240+x);ey=int(expected[1]*32-176+y)
  ox=max(0,ex-96);oy=max(0,ey-96);roi=mp[oy:ey+h+96,ox:ex+w+96]
  result=cv2.matchTemplate(roi,im[y:y+h,x:x+w],cv2.TM_CCOEFF_NORMED);_,score,_,(mx,my)=cv2.minMaxLoc(result)
  candidates.append((score,(mx+ox-x+240)/32,(my+oy-y+176)/32))
 score,x,y=max(candidates)
 if score<=.80:cv2.imwrite(str(out/'position-review.png'),im)
 assert score>.80,('public position confidence',candidates)
 return x,y
edges=subprocess.Popen([str(ROOT/'scripts/key_edges')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1)
def close_edges():
 try:edges.stdin.close();edges.wait(timeout=2)
 except Exception:pass
atexit.register(close_edges)
def edge(key,down):
 edges.stdin.write(('down ' if down else 'up ')+key+'\n');edges.stdin.flush();assert edges.stdout.readline().strip()=='OK'
last_frame=0
actual=(20.,30.)
def observe_position():
 global last_frame,actual
 p=ROOT/'recordings/capture-preview.png'
 deadline=time.time()+1
 while p.stat().st_mtime_ns==last_frame:
  assert time.time()<deadline,'No fresh recorded frame'
  time.sleep(.004)
 last_frame=p.stat().st_mtime_ns;actual=public_position(actual);return actual
def walk(keys,stage,start):
 global actual
 current=tuple(start)
 for d,g in groupby(keys):
  n=len(list(g));dx,dy={'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}[d];goal=(current[0]+dx*n,current[1]+dy*n)
  edge(d,True);pressed=time.time();deadline=pressed+n*.3+2
  try:
   while True:
    x,y=observe_position();remaining=(goal[0]-x)*dx+(goal[1]-y)*dy
    if remaining<(0.99 if n==1 else 1.3) and abs((goal[0]-x)*dy+(goal[1]-y)*dx)<.1:
     log('key_release',direction=d,goal=goal,actual=actual,held=time.time()-pressed);break
    assert time.time()<deadline,('Movement blocked',current,goal,actual)
  finally:edge(d,False)
  current=goal
 # Finish the final committed step before interacting or testing a crystal.
 deadline=time.time()+1
 while abs(actual[0]-current[0])+abs(actual[1]-current[1])>.12:
  observe_position();assert time.time()<deadline,('Arrival mismatch',actual,current)
def climb(part):
 global actual
 edge(part['direction'],True);time.sleep(.10);edge(part['direction'],False)
 edge('c',True);time.sleep(.10);edge('c',False)
 goal=part['end'];deadline=time.time()+3
 while abs(actual[0]-goal[0])+abs(actual[1]-goal[1])>.15:
  observe_position();assert time.time()<deadline,('Cliff landing timeout',actual,goal)
log('attempt_start')
act('down:.18','c','wait:1')
# Scene dialogue is read from captured pixels; the chase begins at the red cue.
t=time.time()
while time.time()-t<180:
 if warning():break
 im=frame();roi=im[292:357,30:480];white=np.mean(np.min(roi,axis=2)>235)
 if white>.5:
  text=read();log('dialogue',text=text);act('c','wait:.3')
 else:time.sleep(.06)
else:raise SystemExit('No chase cue within three minutes')
log('start_warning');cv2.imwrite(str(out/'start.png'),frame())
for row in plan:
 log('route_start',stage=row['stage'])
 for part in row['parts']:
  if 'walk' in part:walk(part['walk'],row['stage'],part['start'])
  elif 'cliff' in part:climb(part)
  else:act(part['exit']+':.15','wait:1')
 cv2.imwrite(str(out/f'arrival-{row["stage"]}.png'),frame())
 if row['stage']==8:break
 floor=cv2.imread(str(ROOT/"work"/f"amethyst-open-{row['stage']}.png"))
 # Camera centers on the player; compare the crystal's replacement rock tile.
 gx,gy=row['goal'];tx,ty=[(39,33),(61,38),(27,49),(21,62),(53,60)][row['stage']-3];x=240+(tx-gx)*32;y=176+(ty-gy)*32
 assert 0<=x<480 and 0<=y<352
 t=time.time();best=1e9
 while time.time()-t<15:
  im=frame();tile=im[y:y+32,x:x+32];err=float(np.abs(tile.astype(float)-floor.astype(float)).mean());best=min(best,err)
  if err<10:
   log('crystal_break',stage=row['stage'],error=err);cv2.imwrite(str(out/f'crystal-{row["stage"]}.png'),im);break
  time.sleep(.04)
 else:
  cv2.imwrite(str(out/'review.png'),frame());log('review_timeout',stage=row['stage'],best_error=best);raise SystemExit('Crystal did not verify; review public frame')
log('attempt_end');journal['end_epoch']=time.time();jp.write_text(json.dumps(journal,indent=2));print(read(),flush=True)
