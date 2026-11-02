"""Route explicit known map/coordinates; no saving. Stop on dialogue/battle."""
from nav import *
from locate import locate
# Each JSON step: [map,startx,starty,destx,desty, optional key actions]
steps=json.loads(pathlib.Path(sys.argv[1]).read_text())
for step_index,(mid,sx,sy,tx,ty,*tail) in enumerate(steps):
 observed_positions=[]
 for attempt in range(40):
  if step_index==0 and attempt==0 and "--from-verified" in sys.argv:actual=mid
  else:
   try:actual,sx,sy=locate(mid)
   except SystemExit as error:
    txt=read().lower()
    if error.code==2 and 'repel' in txt and re.search(r'(?:w|u)ore\s*of\s*f',txt):
     subprocess.run([sys.executable,str(ROOT/'scripts/renew_repel.py')]+(['--cancel'] if os.environ.get('REBORN_REPEL_POLICY')=='cancel' else []),check=True)
     print('REPEL MESSAGE CLEARED after coordinate interruption',flush=True);continue
    raise
  if actual!=mid:raise SystemExit(f'Map mismatch: actual {actual}, expected {mid}')
  if (sx,sy)==(tx,ty):break
  observed_positions.append((sx,sy))
  if len(observed_positions)>=6 and len(set(observed_positions[-6:]))<=2:
   raise SystemExit('Repeating route cycle: inspect turbo or obstacle before retrying')
  if len(observed_positions)>=3 and len(set(observed_positions[-3:]))==1:
   raise SystemExit('Repeated coordinate: inspect map state before retrying')
  v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy)],stderr=subprocess.DEVNULL))
  path=route(v,(tx,ty));print('ROUTE',mid,[sx,sy],'→',[tx,ty],len(path),'tiles',flush=True)
  # Bound by actual steps, so a route with many turns still makes useful
  # progress before the next coordinate check. Moving NPCs are replanned.
  chunk_limit=min(112,max(1,int(os.environ.get('REBORN_ROUTE_CHUNK','84' if 678<=mid<=683 or 710<=mid<=715 else '28'))))
  path=path[:(20 if mid==355 else chunk_limit)]
  groups=[(key,len(list(g))) for key,g in groupby(path)]
  mounted=json.loads((ROOT/"notes/navigation-state.json").read_text()).get("switches",{}).get("291",False)
  batch_size=len(groups)
  for j in range(0,len(groups),batch_size):
   seq=[]
   cursor=(sx,sy);graph=route(v,(tx,ty),True)
   for key,n in groups[j:j+batch_size]:
    for _ in range(n):
     if action_jump(v,cursor,key):seq.extend([key[5:]+':.03','c','wait:.9'])
     elif key.startswith('jump:'):
      # Toybox chains several bouncing pads; wait until the forced route ends
      # before a following direction can reverse a later pad mid-flight.
      jump_wait=6 if mid==874 else (3 if mid in [209,882,887] else .9)
      seq.extend([key[5:]+':.12','wait:'+str(jump_wait)])
     else:
      seq.append(key+':.12')
      # Splash Grounds retains the slower underwater movement animation.
      # Public coordinates297 verified dropped direction changes without a gap.
      step_pause=float(os.environ.get('REBORN_ROUTE_STEP_PAUSE','0.10' if mid in [862,886] else '0'))
      assert 0<=step_pause<=.3
      if step_pause:seq.append('wait:'+str(step_pause))
     destinations=[p for k,p in graph.get(cursor,[]) if k==key]
     if len(destinations)!=1:raise SystemExit('Route edge ambiguity')
     # Tall grass disables running (installed Walk_Run.rb), so the next tap
     # must wait for the slower step to finish before changing direction.
     if not key.startswith('jump:') and 'terrain' in v:
      width,height=v['width'],v['height'];tags=v['terrain']['data'];tiles=v['data']['data']
      def grass_at(point):
       xx,yy=point
       for zz in [2,1,0]:
        tag=tags[tiles[xx+width*yy+width*height*zz]]
        if tag and tag!=13:return tag==10
       return False
      if grass_at(cursor) or grass_at(destinations[0]):seq.append('wait:.15')
     cursor=destinations[0]
   # Circus/elevator paths have ordinary straight ground. A held key removes
   # per-tap overhead; each bounded chunk is still checked at its actual endpoint.
   if mid==694 or os.environ.get('REBORN_ROUTE_HELD')=='1':
    # Verify coordinates before every turn following a long hold. Small
    # timing differences must not carry into a later direction change.
    groups_seq=[(key,len(list(items)))for key,items in groupby(seq)]
    prefix=[]
    for key,n in groups_seq:
     if key.endswith(':.12') and n>=6:
      if not prefix:prefix=[key.split(':')[0]+':'+str(round(n*.125+.02,3))]
      break
     prefix.extend([key]*n)
    seq=prefix or seq
   if mid in [355,365]:
    held=[]
    for key,items in groupby(seq):
     n=len(list(items))
     tile_seconds=.1
     if key.endswith(':.12') and n>1:held.append(key.split(':')[0]+':'+str(round(n*tile_seconds+.02,3)))
     else:held.extend([key]*n)
    seq=held
   try:act(*seq)
   except subprocess.CalledProcessError as error:
    if error.returncode!=2:raise
    # A capture interruption releases the held key. Re-read coordinates only
    # after the recorder's heartbeat confirms that capture has recovered.
    recovered=False
    for _ in range(20):
     try:
      health=json.loads((ROOT/'recordings/capture-health.json').read_text())
      recovered=health.get('active',False) and time.time()-health.get('epoch',0)<2
     except (OSError,ValueError):recovered=False
     if recovered:break
     time.sleep(.5)
    if not recovered:raise
    print('CAPTURE RECOVERED: recalculating from actual coordinates',flush=True)
    break
   rr=snap();txt=' '.join(t['text'] for t in rr)
   if 'poison' in txt.lower() and ('faded' in txt.lower() or 'survived' in txt.lower() or 'surwived' in txt.lower()):
    act('c','wait:0.4');print('Poison recovery message cleared',flush=True);break
   if 'repel' in txt.lower() and any(z in ''.join(txt.lower().split()) for z in ['woreoff','uoreoff']):
    subprocess.run([sys.executable,str(ROOT/'scripts/renew_repel.py')]+(['--cancel'] if os.environ.get('REBORN_REPEL_POLICY')=='cancel' else []),check=True)
    print('REPEL EXPIRED: stopped movement; recalculating route',flush=True)
    break
   if re.search(r'(?<![a-z])hp(?![a-z])|\bfight\b|\bwild\s',txt.lower()) or any(t['y']>.73 and len(t['text'])>22 for t in rr):
    print('INTERRUPTED',txt,flush=True);sys.exit(2)
   # Re-read coordinates after each bounded batch before planning the next turns.
   break
 else:raise SystemExit('Position mismatch after retries')
 if tail:act(*tail[0]);print(read(),flush=True)
print('QUEUE DONE',flush=True)
