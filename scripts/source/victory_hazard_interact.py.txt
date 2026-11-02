"""Source-reviewed lower main-room cart/lever, starting and ending in Party."""
from nav import *
from hazard_position import party_position
E=int(sys.argv[1]);assert E in [118,122,128,130,132,133,134,136,140,141]
label=sys.argv[2];assert re.fullmatch(r'[A-Za-z0-9-]+',label)
m,sx,sy=party_position();assert m==784
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'784',str(sx),str(sy)],stderr=subprocess.DEVNULL));e=v['events'][str(E)]
options=[]
for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
 target=(e['x']+dx,e['y']+dy)
 try:options.append((len(route(v,target)),target,k,route(v,target)))
 except ValueError:pass
_,goal,k,path=min(options);assert len(path)<110
g=route(v,None,True);cur=(sx,sy);seq=[]
for key in path:
 nxt=next(n for kk,n in g[cur] if kk==key)
 if key.startswith('jump:'):seq += [key[5:]+':.12','wait:'+str(max(.9,.2*(abs(nxt[0]-cur[0])+abs(nxt[1]-cur[1]))))]
 else:seq.append(key+':.12')
 cur=nxt
assert cur==goal
print('HAZARD INTERACTION',E,goal,k,path,flush=True)
act('x','wait:.8','x','wait:.2',*seq,k+':.12','c','wait:'+('10' if E in [122,128,132,133,140,141] else '.6'))
t=read().lower();print(t,flush=True)
if any(w in t for w in ['fight','repel','used ','yes','no']):raise SystemExit('Public interruption review')
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True)
print('INTERACTION SAVED',label,flush=True)
