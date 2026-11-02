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
 return round(x),round(y)
def walk(keys,stage,start):
 if stage>3:
  seq=[];current=tuple(start)
  for d,g in groupby(keys):
   n=len(list(g));dx,dy={'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}[d];current=(current[0]+dx*n,current[1]+dy*n)
   seq.extend([d+':'+str(.12 if n==1 else round(.1*n+.02,3))])
  if seq:act(*seq)
  return
 current=tuple(start)
 for d,g in groupby(keys):
  n=len(list(g));dx,dy={'left':(-1,0),'right':(1,0),'up':(0,-1),'down':(0,1)}[d];expected=(current[0]+dx*n,current[1]+dy*n)
  act(d+':'+str(.12 if n==1 else round(.1*n+.02,3)), 'wait:.08')
  verify_arrival(stage,expected);current=expected
def verify_arrival(stage,expected):
 for attempt in range(3):
  time.sleep(.23);actual=public_position(expected)
  if actual==tuple(expected):return
  cv2.imwrite(str(out/f'correction-{len(journal["events"])}.png'),frame())
  log('position_correction',actual=actual,expected=expected)
  assert abs(actual[0]-expected[0])+abs(actual[1]-expected[1])<=4
  v=maps[stage];v['position']=actual;keys=route(v,tuple(expected))
  assert len(keys)<=8
  for d in keys:act(d+':.12','wait:.08')
 raise SystemExit('Public arrival could not be corrected')
log('attempt_start');log('start_warning');act('c')
for row in plan[3:4]:
 log('route_start',stage=row['stage'])
 if row['stage']>3:
  seq=[]
  for part in row['parts']:
   if 'walk' in part:
    for d,g in groupby(part['walk']):
     n=len(list(g));seq.append(d+':'+str(.12 if n==1 else round(.1*n+.02,3)))
   elif 'cliff' in part:seq.extend([part['direction']+':.12','c:.12','wait:.2'])
   else:seq.extend([part['exit']+':.15','wait:1'])
  verify_capture_frame();subprocess.run([str(ROOT/'scripts/key_fast'),*seq],check=True)
 else:
  for part in row['parts']:walk(part['walk'],row['stage'],part['start'])
 if row['stage']!=8:verify_arrival(row['stage'],row['goal'])
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
act('d:.12','wait:.3');log('normal_quicksave_requested');print(read(),flush=True);
log('attempt_end');journal['end_epoch']=time.time();jp.write_text(json.dumps(journal,indent=2));print(read(),flush=True)
