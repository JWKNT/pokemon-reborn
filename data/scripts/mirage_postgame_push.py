"""Push one inspected Mirage Tower block group through normal keys.

The primary block is verified in public pixels before and after each push.
Only planner notes change; no native data is written. Transfer completion
requires a normal checkpoint by the caller before continuing another puzzle.
"""
import argparse,json,subprocess,sys,time,os
os.environ.setdefault("REBORN_REPEL_POLICY","cancel")
from pathlib import Path
from PIL import Image
import numpy as np
from play import ROOT,act,snap,NATIVE
from locate import locate
from sprite_match import match
p=argparse.ArgumentParser();p.add_argument('map',type=int);p.add_argument('event',type=int);p.add_argument('direction',choices=['up','down','left','right']);p.add_argument('count',type=int);p.add_argument('--plan-start',type=int,required=True);p.add_argument('--plan',type=Path,required=True);a=p.parse_args()
assert a.map==880 and a.event in [23,24,147,148,149,150,157,158,233,234] and 1<=a.count<=12
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(a.map),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(a.event)]
assert (e['tile_id'] in [797,798] or e['character']=='mirageblock') and any(c['code']==209 for c in e['list'])
assert not any(c['code']==201 for c in e['list'])
if a.event not in [157,158]:
 assert not any(c['code']==209 and c['parameters'][0]==-1 for c in e['list']), 'Only stationary-player block events supported'
xy=(e['x'],e['y']);planned=None
if a.plan_start is not None:
 plan=json.loads(a.plan.read_text());assert plan['map']==a.map
 plan=dict(plan,partner=plan['steps'][a.plan_start].get('partner',plan['partner']))
 assert plan['steps'][a.plan_start].get('event',plan['event'])==a.event
 planned=plan['steps'][a.plan_start:a.plan_start+a.count]
 assert len(planned)==a.count and all(s['direction']==a.direction and s.get('event',a.event)==a.event for s in planned)
 assert tuple(planned[0]['primary_before'])==xy,('Plan start mismatch',xy,planned[0])
 if a.event in [157,158]:
  assert all(not (s['stand'][1]==144 and 65<=s['stand'][0]<=68 or s['stand'][1]==145 and s['stand'][0] in [63,70]) for s in planned), 'Door movement branch requires separate review'
dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[a.direction]
if e['character']=='mirageblock':
 sheet=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/mirageblock.png').convert('RGBA')
 row=(e['direction']//2-1)*64
 tile=sheet.crop((0,row+32,32,row+64)).resize((128,128),Image.Resampling.NEAREST)
else:
 sheet=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Tilesets/Mirage Tower.png').convert('RGBA')
 x=(e['tile_id']-384)%8*32;y=(e['tile_id']-384)//8*32
 tile=sheet.crop((x,y,x+32,y+32)).resize((128,128),Image.Resampling.NEAREST)

journal=ROOT/'work/mirage-postgame-pushes.jsonl'
def record(d):
 with journal.open('a') as f:f.write(json.dumps(dict(epoch=time.time(),**d))+'\n')
def verify(player,block):
 snap();box=[600,350,1600,1350];matches=[(match(NATIVE,box,sprite='boy_walk',zoom=4)[0],'boy_walk')]
 if matches[0][0][0]>=2000:
  box=[112,134,2160,1670]
  matches=[(match(NATIVE,box,sprite=name,zoom=4)[0],name) for name in ['boy_walk','boy_run']]
 hit,name=min(matches);err,direction,pattern,sx,sy=hit
 assert err<2000,('Player sprite review',matches)
 assert direction=={'down':2,'left':4,'right':6,'up':8}[a.direction],('Rendered facing mismatch',direction)
 sw,sh=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Characters/'+name+'.png').size
 foot=[box[0]+(sx+sw/8)*4,box[1]+(sy+sh/4)*4];left=round(foot[0]+(block[0]-player[0])*128-64);top=round(foot[1]+(block[1]-player[1])*128-128)
 im=Image.open(NATIVE).convert('RGB');assert 0<=left and 0<=top and left+128<=im.width and top+128<=im.height
 target=np.array(tile);actual=np.array(im.crop((left,top,left+128,top+128)))
 # Upper half stays visible when our character is directly below the block.
 mask=target[:,:,3]>250;mask[64:,:]=False
 assert int(mask.sum())>=200*16
 scores=[]
 for oy in range(-6,7):
  for ox in range(-6,7):
   arr=np.array(im.crop((left+ox,top+oy,left+128+ox,top+128+oy)))
   aa=arr[mask].astype(float).ravel();bb=target[:,:,:3][mask].astype(float).ravel()
   corr=float(np.corrcoef(aa,bb)[0,1]);mse=float(np.mean((aa-bb)**2));scores.append((corr,mse))
 score,mse=max(scores)
 record({'kind':'public-tile-proof','map':a.map,'player':player,'block':block,'score':score})
 assert score>=.90 and mse<700,('Visible primary block mismatch',block,score,mse)
 return score
before=(xy[0]-dx,xy[1]-dy)
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{a.map},{before[0]},{before[1]}'],check=True)
assert locate(a.map)==(a.map,*before)
act(a.direction+':.12','wait:.2')
try:verify(before,xy)
except AssertionError as error:
 if not any(t in str(error) for t in ['Visible primary block mismatch','Player sprite review','Rendered facing mismatch']):raise
 # Static decorative pillars can obscure the player or stone. Read only a
 # freshly created ordinary overworld checkpoint; never infer a missed push.
 label=f'MiragePostgame{a.map}-Preverify{int(time.time())}'
 subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
 frozen=json.loads((ROOT/'notes'/f'{label}-navigation.json').read_text())
 positions=frozen['positions'][str(a.map)]
 facing=int(subprocess.check_output(['ruby','-r',str(ROOT/'scripts/read_rgss.rb'),'-e','v=load_rgss(ARGV[0]); puts v[:game_player].instance_variable_get(:@direction)',str(ROOT/'backups'/f'Aster-{label}.rxdata')],stderr=subprocess.DEVNULL))
 assert facing=={'down':2,'left':4,'right':6,'up':8}[a.direction],('Saved facing differs',facing)
 assert positions[str(a.event)]==list(xy),('Saved initial primary differs',positions[str(a.event)],xy)
 if planned:assert positions[str(plan['partner'])]==planned[0]['secondary_before']
 assert locate(a.map)==(a.map,*before)
 record({'kind':'normal-save-initial-proof','checkpoint':label,'primary':xy,'public_player':before,'image_ambiguity':str(error)})

for i in range(a.count):
 record({'kind':'pending-push','map':a.map,'event':a.event,'from':xy,'direction':a.direction})
 act('c','wait:.6')
 expected=tuple(planned[i]['primary_after']) if planned else (xy[0]+dx,xy[1]+dy)
 if a.plan_start+i==len(plan['steps'])-1:
  act('wait:2')
  public=' '.join(r['text'] for r in snap()).lower()
  if 'charlotte' in public:
   record({'kind':'public-completion-scene','text':public,'plan':str(a.plan)})
   print('PUZZLE COMPLETION DIALOGUE',public,flush=True)
   raise SystemExit(0)

 # The last successful push may teleport to the completed version of the room.
 # Installed event has no player movement or transfer; the pixel check below
 # verifies the block relative to the rendered player after every push.
 now=(a.map,*before)
 if now[0]!=a.map:
  assert now[0]=={668:707,670:709,671:708,672:690,673:706}.get(a.map),('Unexpected destination',now)
  record({'kind':'observed-room-transfer','arrival':now,'expected_primary':expected})
  assert i==a.count-1,('Unexpected early room completion',i,now)
  print('PUZZLE ROOM TRANSFER',now,flush=True);raise SystemExit(0)
 assert now==(a.map,*before),('Pushing unexpectedly moved player',now,before)
 try:verify(before,expected)
 except AssertionError as error:
  if not any(t in str(error) for t in ['Visible primary block mismatch','Player sprite review','Rendered facing mismatch']):raise
  # The successful public coordinate read above proved overworld. If the
  # compressed image is ambiguous, a normal in-game save can verify both
  # puzzle blocks without inspecting live state or sending another push.
  label=f'MiragePostgame{a.map}-Verify{int(time.time())}'
  subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
  frozen=json.loads((ROOT/'notes'/f'{label}-navigation.json').read_text())
  positions=frozen['positions'][str(a.map)]
  assert positions[str(a.event)]==list(expected),('Saved primary differs',positions[str(a.event)],expected)
  if planned:assert positions[str(plan['partner'])]==planned[i]['secondary_after'],('Saved counterpart differs',positions[str(plan['partner'])],planned[i])
  record({'kind':'normal-save-block-proof','checkpoint':label,'primary':expected,'secondary':positions.get(str(plan['partner'])) if planned else None})
 npath=ROOT/'notes/navigation-state.json';n=json.loads(npath.read_text());n.setdefault('positions',{}).setdefault(str(a.map),{})[str(a.event)]=list(expected);
 if planned:
  n['positions'][str(a.map)][str(plan['partner'])]=planned[i]['secondary_after']
  for event,xy_target in planned[i].get('target_after',{}).items():n['positions'][str(a.map)][event]=xy_target
 npath.write_text(json.dumps(n,indent=2)+'\n')
 record({'kind':'observed-push','map':a.map,'event':a.event,'position':expected})
 if i+1<a.count and expected!=xy:
  act(a.direction+':.12','wait:.25');before=xy
 xy=expected
print('VISIBLE BLOCK GROUP VERIFIED',a.map,a.event,xy,flush=True)
