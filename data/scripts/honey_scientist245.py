"""Bounded ordinary interaction with the visually tracked Nature Center scientist."""
from nav import *
from locate import locate
from find_visible_sprite import find
for i in range(12):
 mid,x,y=locate(294)
 if mid!=294:raise SystemExit('Wrong map')
 t=read()
 if len(t.splitlines())>1:print('DIALOGUE REVIEW',t);break
 r=find('trchar008');print('VISIBLE',r,flush=True)
 if not r or r[0]>.08:raise SystemExit('Sprite match uncertain')
 ex=x+round((r[1]-256)/32);ey=y+round((r[2]-208)/32)
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'294',str(x),str(y)],stderr=subprocess.DEVNULL))
 v['events']['29'].update(x=ex,y=ey)
 choices=[]
 for dx,dy,key in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  try:p=route(v,(ex+dx,ey+dy));choices.append((len(p),p,key))
  except ValueError:pass
 if not choices:raise SystemExit('No accessible side')
 n,p,key=min(choices)
 if any(k.startswith('jump:') for k in p):raise SystemExit('Unexpected jump')
 act(*p[:3])
 if n<=3:
  act(key,'c','wait:.3');t=read();print(t,flush=True)
  if len(t.splitlines())>1:break
else:raise SystemExit('Bounded pursuit exhausted')
