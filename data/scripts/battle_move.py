"""Choose one move, optionally an explicitly planned enemy target, via normal UI."""
from play import *
from PIL import Image
import re
args=[x for x in sys.argv[1:] if x not in ['--watch','--mega']];foe_names=None
if '--foe-names' in args:
 i=args.index('--foe-names');foe_names=args[i+1].split(',');assert len(foe_names)==2;del args[i:i+2]
slot=int(args[0]);target=int(args[1]) if len(args)>1 else None
assert 0<=slot<=3 and target in [None,1,3]
command_rows=snap();t='\n'.join(v['text'] for v in command_rows).lower()
if 'fight' not in t:raise SystemExit('Expected battle command menu')
control=ROOT/'notes/battle-control.json'
if control.exists():
 expected=json.loads(control.read_text()).get('expected_foes')
 if expected:
  import difflib
  enemy=' '.join(v['text'].lower().translate(str.maketrans({'р':'p','у':'y','а':'a','о':'o','с':'c','е':'e','х':'x','к':'k','і':'i','ј':'j'})) for v in command_rows if v['y']<.37).replace('meougtic','meowstic').replace('meoustic','meowstic').replace('hron','aron')
  assert any(difflib.SequenceMatcher(None,n.lower(),w.strip('.,')).ratio()>=.78 for n in expected for w in enemy.split()),'Expected foe guard: '+enemy

# Command movement is clamped (Battle_Scene.pbCommandMenuEx); normalize
# directly so encounter movement cannot leave a stale Bag/Run selection.
act('left:0.22','up:0.22','c','wait:0.6')
t=read();print(t,flush=True)
grid_names=['rock slide','earthquake','surf','surt','protect','ice beam','freeze-dr','recouer','light screen','trick roon','trick room','shadon ball','destiny bond','extreme speed','crunch','flanethrouer','flamethrower','norning sun','morning sun','high jump kick','wide guard','hlide guard','lide guard','fake out','fake üut','u-turn']
grid_names += ['discharge','charge beam','charge bean','thunder wave','thunder laue','gear grind','mirror shot','shift gear','drill run','sandstorm','swords dance','waterfall','brick break']
if 'PP' not in t and not re.search(r'\d+\s*[,/]\s*[,/]?\s*\d+',t) and sum(n in t.lower()for n in grid_names)<2:raise SystemExit('Move grid review')
def cursor():
 im=Image.open(STATE).convert('RGB');w,h=im.size;s=[]
 for y in [0,1]:
  for x in [0,1]:
   box=(int(w*(.062 if x==0 else .392)),int(h*(.742 if y==0 else .834)),int(w*(.09 if x==0 else .42)),int(h*(.792 if y==0 else .888)))
   s.append(sum(min(p)>180 and max(p)-min(p)<75 for p in im.crop(box).getdata()))
 return max(range(4),key=lambda i:s[i])
c=cursor();seq=[]
if c%2!=slot%2:seq.append('right:0.12' if slot%2 else 'left:0.12')
if c//2!=slot//2:seq.append('down:0.12' if slot//2 else 'up:0.12')
if seq:act(*seq,'wait:0.2');snap()
if cursor()!=slot:raise SystemExit('Move cursor review')
if '--mega' in sys.argv:
 from mega_button import enable
 enable()
