"""Select, but never use, a named visible bag item; abort outside the bag."""
from play import *
# Let each list animation settle before another fast-driver arrow.
_play_act=act
def act(*keys):
 _play_act(*[v for k in keys for v in ((k,'wait:.09') if k.startswith(('up','down')) else (k,))])
from PIL import Image
import re,unicodedata,difflib
from bag_scan_policy import installed_stride_supported,viewport,transition,STRIDE
def ascii_name(s):return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
wanted=re.sub('[^a-z0-9]','',ascii_name(sys.argv[1]))
# Native save IDs use HMxx; Reborn displays these reusable machines as TMXn.
if re.fullmatch(r'hm0?\d+',wanted):wanted='tmx'+str(int(wanted[2:]))
seen=set()
single_step='--single-step' in sys.argv
stride_supported=installed_stride_supported() and not single_step
previous_stride=None
backfill_pending=False
memory_route_used=False
for _ in range(100):
 r=snap();txt=' '.join(v['text'] for v in r).lower()
 if not any(w in txt for w in ['sort','medicine','items','close','candy','repel','tmx','charge beam','rock smash']) and not re.search(r'\bt[mh][a-z0-9]',txt):raise SystemExit('Bag screen review')
 im=Image.open(STATE).convert('RGB');w,h=im.size
 ys=[]
 for y in range(int(h*.11),int(h*.66)):
  n=sum(rr>170 and gg<100 and bb<110 for rr,gg,bb in [im.getpixel((x,y)) for x in range(int(w*.43),int(w*.83),3)])
  if n>int(w*.40/3)*.6:ys.append(y/h)
 if not ys:raise SystemExit('Bag cursor review')
 center=(min(ys)+max(ys))/2
 names=[v for v in r if .36<v['x']<.75 and .055<v['y']<.66
        and not re.fullmatch(r'(?:[x×]\s*[0-9Il|]+|\d+)',v['text'].strip(),re.I)]
 if not names:raise SystemExit('Bag visible name rows missing')
 current=min(names,key=lambda v:abs(v['y']+v['h']/2-center))
 if abs(current['y']+current['h']/2-center)>.0355:raise SystemExit('Bag selected-name/cursor alignment review')
 def norm(s):
  value=re.sub('[^a-z0-9]','',ascii_name(s)).replace('hwakening','awakening').replace('antidate','antidote').replace('lemanade','lemonade').replace('buickball','quickball').replace('expcandu','expcandy').replace('incenze','incense').replace('tellurie','telluric').replace('kelpey','kelpsy').replace('pouer','power').replace('powerkeight','powerweight')
  # Session370 native frames: TM80 Rock Slide repeatedly OCRs as THOU ROCKSIDE.
  # Require the distinctive move label as well as a machine-like prefix.
  if wanted=='tm80' and re.fullmatch(r't[mhn][a-z0-9]*(?:rockslide|rockside)',value):return wanted
  if wanted=='zinc' and value=='zine':return wanted # Visually reviewed session278.
  if wanted=='evtuner' and value=='eytuner':return wanted
  if wanted=='expcandyxl' and re.fullmatch(r'expcandy[a-z]l',value):return wanted
  if wanted in ('tmx5','tmx5waterfall') and re.fullmatch(r't[mhn][a-z0-9]+waterfall',value):return wanted
  if wanted=='tmx6dive' and value.startswith('t') and value.endswith('dive'):return wanted
  if wanted in ('hm02','tmx2fly') and re.fullmatch(r't[mhn][a-z0-9]+fly',value):return wanted
  if value.startswith('th'):value='tm'+value[2:]
  if value.startswith(('tmn','tma')):value='tmx'+value[3:]
  if wanted=='xaccuracy' and value in {'accuracy','xaccuracy','kaccuracy','naccuracy','aaccuracy','arccuracy','xarccuracy','ahccuracu','arecuracy','arccuracu'}:return wanted
  if wanted=='xspatk' and re.fullmatch(r'[akmnx]?sp[ah]tk',value):return wanted
  if wanted=='xspdef' and re.fullmatch(r'[akmnx]?spd(?:e|er)f',value):return wanted
  if wanted=='xspeed' and re.fullmatch(r'[akmnx]?speed',value):return wanted
  if wanted=='xdefend' and re.fullmatch(r'[ahkmnx]?defend',value):return wanted
  if wanted=='xattack' and re.fullmatch(r'[akmnx]?attack',value):return wanted
  return {'defend':'xdefend','kdefend':'xdefend','ndefend':'xdefend','kspdef':'xspdef'}.get(value,value)
 # Reuse only previously rendered medicine row adjacency to choose a shorter
 # direction. Every move is reobserved; actual selection still requires the
 # existing exact rendered-name check. Stale adjacency can only move a cursor.
 def memo_norm(label):
  label=norm(label)
  if re.fullmatch(r'tmx?\d+',wanted):
   if label=='closebag':return label
   machine=re.match(r'tmx?\d+',label)
   return machine.group() if machine else None
  label={'zine':'zinc','pplp':'ppup'}.get(label,label)
  known=['burnheal','antidote','paralyzeheal','awakening','poprocks','fullheal','xaccuracy','xattack','xspdef','revive','ppup','zinc','swiftwing','maxelixir','maxether','protein','fullrestore','expcandyxl','xdefend','xspatk','xspeed','ultrapotion','maxpotion','bubbletea','evtuner','closebag']
  if label in known:return label
  match=difflib.get_close_matches(label,known,n=1,cutoff=.78)
  return match[0] if match else None
 machine_pocket=bool(re.fullmatch(r'tmx?\d+',wanted))
 memory_path=ROOT/'work'/('bag-visible-machine-adjacency.json' if machine_pocket else 'bag-visible-adjacency-v2.json')
 memory={}
 if machine_pocket or any(z in txt for z in ['medicine','medieine','nedicine']):
  try:memory=json.loads(memory_path.read_text())
  except (OSError,ValueError):pass
  ordered=sorted(names,key=lambda z:z['y'])
  for first,second in zip(ordered,ordered[1:]):
   if .055 < second['y']-first['y'] < .087:
    one,two=memo_norm(first['text']),memo_norm(second['text'])
    if one and two and one!=two:
     memory.setdefault(one,{})['down']=two
     memory.setdefault(two,{})['up']=one
  memory_path.write_text(json.dumps(memory))
 print('SELECTED',current['text'],flush=True)
 def matches(s):
  n=norm(s)
  # X/Y Mega Stones differ by a meaningful final letter; fuzzy OCR must
  # never select the other form even when the rest of the name matches.
  if wanted in ('mewtwonitex','mewtwonitey','charizarditex','charizarditey'):
   return n.endswith(wanted[-1]) and difflib.SequenceMatcher(None,n[:-1],wanted[:-1]).ratio()>=.85
  # The visible machine row includes its move name (TM20 Safeguard).
  # Compare the complete numeric identifier so TM2 cannot match TM20.
  if re.fullmatch(r'tmx?\d+',wanted):
   identifier=re.match(r'tmx?\d+',n)
   if identifier and identifier.group()==wanted:return True
  return n==wanted or (len(wanted)>=9 and difflib.SequenceMatcher(None,n,wanted).ratio()>=.9)
 if matches(current['text']):break
 target=next((v for v in names if matches(v['text'])),None)
 if target:
  n=round((target['y']-current['y'])/(h and .071));n=max(-7,min(7,n))
  if not n:raise SystemExit('Bag target alignment review')
  act(*([('down:.18' if n>0 else 'up:.18') if single_step else ('down' if n>0 else 'up')]*abs(n)),'wait:0.3')
 else:
  # Search the observed adjacency graph; never invent hidden row indices.
  frontier=[(memo_norm(current['text']),[])];visited=set();route=None
  while frontier:
   node,path=frontier.pop(0)
   if node==wanted:route=path;break
   if node in visited or len(path)>=40:continue
   visited.add(node)
   for direction,nxt in memory.get(node,{}).items():
    frontier.append((nxt,path+[direction]))
  memory_signature=(norm(current['text']),tuple(norm(v['text']) for v in names),'memory')
  if route and not memory_route_used and len(set(route))==1 and memory_signature not in seen and '--no-memory' not in sys.argv and os.environ.get('REBORN_BAG_NO_MEMORY')!='1':
   memory_route_used=True
   seen.add(memory_signature)
   bounded=route[:1 if single_step else 4]
   print('OBSERVED BAG ROUTE',bounded,flush=True)
   act(*[v+':.12' for v in bounded],'wait:.3')
   previous_stride=None;backfill_pending=False
   continue
  view=viewport(names,current,norm)
  if backfill_pending:
   if view is None or not view['tail_visible']:
    # Current selection is still visually verified. Restart a complete
    # one-row scan instead of assuming the uncertain stride covered rows.
    stride_supported=False;single_step=True;seen.clear();previous_stride=None
    backfill_pending=False
    print('BAG WRAP OCR UNCERTAIN; restarting verified one-row scan',flush=True)
   else:
    backfill_pending=False
    previous_stride=view
    print('BAG WRAP TAIL VERIFIED; returning to first page',flush=True)
    act(*(['down:.12']*STRIDE),'wait:0.3');continue
  if previous_stride is not None:
   state=transition(previous_stride,view)
   previous_stride=None
   if state=='uncertain':
    stride_supported=False;single_step=True;seen.clear()
    print('BAG STRIDE OCR UNCERTAIN; restarting verified one-row scan',flush=True)
   if state=='backfill-tail':
    # Four separate normal taps can wrap past unseen final rows. Reverse the
    # bounded stride; source scrolling leaves the last seven rows visible.
    # The next capture must show CLOSE BAG, never guessed hidden item data.
    backfill_pending=True
    print('BAG POSSIBLE WRAP; inspecting skipped tail before continuing',flush=True)
    act(*(['up:.12']*STRIDE),'wait:0.3');continue
  signature=(current['text'],tuple(v['text'] for v in names))
  if signature in seen:
   print('Complete visible bag cycle: item not found',flush=True)
   raise SystemExit(4)
  seen.add(signature)
  step=STRIDE if stride_supported and view is not None else 1
  previous_stride=view if step==STRIDE else None
  print('BAG VISIBLE-ONLY SCAN',step,'rows',flush=True)
  act(*(['down:.12']*step) if step==STRIDE else ['down:.18' if single_step else 'down'],'wait:0.3')
else:raise SystemExit('Bag scan limit')
