"""Continuous ordinary path plus one reviewed Emerald lever interaction."""
from nav import *
from locate import locate
from itertools import groupby
eid=int(sys.argv[1]);assert eid in [46,48,50,53,54,56,57]
m,x,y=locate(805)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'805',str(x),str(y)],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
opts=[]
for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
 try:
  p=route(v,(e['x']+dx,e['y']+dy));opts.append((len(p),p,k))
 except ValueError:pass
_,p,k=min(opts);assert len(p)<=100
seq=[]
for d,g in groupby(p):
 n=len(list(g));seq.append(d+':'+str(round(.1*n+.02,3)) if n>=3 else d+':.12')
 if n==2:seq.append(d+':.12')
print('FAST LEVER',eid,p,flush=True)
act(*seq,k+':.18','c','wait:.3')
print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),f'Emerald211-Lever{eid}'],check=True)
print('SAVED LEVER RESULT; verify switch before next action',flush=True)
