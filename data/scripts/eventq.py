"""Approach an observed map event through normal game controls; no saves."""
from nav import *
from locate import locate,capture_ready
mid,eid=int(sys.argv[1]),int(sys.argv[2]);kind=sys.argv[3] if len(sys.argv)>3 else 'talk'
a,sx,sy=locate(mid)
if a!=mid:raise SystemExit(f'Wrong map: observed {a}, expected {mid}')
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy)],stderr=subprocess.DEVNULL))
e=v['events'][str(eid)];x,y=e['x'],e['y'];opts=[]
if kind=='enter' and not any(c['code']==201 for c in e['list'] or []):raise SystemExit('Entry event has no transfer; no input sent')
def transfer_arrived():
 capture_ready();act('wait:2')
 actual=locate()
 destinations={tuple(c['parameters'][1:4]) for c in e['list'] or [] if c['code']==201 and c['parameters'][0]==0}
 if actual in destinations:
  print('TRANSFER VERIFIED AFTER INTERRUPTION',actual,flush=True);return True
 return False
if not any(c['code'] not in [0,108,408] for c in (e['list'] or [])):raise SystemExit('Inactive event; no interaction')
required={c['parameters'][2] for c in e['list'] if c['code']==111 and len(c['parameters'])>=3 and c['parameters'][:2]==[6,-1]} if kind in ['item','enter'] else set()
meaningful=[c for c in e['list'] if c['code'] not in [0,108,408]]
if kind=='talk' and meaningful and meaningful[0]['code']==111 and meaningful[0]['parameters'][:2]==[6,-1]:
 direction=meaningful[0]['parameters'][2]
 # Some crystals deliberately do nothing from one side; their actions are in ELSE.
 required=({2,4,6,8}-{direction}) if len(meaningful)>1 and meaningful[1]['code']==411 else {direction}
# An immediate Exit Event Processing means this facing is forbidden, not required.
forbidden=set()
cmds=e['list'] or []
for i,c in enumerate(cmds[:-1]):
 if c['code']==111 and c['parameters'][:2]==[6,-1] and cmds[i+1]['code']==115:
  forbidden.add(c['parameters'][2])
if forbidden:required={2,4,6,8}-forbidden
for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
 if required and {'down':2,'left':4,'right':6,'up':8}[k] not in required:continue
 try:
  p=(x+dx,y+dy)
  if p!=(sx,sy) and any((ee['x'],ee['y'])==p and any(cc['code']==201 for cc in (ee['list'] or [])) for ee in v['events'].values()):continue
  opts.append((len(route(v,p)),p,k))
 except ValueError:pass
if not opts and kind=='talk':
 # RPG XP counters permit action-button interaction from two tiles away.
 # Check the installed tile flag, rather than guessing a booth's open side.
 w,h=v['width'],v['height']
 for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  cx,cy=x+dx,y+dy
  if not (0<=cx<w and 0<=cy<h):continue
  tiles=[v['data']['data'][cx+w*cy+w*h*z] for z in [2,1,0]]
  if not any(v['passages']['data'][t]&128 for t in tiles):continue
  try:
   p=(x+2*dx,y+2*dy);opts.append((len(route(v,p)),p,k))
  except ValueError:pass
if not opts:raise SystemExit('No accessible side')
hidden=kind=='item' and e['name']=='HiddenItem';turn_only=False
if hidden:
 faced=[]
 for _,pp,kk in opts:
  dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[kk]
  bb=(pp[0]-dx,pp[1]-dy)
  try:
   rr=route(v,bb);vv=dict(v,position=list(bb))
   if route(vv,pp)==[kk]:faced.append((len(rr)+1,pp,kk,bb))
  except ValueError:pass
 if faced:
  _,p,k,before=min(faced);steps=[[mid,sx,sy,*before,[]],[mid,0,0,*p,[]]]
 else:
  _,p,k=min(opts);steps=[[mid,sx,sy,*p,[]]];turn_only=True
else:
 _,p,k=min(opts);steps=[[mid,sx,sy,*p,[]]]
# Blake's live icicles can knock the player away during the coordinate pause.
# A short bounded burst crosses these doors; verify the resulting map and
# allow only the few ordinary steps that the held key can take after transfer.
exposed_victory_door=kind=='enter' and mid==784 and eid in [2,3,4,5]
print('EVENT',eid,kind,'from',p,k,flush=True)
f=ROOT/'notes/route-next.json';f.write_text(json.dumps(steps))
rc=subprocess.call([sys.executable,str(ROOT/'scripts/queue_route.py'),str(f),'--from-verified'])
if rc:
 if kind=='enter' and transfer_arrived():raise SystemExit(0)
 raise SystemExit(rc)
