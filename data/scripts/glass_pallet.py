"""Move a reviewed Glass pallet via its normal C-then-direction interface.
Only the observed completed source transition is mirrored in planning notes.
"""
from play import *
from locate import locate
from nav import route
from glass_positions import refresh
import argparse
p=argparse.ArgumentParser();p.add_argument('core',type=int);p.add_argument('direction',choices=['up','down','left','right']);a=p.parse_args()
actual=locate(732);assert actual[0]==732,actual
note=ROOT/'notes/navigation-state.json';state=json.loads(note.read_text());assert state['switches'].get('947'), 'Espeon must be the observed following companion'
model=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'732',*map(str,actual[1:])],stderr=subprocess.DEVNULL))
core=model['events'][str(a.core)];group=core['name'].split('Core')[0];desired={'down':2,'left':4,'right':6,'up':8}[a.direction];forbidden=10-desired
cs=core['list'];begins=[i for i,c in enumerate(cs)if c['code']==111 and c['parameters'][:2]==[1,62]and c['parameters'][3]==desired]
assert len(begins)==1,'This direction is not an available reviewed pallet motion'
beg=begins[0];indent=cs[beg]['indent'];end=next((i for i in range(beg+1,len(cs))if cs[i]['indent']<=indent and cs[i]['code']in[111,411,412]),len(cs));branch=cs[beg:end]
assign=[];conditions={};active={indent:True}
for c in branch[1:]:
 code,aa,depth=c['code'],c['parameters'],c['indent']
 parent=all(z for d,z in active.items() if d<depth)
 if code==111:
  if aa[:2]==[6,-1]:ok=False # We exclude the forbidden face below.
  elif aa[0]==1 and aa[2]==0:
   left=state['variables'].get(str(aa[1]),0);right=aa[3]
   ok=[left==right,left>=right,left<=right,left>right,left<right,left!=right][aa[4]]
  else:raise SystemExit('Unreviewed pallet branch condition '+str(aa))
  conditions[depth]=ok;active[depth]=parent and ok
 elif code==411:active[depth]=parent and not conditions[depth]
 elif code==412:active.pop(depth,None)
 elif parent and code==122 and 408<=aa[0]<=421:assign.append(aa)
assert len(assign)==1 and assign[0][0]==assign[0][1]and assign[0][2:4]==[0,0],('Ambiguous motion requires specific source review',assign)
assert any(c['code']==209 and c['parameters'][0]==a.core and any(m['code']in[1,2,3,4]for m in c['parameters'][1]['list'])for c in branch)
options=[]
for eid,e in model['events'].items():
 if (re.match(r'GB\d+',e['name']).group(0)if re.match(r'GB\d+',e['name'])else '')!=group or not any(c['code']==105 for c in e['list']):continue
 for dx,dy,k,d in [(0,1,'up',8),(0,-1,'down',2),(1,0,'left',4),(-1,0,'right',6)]:
  if d==forbidden:continue
  target=(e['x']+dx,e['y']+dy)
  try:options.append((len(route(model,target)),target,k,int(eid)))
  except ValueError:pass
assert options,'No accessible safe pallet face'
_,target,k,eid=min(options);print('REVIEWED PALLET',a.core,'interact',eid,'from',target,k,'move',a.direction,'sets',assign[0],flush=True)
f=ROOT/'notes/route-next.json';f.write_text(json.dumps([[732,0,0,*target,[]]]));subprocess.run([sys.executable,str(ROOT/'scripts/queue_route.py'),str(f)],check=True)
act(k+':.12','wait:.3','c','wait:.7');t=read();print(t,flush=True)
assert not re.search(r'\bhp\b|fight|choose a pok|yes|no',t,re.I),'Unexpected pallet input state'
# Source code105 is the visible purple directional-push prompt, not movement.
act(a.direction+':.12','wait:3');t=read();print(t,flush=True)
assert not re.search(r'\bhp\b|fight|choose a pok|yes|no',t,re.I),'Pallet result needs review'
assert locate(732)==(732,*target),'Player displaced while choosing pallet direction'
# An unchanged player coordinate is insufficient: with Espeon waiting, C can
# do nothing and a blocked arrow also leaves the player unchanged. Verify this
# meaningful puzzle transition against a normal native quicksave before using
# it to plan further actions. Never write the anticipated value into the save.
label=f'Glass-pallet-{a.core}-{a.direction}'
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
state=json.loads(note.read_text())
assert state['variables'].get(str(assign[0][0]))==assign[0][4],('Native save did not confirm pallet motion',assign[0],state['variables'].get(str(assign[0][0])))
source=json.loads((ROOT/'work/story-map-732-events.json').read_text());note.write_text(json.dumps(refresh(state,source)))
with(ROOT/'notes/glass-pallet-actions.jsonl').open('a')as f:f.write(json.dumps({'epoch':time.time(),'core':a.core,'interacted_event':eid,'player':list(target),'direction':a.direction,'source_assignment':assign[0],'evidence':'Normal inspected directional input; overworld returned and player coordinate unchanged. Review video/native checkpoint before relying on a new motion.'})+'\n')
print('PALLET MOTION VERIFIED IN NATIVE SAVE; PLANNER REFRESHED',flush=True)
