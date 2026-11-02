"""Approach a moving approved volunteer using screenshot sprite pixels and native coordinates."""
from nav import *
from locate import locate
from sprite_sensor import detect
import difflib,datetime
import play
# Same authorized CGEvent driver, shorter gaps; capture/usage guards remain active.
play.KEY=str(ROOT/'scripts/key_fast')
m,e=map(int,sys.argv[1:3]);review=json.loads((ROOT/'work/adrienn-volunteers-reviewed.json').read_text());assert any((r['map'],r['event'])==(m,e)for r in review)
source=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(m),str(e)],stderr=subprocess.DEVNULL));texts=[]
for pg in source['pages']:
 for c in pg['list']:
  if c['code']==101:texts.append(str(c['parameters'][0]))
  elif c['code']==401 and texts:texts[-1]+=' '+str(c['parameters'][0])
norm=lambda s:re.sub('[^a-z]','',s.lower().replace('Pokemon Reborn',''))
ledger=[];started=time.time()
for attempt in range(40):
 rows=snap();t=' '.join(r['text']for r in rows);low=t.lower()
 if any(r['y']>.72 and len(r['text'])>1 for r in rows)and any(difflib.SequenceMatcher(None,norm(t),norm(s)).ratio()>.65 or (len(norm(t))>=6 and norm(s).startswith(norm(t))) for s in texts):
  print('OBSERVED VOLUNTEER DIALOGUE READY',m,e,flush=True);break
 if re.search(r'found\s*\d+\s*coins',low):
  act('c','wait:.4');continue
 if re.search(r'\bhp\b|\bfight\b|pp:',low):
  if m in [570,531,533] and 'fight' in low and 'cofagrig' in low:
   subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(started)],check=True);continue
  raise SystemExit('NPC chase battle review: '+t)
 a,x,y=locate(m);assert a==m
 snap();v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(x),str(y)],stderr=subprocess.DEVNULL));target=v['events'][str(e)];char=target['character']
 tone=None
 if m in [527,524,530,520,543,551]:
  now=datetime.datetime.now();h=now.hour;f=now.minute/60
  tones={8:[5.3,-24,-10,0],9:[8.5,-13,-9,0],10:[5.7,-9,-8,0],11:[2.8,-4,-6,0],12:[0,0,0,0],13:[0,0,0,0],14:[0,0,0,0],15:[0,0,0,0],16:[-3,-7,-2,0],17:[-5,-9,-5,0]}
  assert h in tones and h+1 in tones,'Outdoor tint outside reviewed daytime range'
  tone=[a+(b-a)*f for a,b in zip(tones[h],tones[h+1])]
 players=detect(NATIVE,'boy_walk',tone=tone)
 if not players:
  # Arcade furniture can occlude the lower body; verify the visible head.
  assert Image.open(NATIVE).size==(2272,1816),'Window geometry changed; recalibrate before using the anchor'
  players=[p for p in detect(NATIVE,'boy_walk',head_only=True,tone=tone)if abs(p['foot'][0]-1136)<=8 and abs(p['foot'][1]-964)<=8]
  if len(players)==1:players[0]['foot']=[1136,964]
 assert len(players)==1,('Player sprite ambiguous',players)
 candidates=detect(NATIVE,char,tone=tone);pp=players[0]['foot'];seen=[]
 for c in candidates:
  dx,dy=(c['foot'][0]-pp[0])/128,(c['foot'][1]-pp[1])/128
  # A moving sprite may be between tiles; this is a nearest-tile route estimate.
  xy=(x+round(dx),y+round(dy))
  # A static identical sprite is excluded by its installed map tile.
  if any(int(k)!=e and q['character']==char and q.get('move_type')==0 and(q['x'],q['y'])==xy for k,q in v['events'].items()):continue
  seen.append((xy,c))
 if not seen:
  print('TARGET TEMPORARILY OCCLUDED; WAITING FOR VISIBLE PIXELS',flush=True);act('wait:.5');continue
 assert len(seen)==1,('Moving target sprite ambiguous',seen)
 (nx,ny),proof=seen[0];v['events'][str(e)].update(x=nx,y=ny);options=[]
 for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  try:path=route(v,(nx+dx,ny+dy));options.append((len(path),path,k))
  except ValueError:pass
 assert options,'No ordinary path to observed NPC'
 _,path,facing=min(options);keys=[k+':.08'for k in path[:3]]
 if len(path)<=3:keys += ['wait:.2',facing+':.03','c','wait:.4']
 ledger.append({'epoch':time.time(),'player':[x,y],'target':[nx,ny],'sprite':char,'confidence':proof['score'],'planned_keys':keys});(ROOT/'notes'/f'npc-chase-{m}-{e}.json').write_text(json.dumps(ledger,indent=2))
 print('SPRITE CHASE',m,e,'player',[x,y],'target',[nx,ny],'steps',len(path),flush=True)
 act(*keys)
else:raise SystemExit('NPC chase iteration bound')