if exposed_victory_door:
 act(k+':.6','wait:1')
 actual=locate()
 destinations=[c['parameters'][1:4] for c in e['list'] if c['code']==201 and c['parameters'][0]==0]
 if any(actual[0]==dm and abs(actual[1]-dx)+abs(actual[2]-dy)<=6 for dm,dx,dy in destinations):
  print('EXPOSED TRANSFER VERIFIED',actual,flush=True);raise SystemExit(0)
 raise SystemExit('Exposed doorway destination review: '+str(actual))
if kind in ['cut','smash']:
 if ('pbCut' if kind=='cut' else 'pbRockSmash') not in str(e['list']):raise SystemExit('Wrong field-move event')
 act(k,'c','wait:0.7')
 opening=read();print(opening,flush=True)
 if 'may be able' in opening.lower():
  raise SystemExit('Field move unavailable; obstacle remains present')
 act('c','wait:0.7','c','wait:0.7','c','wait:3')
 t=read();print(t,flush=True)
 if 'channel opens' in t.lower() and 'lava' in t.lower():
  act('c','wait:1');t=read();print(t,flush=True)
 for _ in range(5):
  if 'shard' not in t.lower() or not any(z in t.lower() for z in ['put','obtained','found']):break
  act('c','wait:0.6');t=read();print(t,flush=True)
 rr=snap()
 if re.search(r'\bhp\b|\bwild\b|\bfight\b',t,re.I) and kind=='smash' and 'pbRockSmashRandomEncounter' in str(e['list']):
  print('INSPECTED ROCK SMASH WILD; normal Run only',flush=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py')],check=True)
  t=read();rr=snap()
 if any(v['y']>.72 and len(v['text'])>18 for v in rr) or re.search(r'\bhp\b|\bfight\b',t,re.I):raise SystemExit('Field move review')
 f=ROOT/'notes/navigation-overrides.json';vv=json.loads(f.read_text());vv.setdefault(str(mid),[])
 if eid not in vv[str(mid)]:vv[str(mid)].append(eid)
 f.write_text(json.dumps(vv))
 statepath=ROOT/'notes/navigation-state.json';state=json.loads(statepath.read_text()) if statepath.exists() else {'variables':{}}
 for cmd in e['list']:
  if cmd['code']==121:
   aa=cmd['parameters']
   if aa[0]==aa[1] and aa[0]!=568:state.setdefault('switches',{})[str(aa[0])]=aa[2]==0
  if cmd['code']==122:
   a=cmd['parameters']
   if a[0]!=a[1] or a[3]!=0 or a[2] not in [0,1]:raise SystemExit('Route state review')
   key=str(a[0])
   if a[2]==0:state['variables'][key]=a[4]
   else:state['variables'][key]+=a[4]
 statepath.write_text(json.dumps(state))
 # Smashable walls become transfer events rather than disappearing.
 transfer_page=False
 if any(c['code'] in [122,123] for c in e['list']):
  source=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(mid),str(eid)],stderr=subprocess.DEVNULL))
  transfer_page=any(any(c['code']==201 for c in page['list']) for page in source['pages'])
  if transfer_page:
   for c in e['list']:
    if c['code']==123:state.setdefault('self_switches',{})[f'{mid},{eid},{c["parameters"][0]}']=c['parameters'][1]==0
   statepath.write_text(json.dumps(state))
 if transfer_page or any(c['code']==121 and c['parameters'][0] not in (568,1260) for c in e['list']):
  vv[str(mid)]=[i for i in vv[str(mid)] if i!=eid];f.write_text(json.dumps(vv))
elif kind=='item':
 # A hidden item on an impassable console needs a reliable facing tap after
 # the coordinate popup. Short taps can miss the game's polling frame.
 bump_hidden=False
 if hidden:
  try:route(v,(x,y))
  except ValueError:bump_hidden=True
 facing=[k+':.18'] if bump_hidden else ([k+':0.03'] if turn_only else ([] if hidden else [k]))
 act(*facing,'wait:0.5','c','wait:0.8');t=read();print(t,flush=True)
 if 'pbItemBall' in str(e['list']):
  for _ in range(2):
   if any(word in t.lower() for word in ['found','obtained','received','put the','bag is full']):break
   act('wait:.6');t=read();print(t,flush=True)
  else:raise SystemExit('Pickup not publicly confirmed; inspect actual state before continuing')
 act('x:2.5','wait:0.5');t=read();print(t,flush=True)
 if 'Bag' in t and ('dex' in t.lower() or 'Options' in t):act('x','wait:1')
elif kind=='enter':
 if not any(c['code']==201 for c in e['list']):raise SystemExit('Not a transfer event')
 # New World portals have a scripted fade/wait before the actual transfer.
 # Let that animation finish before opening the coordinate overlay.
 portal_delay=sum(c['parameters'][0] for c in e['list'] if c['code']==106)>=60
 try:act(k,'wait:6' if portal_delay else 'wait:2')
 except subprocess.CalledProcessError as error:
  if error.returncode!=2:raise
  if not transfer_arrived():raise
 print(read(),flush=True)
else:act(k,'c','wait:1');print(read(),flush=True)
