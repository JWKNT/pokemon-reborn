"""Time a reviewed crossing from live sprite pixels only; recording guard remains active."""
from play import ROOT,read
from sprite_match import match
from PIL import Image
import subprocess,sys,time,json
# Player and guard coordinates must first be confirmed on screen.
px,py,gx,gy,direction=map(int,sys.argv[1:6]);keys=sys.argv[6:];probe='--probe' in keys;on_phase='--on-phase' in keys;quiet='--quiet-end' in keys;keys=[k for k in keys if not k.startswith('--')];assert keys or probe
raw=ROOT/'work/guard-live.png';base=ROOT/'work/guard-base.png'
x=256+(gx-px)*32-16;y=208+(gy-py)*32-44
margin=4 if (gx,gy) in [(41,18),(9,26),(9,10)] else 16
clip_top=max(0,margin-y)
if clip_top>34:raise SystemExit("Guard sprite too clipped")
box=(x-4,y+clip_top-margin,x+36,y+44+margin)
if min(box)<0 or box[2]>512 or box[3]>384:raise SystemExit('Guard not within visible camera')
static={(41,18):[6,8],(9,26):[4,8],(9,10):[2,8]}
directions=static.get((gx,gy),[2,8] if gx==32 else [4,6]);patterns=[0] if (gx,gy) in static else None
seen_other=on_phase
for _ in range(100):
 subprocess.run(['/usr/sbin/screencapture','-x','-l','260608',str(raw)],check=True)
 im=Image.open(raw)
 if im.size!=(2272,1816):raise SystemExit('Window geometry changed')
 im.crop((112,134,2160,1670)).resize((512,384),Image.Resampling.NEAREST).save(base)
 scores=match(base,box,directions=directions,patterns=patterns,clip_top=clip_top);best=scores[0];other=min(q[0] for q in scores if q[1]!=best[1])
 print(time.time(),best,'other',round(other,1),flush=True)
 if probe:
  Image.open(base).crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.NEAREST).save(ROOT/'work/guard-probe.png')
  break
 if best[0]>1500 or other<best[0]*1.2:continue
 if best[1]!=direction:seen_other=True
 elif seen_other:
  subprocess.run([str(ROOT/'scripts/key_fast'),*keys],check=True)
  print('CROSSING SENT',keys,flush=True)
  if not quiet:print(read(),flush=True)
  break
else:raise SystemExit('No confident facing transition; no crossing attempted')
