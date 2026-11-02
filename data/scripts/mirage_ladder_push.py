"""Bounded normal ladder pushes; verify resulting puzzle positions with a native save."""
import sys,json,subprocess,time,copy
from play import ROOT,act,read
from locate import locate
from route_readonly import route
mid,eid,count=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[4]);direction=sys.argv[3];label=sys.argv[5]
assert mid==882 and eid in [20,35,36,40,41] and 1<=count<=12
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[direction]
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
assert e['tile_id']==839 and any(c['code']==209 for c in e['list'])
x,y=e['x'],e['y'];blocked={(z['x'],z['y']) for k,z in v['events'].items() if k!=str(eid) and not z['through']}
gv=copy.deepcopy(v);gv['events'].pop(str(eid));gv['position']=[-1,-1];gv['ignore_ice']=True;g=route(gv,None,True)
def ice(p):
 w,h=v['width'],v['height']
 for z in [2,1,0]:
  tag=v['terrain']['data'][v['data']['data'][p[0]+w*p[1]+w*h*z]]
  if tag and tag!=13:return tag==12
 return False
pos=(x,y)
for i in range(count):
 dest=(pos[0]+dx,pos[1]+dy)
 assert (direction,dest) in g.get(pos,[]) and dest not in blocked,('Unsafe push',pos,dest)
 while ice(dest):
  nn=(dest[0]+dx,dest[1]+dy)
  if (direction,nn) not in g.get(dest,[]) or nn in blocked:break
  dest=nn
 pos=dest
expected=list(pos)
stand=(x-dx,y-dy)
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{mid},{stand[0]},{stand[1]}'],check=True)
assert locate(mid)==(mid,*stand)
act(direction+':.12','wait:.2')
for i in range(count):
 t=read().lower();assert not any(s in t for s in ['yes','no\n','fight','wild','hp','would you']),('Unexpected screen',t)
 act('c','wait:3')
 if i+1<count:act(direction+':.12','wait:.25')
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
n=json.loads((ROOT/'notes'/f'{label}-navigation.json').read_text());actual=n['positions'][str(mid)][str(eid)];assert actual==expected,('Ladder result differs',actual,expected)
print('LADDER GROUP VERIFIED',eid,actual,flush=True)
