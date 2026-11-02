"""Short public-coordinate corrections for a reviewed hazard cart/lever."""
from nav import *
import shutil,time
E=int(sys.argv[1]);label=sys.argv[2];assert E in [118,122,126,128,130,132,133,134,136,140,141,142,148]
assert re.fullmatch(r'[A-Za-z0-9-]+',label)
t=read().lower();assert 'cancel' in t and t.count('hp')>=5
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'784','0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(E)]
def frozen_stop(message):
 act('c','wait:.6');subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True);raise SystemExit(message)
def public_position():
 act('d:.6','wait:.1');epoch=time.time()
 for _ in range(30):
  h=json.loads((ROOT/'recordings/capture-health.json').read_text())
  if h.get('active') and h.get('preview_epoch',0)>=epoch and time.time()-h['epoch']<2:break
  time.sleep(.05)
 else:raise SystemExit('Fresh coordinate capture unavailable')
 cp=ROOT/'work/rapid-hazard-coordinates.png';shutil.copyfile(ROOT/'recordings/capture-preview.png',cp)
 rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)]));txt=' '.join(r['text']for r in rows)
 print('RAPID PUBLIC COORDINATES',txt,flush=True)
 match=re.search(r"X\s*(\d+)\s*[,.;]?\s*Y[\s\x27\u2019]*(\d+)\s*[,.;]?\s*map\s*(\d+)",txt,re.I)
 if not match:frozen_stop('Coordinate review')
 sx,sy,m=map(int,match.groups());assert m==784
 return sx,sy
act('x','wait:.8','x','wait:.2');seen=[]
for attempt in range(20):
 sx,sy=public_position();v['position']=[sx,sy];seen.append((sx,sy))
 if len(seen)>=4 and len(set(seen[-4:]))==1:frozen_stop('No route progress')
 options=[]
 for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  dest=(e['x']+dx,e['y']+dy)
  try:options.append((len(route(v,dest)),dest,k,route(v,dest)))
  except ValueError:pass
 if not options:frozen_stop('No interaction approach')
 _,goal,facing,path=min(options);assert len(path)<110;complete=len(path)<=6;chunk=path if complete else path[:6]
 g=route(v,None,True);cur=(sx,sy);seq=[]
 for k in chunk:
  nxt=next(n for kk,n in g[cur]if kk==k)
  if k.startswith('jump:'):seq += [k[5:]+':.12','wait:'+str(max(.9,.2*(abs(nxt[0]-cur[0])+abs(nxt[1]-cur[1]))))]
  else:seq.append(k+':.12')
  cur=nxt
 if complete:
  assert cur==goal;seq += ['wait:.3']+[facing+(':.03'if E==148 else':.18')]+['c','wait:'+('10'if E in [122,128,132,133,140,141]else ('2'if E==148 else '.7'))]
 print('RAPID INTERACTION CHUNK',E,(sx,sy),goal,chunk,complete,flush=True);act('c:.12','wait:.1',*seq)
 if complete:break
 act('wait:.25')
else:
 subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True);raise SystemExit('Approach limit')
t=read().lower();print(t,flush=True)
if E in [126,142]:
 assert 'pbRockClimb' in str(e['list']) and any(c['code']==201 and c['parameters'][1]==786 for c in e['list'])
 subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--yes','--limit=10'],check=True)
 t=read().lower()
if E==148:
 assert 'MAXREPEL' in str(e['list']) and 'pbItemBall' in str(e['list'])
 assert any(w in t for w in ['repel','obtained','found','put the']),t
 subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=6'],check=True)
 t=read().lower()
if any(w in t for w in ['fight','repel','used ','yes','no']):raise SystemExit('Public interruption review')
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True)
if E in [126,142]:
 result=json.loads((ROOT/'notes'/f'{label}-status.json').read_text())
 assert result['map']==786 and result['position']==({126:[69,21],142:[104,15]}[E]), ('Rock Climb transfer not reached',result['map'],result['position'])
print('RAPID INTERACTION SAVED',label,flush=True)
