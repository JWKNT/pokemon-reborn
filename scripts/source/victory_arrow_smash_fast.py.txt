"""Short public-coordinate corrections for a reviewed hazard cart/lever."""
from nav import *
import shutil,time
E=int(sys.argv[1]);label=sys.argv[2];assert E in [62,63,64]
assert re.fullmatch(r'[A-Za-z0-9-]+',label)
t=read().lower();assert 'cancel' in t and t.count('hp')>=5
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'787','0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(E)]
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
  assert 'Kernel.pbRockSmash' in str(e['list'])
  assert cur==goal;seq += ['wait:.3']+[facing+(':.03'if E==148 else':.18')]+['c','wait:'+('10'if E in [122,128,132,133,140,141]else ('2'if E==148 else '.7'))]
 print('RAPID INTERACTION CHUNK',E,(sx,sy),goal,chunk,complete,flush=True);act('c:.12','wait:.1',*seq)
 if complete:break
 act('wait:.25')
else:
 subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True);raise SystemExit('Approach limit')

# Resolve only the normal Rock Smash prompt, stopping on a wild battle.
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--yes','--limit=10'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True)
# Verify the visibly smashed event in this freshly written owned map snapshot.
ruby="require_relative 'scripts/read_rgss';v=load_rgss(ARGV[0]);e=v[:Map].instance_variable_get(:@events)[ARGV[1].to_i];puts JSON.generate({map:v[:map_id],erased:e.instance_variable_get(:@erased)})"
frozen=ROOT/'backups'/f'Aster-{label}.rxdata'
proof=json.loads(subprocess.check_output(['ruby','-e',ruby,str(frozen),str(E)],cwd=ROOT,stderr=subprocess.DEVNULL))
assert proof=={'map':787,'erased':True},('Rock was not erased',proof)
p=ROOT/'notes/navigation-overrides.json';n=json.loads(p.read_text());n.setdefault('787',[])
if E not in n['787']:n['787'].append(E)
p.write_text(json.dumps(n)+'\n')
print('NORMAL ROCK SMASH VERIFIED',E,proof,flush=True)