act('c:0.08','wait:0.6')
if target is not None:
 rtarget=snap()
 # Installed pbFirstTarget always starts at the first living opponent. When
 # slot1 has fainted, slot3 is already selected; LEFT would select our ally.
 def hud_present(lo,hi):
  return any(lo<v['y']<hi and (re.search(r'(?<![a-z])f?hp(?![a-z])',v['text'],re.I) or
   re.search(r'l[uvụ][.?\s]*\d{1,3}',v['text'],re.I))for v in rtarget)
 has1=hud_present(.08,.21);has3=hud_present(.21,.37)
 # Target selection blinks the selected HUD. No turn has advanced between
 # the verified command and this menu, so its living-opponent HUD is stable.
 rtarget=command_rows
 has1=has1 or hud_present(.08,.21);has3=has3 or hud_present(.21,.37)
 if foe_names:
  import difflib
  def observed_name(name,lo,hi):return any(v['x']<.45 and lo<v['y']<hi and difflib.SequenceMatcher(None,name.lower(),v['text'].lower()).ratio()>.8 for v in command_rows)
  has1=has1 or observed_name(foe_names[0],.08,.21);has3=has3 or observed_name(foe_names[1],.21,.37)
 first=1 if has1 else (3 if has3 else None)
 assert first is not None and ((target==1 and has1)or(target==3 and has3)), 'Requested enemy HUD needs review'
 act(*(['left:0.22','wait:0.3'] if target!=first else []),'c:0.12','wait:0.6')

if '--watch' in sys.argv and os.environ.get('REBORN_EXPECT_WILD_FINISH')=='1':
 assert os.environ.get('REBORN_FAST_CHEST_TRANSITION')=='1'
 from fast_chest_transition import finish
 watch_start=time.time()
 finish(timeout=60)
 from retain_tail import retain
 retain(epoch=watch_start,seconds=time.time()-watch_start+1)
 raise SystemExit(0)

if '--watch' in sys.argv:
 last='';blank=0;stable_caption='';stable_count=0
 for _ in range(20):
  t=read()
  if t!=last:print(t,flush=True);last=t
  # Enemy Mega-Evolution announcements can wait for confirmation. Advance
  # only this recognized caption after three identical public observations.
  compact_caption=' '.join(t.lower().split())
  stable_count=stable_count+1 if compact_caption==stable_caption else 1
  stable_caption=compact_caption
  if stable_count>=3 and 'reacting to' in compact_caption and ('mega' in compact_caption or ('foe' in compact_caption and 'ite' in compact_caption)):
   act('c','wait:.4');stable_count=0;continue
  if 'no pp left' in t.lower():
   act('c','wait:.3','x','wait:.3');raise SystemExit('Selected move exhausted; no battle action advanced')
  if 'trying to learn' in ' '.join(t.lower().split()):
   from learning import resolve
   if not resolve(t):raise SystemExit('Unplanned learning prompt: review required')
   continue
  leveltext=' '.join(t.lower().split())
  if re.search(r'\ble[vw]el\s*\d+\s*[!i]',leveltext) or 'max. hp' in leveltext or 'max.hp' in leveltext:
   act('c','wait:.2');continue
  imw=Image.open(STATE).convert('RGB');ww,hh=imw.size;bw=imw.crop((int(ww*.08),int(hh*.75),int(ww*.90),int(hh*.87)))
  world=not re.search(r'\bhp\b|\bfight\b|pp:',t.lower()) and sum(min(px)>235 and max(px)-min(px)<5 for px in bw.getdata())/(bw.width*bw.height)<.55
  blank=blank+1 if world or len(t.lower().replace('pokemon reborn','').strip())<10 else 0
  if blank>=2:
   if os.environ.get('REBORN_FAST_CHEST_TRANSITION')=='1':
    from fast_chest_transition import finish
    finish()
   break
  if any(w in t.lower() for w in ['fainted','destiny bond','trying to take its foe down']):
   from retain_tail import retain
   retain()
   if os.environ.get('REBORN_FAST_CHEST_TRANSITION')=='1' and 'wild' in t.lower() and 'fainted' in t.lower():
    from fast_chest_transition import finish
    finish()
   break
  if 'FIGHT' in t or 'Choose a Pok' in t or 'about to send in' in ' '.join(t.split()) or re.search(r'de.?feated',t,re.I) or ('CANCEL' in t and t.count('HP') >= 3):break
  act('wait:0.2')
else:
 act('wait:3');print(read(),flush=True)
