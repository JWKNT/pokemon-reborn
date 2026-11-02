"""Cross a read-only installed map connection with normal walking, verifying arrival."""
from nav import *
from locate import locate
m,n=map(int,sys.argv[1:3]);near=tuple(map(int,sys.argv[3:5])) if len(sys.argv)>=5 else None
actual,x,y=locate(m);assert actual==m
connections=json.loads((ROOT/'work/map-connections-reviewed.json').read_text())
pairs=[]
for a,ax,ay,b,bx,by in connections:
 if (a,b)==(m,n):pairs.append((ax,ay,bx,by))
 if (b,a)==(m,n):pairs.append((bx,by,ax,ay))
assert pairs,'No installed connection between requested maps'
def load(mid,position):return json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),*map(str,position)],stderr=subprocess.DEVNULL))
v=load(m,(x,y));vv=load(n,(0,0));choices=[]
for ax,ay,bx,by in pairs:
 for k,dx,dy in [('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]:
  edge=[(xx,0)for xx in range(v['width'])]if k=='up' else ([(xx,v['height']-1)for xx in range(v['width'])]if k=='down' else ([(0,yy)for yy in range(v['height'])]if k=='left' else [(v['width']-1,yy)for yy in range(v['height'])]))
  for sx,sy in edge:
   tx,ty=sx+dx-ax+bx,sy+dy-ay+by
   if not (0<=tx<vv['width'] and 0<=ty<vv['height']):continue
   # The translated source edge must be outside the destination by one tile.
   fx,fy=sx-ax+bx,sy-ay+by
   if 0<=fx<vv['width'] and 0<=fy<vv['height']:continue
   try:
    p=route(v,(sx,sy));nv=dict(vv,position=[tx,ty]);tail=route(nv,near)if near else []
    # Require a real reciprocal inward walking edge at the destination.
    graph=route(nv,None,True)
    if not graph.get((tx,ty)):continue
    choices.append((len(p)+len(tail),(sx,sy),k,(tx,ty)))
   except ValueError:pass
assert choices,'No reachable ordinary walking connection'
_,p,k,d=min(choices);print('CONNECTED WALK',m,p,k,'->',n,d,flush=True)
result=subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{p[0]},{p[1]}'])
if result.returncode:
 a,xx,yy=locate()
 if a==n and abs(xx-d[0])+abs(yy-d[1])<=2:
  print('CONNECTION ARRIVAL VERIFIED during boundary approach',a,xx,yy,flush=True)
  raise SystemExit(0)
 raise SystemExit('Boundary approach stopped away from the verified destination: '+str((a,xx,yy)))
act(k+':.12','wait:1')
a,xx,yy=locate(n);assert a==n,'Connection did not arrive at requested map'
assert abs(xx-d[0])+abs(yy-d[1])<=1,((xx,yy),d)
print('CONNECTION ARRIVAL VERIFIED',a,xx,yy,flush=True)
