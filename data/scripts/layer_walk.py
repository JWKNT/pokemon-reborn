"""Execute a bounded Route 2 layered path; verify coordinates and update planning notes."""
from layer_route import *
from locate import locate
from PIL import Image
hold_straights='--hold-straights' in sys.argv
args=[a for a in sys.argv if a!='--hold-straights']
mid,tx,ty=map(int,args[1:4]);ground=bool(int(args[4]))
target_ground=bool(int(args[5])) if len(args)>5 else None
def ordinary_wtc_wild(text):
 if mid in [358,360]:
  approved=['rufflet','hawlucha','meditite','boldore','rhyhorn','rhydon','ursaring','machoke','trapinch','rockruff','donphan','mienfoo','absol','noctowl','vullaby']
  if not ('fight' in text or re.search(r'\bhp\b',text)) or not any(z in text for z in approved):return False
  rows=[json.loads(l)for l in(ROOT/'recordings/screens.jsonl').read_text().splitlines()]
  return any(r['epoch']>=action_started and ('appeared' in ' '.join(r['text']).lower() or re.search(r'\bwild\b',' '.join(r['text']),re.I))for r in rows)
 if mid not in set(range(468,477))|set(range(479,506)):return False
 approved=['gulp','grimer']
 if json.loads((ROOT/'notes/navigation-state.json').read_text())['switches'].get('548'):
  approved+=['muk','sualot','swalot']
 return ('fight' in text or re.search(r'\bhp\b',text)) and any(z in text for z in approved)
mm,x,y=locate(mid)
assert mm==mid
stalls=0
for iteration in range(45):
 if (x,y)==(tx,ty) and (target_ground is None or ground==target_ground):print('LAYER ROUTE COMPLETE',mid,x,y,ground,flush=True);break
 steps=plan(mid,x,y,ground,tx,ty,target_ground);chunk=[]
 for s in steps:
  chunk.append(s)
  if len(chunk)>=28 or s['from'][2]!=s['to'][2]:break
 seq=[]
 for step in chunk:
  key=step['key']
  if step.get('action_jump'):seq.extend([key[5:]+':.03','c','wait:.9'])
  elif key.startswith('jump:'):seq.extend([key[5:]+':.12','wait:.9'])
  else:seq.append(key+':.12')
 if hold_straights:
  compact=[]
  for key,items in groupby(seq):
   n=len(list(items))
   if key.endswith(':.12') and n>1:compact.append(key.split(':')[0]+':'+str(round(n*.1+.02,3)))
   else:compact.extend([key]*n)
  seq=compact
 print('LAYER SEGMENT', (x,y,ground),'to',chunk[-1]['to'],len(chunk),flush=True)
 action_started=time.time()
 try:act(*seq)
 except subprocess.CalledProcessError as error:
  if error.returncode!=2:raise
  recovered=False
  for _ in range(30):
   health=json.loads((ROOT/'recordings/capture-health.json').read_text())
   recovered=health.get('active') and time.time()-health.get('epoch',0)<2
   if recovered:break
   time.sleep(.5)
  if not recovered:raise
  print('CAPTURE RECOVERED; observe actual layer-route endpoint',flush=True)
 r=snap();text=' '.join(a['text'] for a in r).lower()
 # A wild transition can begin just after the last walking input. Observe
 # the fade before opening coordinate UI, rather than treating black as world.
 for _ in range(3):
  im=Image.open(STATE).convert('RGB');w,h=im.size
  pixels=list(im.crop((int(w*.06),int(h*.08),int(w*.94),int(h*.88))).getdata())
  if sum(max(p)<25 for p in pixels)/len(pixels)<.9:break
  act('wait:2');r=snap();text=' '.join(a['text'] for a in r).lower()
 if 'repel' in text and any(z in ''.join(text.split()) for z in ['woreoff','uoreoff']):
  subprocess.run([sys.executable,str(ROOT/'scripts/renew_repel.py')],check=True)
  r=snap();text=' '.join(a['text'] for a in r).lower()
 # These positively identified ordinary wild encounters occur on WTC mud.
 # Never auto-escape a trainer, PULSE boss, or unidentified battle.
 if ordinary_wtc_wild(text):
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(action_started)],check=True)
  r=snap();text=' '.join(a['text'] for a in r).lower()
 if any(s in text for s in ['fight',' hp','wild ','yes','no','wore off','uore off']) or any(a['y']>.73 and len(a['text'])>22 for a in r):raise SystemExit('Route dialogue/battle review: '+text)
 try:mm,nx,ny=locate(mid)
 except SystemExit as error:
  if error.code!=2:raise
  late=read().lower()
  if not ordinary_wtc_wild(late):raise
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(action_started)],check=True)
  mm,nx,ny=locate(mid)
 assert mm==mid
 candidates={(s['to'][0],s['to'][1],s['to'][2]) for s in chunk if tuple(s['to'][:2])==(nx,ny)}
 if not candidates:
  # A held direction can take one extra ordinary step just after a forced
  # stair move. Only accept that exact witnessed endpoint and inspected layer.
  for step in chunk:
   if not step['key'].startswith('jump:'):continue
   k=step['key'][5:];dx,dy,d=DIR[k];ex,ey,eg=step['to']
   if (nx,ny)!=(ex+dx,ey+dy):continue
   model=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(nx),str(ny),json.dumps({'switches':{'410':eg}})],stderr=subprocess.DEVNULL))
   for ev in model['events'].values():
    if ev['trigger']==1 and (ev['x'],ev['y'])==(nx,ny):eg=effect(ev,d,eg)
   candidates.add((nx,ny,eg));print('OBSERVED EXTRA STEP AFTER STAIR',nx,ny,eg,flush=True)
 if (nx,ny)==(x,y):candidates.add((x,y,ground));stalls+=1
 else:stalls=0
 if len(candidates)!=1 or stalls>=3:raise SystemExit('Layer position review: '+str((nx,ny,candidates)))
 x,y,ground=next(iter(candidates))
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v.setdefault('switches',{})['410']=ground;p.write_text(json.dumps(v))
else:raise SystemExit('Layer route iteration limit')
