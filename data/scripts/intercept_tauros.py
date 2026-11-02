"""Bounded screenshot-driven interception of the roaming shortcut Tauros."""
from play import *
from track_tauros import capture,detect
import play
play.KEY=str(ROOT/"scripts/key_fast")
for i in range(100):
 a=capture();r=detect(a)
 if not r or r[0]>12:
  t=read();print('REVIEW',t,flush=True)
  if 'tauros' in t.lower() or 'yes' in t.lower():break
  if any(z in t.lower() for z in ['fight','yes','close bag','quit game']):raise SystemExit('UI review')
  act('wait:0.1');continue
 score,x,y,row,_=r
 vx,vy={0:(0,1),1:(-1,0),2:(1,0),3:(0,-1)}[row]
 dx=x+vx*24-256;dy=y+vy*24-208
 print(i,round(score,1),dx,dy,flush=True)
 if abs(dx)<20 and 12<abs(dy)<52:
  direction='down' if dy>0 else 'up'
  act(direction+':0.025','c:0.08','wait:0.08','c:0.08','wait:0.15')
  t=read();print(t,flush=True)
  if 'tauros' in t.lower() or 'yes' in t.lower():break
 elif abs(dy)<20 and 12<abs(dx)<52:
  direction='right' if dx>0 else 'left'
  act(direction+':0.025','c:0.08','wait:0.08','c:0.08','wait:0.15')
  t=read();print(t,flush=True)
  if 'tauros' in t.lower() or 'yes' in t.lower():break
 else:
  act('wait:0.04')
else:raise SystemExit('Interception limit')
