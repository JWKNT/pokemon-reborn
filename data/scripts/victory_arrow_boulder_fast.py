"""Fast source-reviewed map787 push from a fresh public coordinate frame.

The frozen normal save supplies the boulder position. Walking and pushing form
one continuous key queue so icicles cannot strike during a destination pause.
A fresh normal save must confirm the exact boulder outcome before any next push.
"""
from nav import *
from hazard_position import party_position
import shutil,time
E=int(sys.argv[1]);key=sys.argv[2];assert E in [58,59,60,61,65,69,73,74]
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[key]
t=read().lower();assert 'cancel' in t and t.count('hp')>=5
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'787','0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(E)];assert e['name']=='Boulder' and 'pbPushThisBoulder' in str(e['list'])
other_boxes={i:[ev['x'],ev['y']] for i,ev in v['events'].items() if ev['name']=='Boulder' and i!=str(E)}
count=int(sys.argv[4]) if len(sys.argv)>4 else 1
assert 1<=count<=10
before=(e['x']-dx,e['y']-dy);expected=[e['x']+count*dx,e['y']+count*dy]
wall_burst=len(sys.argv)>4
if wall_burst:
 import ast
 assert False, 'Only source-reviewed SW/NW boulders permit wall bursts'
 tree=ast.parse((ROOT/'scripts/nav.py').read_text());fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='route')
 pure=ast.unparse(fun).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False')
 boxns=dict(ROOT=ROOT,json=json,heapq=heapq,re=re);exec(pure,boxns)
 vv=json.loads(json.dumps(v));vv['events'].pop(str(E));bg=boxns['route'](vv,None,True)
 assert not any(k==key for k,n in bg.get(tuple(expected),[])), 'No physical wall at planned stop'
 blocked={(ev['x'],ev['y']) for ev in vv['events'].values() if not ev['through']}
 cursor=(e['x'],e['y'])
 for _ in range(count):
  dest=(cursor[0]+dx,cursor[1]+dy);assert (key,dest) in bg.get(cursor,[]) and dest not in blocked
  cursor=dest

# Static source work stays in Party. Correct actual movement every six tiles.
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
 sx,sy,m=map(int,match.groups())
 from PIL import Image
 from coordinate_digits import fix_coordinates
 canvas=Image.open(ROOT/'work/capture-preview-frame-template.png').convert('RGB')
 canvas.paste(Image.open(cp).resize((2048,1536)),(112,134))
 native=ROOT/'work/rapid-coordinates-native.png';canvas.save(native)
 fixed=fix_coordinates(native,(sx,sy,m))
 if fixed!=(sx,sy,m):print('PUBLIC DIGIT TEMPLATE CORRECTION',(sx,sy,m),'->',fixed,flush=True)
 sx,sy,m=fixed;assert m==787
 return sx,sy
act('x','wait:.8','x','wait:.2');seen=[]
for attempt in range(15):
 sx,sy=public_position();v['position']=[sx,sy];seen.append((sx,sy))
 if len(seen)>=4 and len(set(seen[-4:]))==1:frozen_stop('No route progress')
 try:p=route(v,before)
 except ValueError:frozen_stop('Route blocked; inspect position')
 assert len(p)<=110;complete=len(p)<=6;chunk=p if complete else p[:6]
 g=route(v,None,True);cursor=(sx,sy);seq=[]
 for k in chunk:
  target=next(n for kk,n in g[cursor] if kk==k)
  if k.startswith('jump:'):seq += [k[5:]+':.12','wait:'+str(max(.9,.2*(abs(target[0]-cursor[0])+abs(target[1]-cursor[1]))))]
  else:seq += [k+':.12']
  cursor=target
 if complete:
  assert cursor==before
  seq += ['wait:.3',key+':'+str(count*.65+.7 if wall_burst else .2),'wait:1.0']
 print('BOULDER APPROACH CHUNK',E,(sx,sy),before,chunk,expected,complete,flush=True)
 act('c:.12','wait:.1',*seq)
 if complete:break
 act('wait:.25')
else:
 subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True);raise SystemExit('Approach limit; inspect')
label=sys.argv[3];assert re.fullmatch(r'[A-Za-z0-9-]+',label)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True)
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['positions']['787'][str(E)]==expected,('Push differs; inspect before retrying',s['positions']['787'][str(E)],expected)
print('HAZARD PUSH VERIFIED',E,expected,flush=True)

assert all(s['positions']['787'][i]==p for i,p in other_boxes.items()),'Another boulder moved: review entire current maze before continuing'
