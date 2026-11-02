"""Resolve only preplanned move choices through normal menus."""
from play import *
import re,difflib
PLANS={'trick room':0,'dragon pulse':None,'thunder':None,'cross poison':1,'power split':None,'guard split':None,'shadow ball':1,'grudge':None,'mean look':None,'destiny bond':3,'signal beam':3,'earthquake':1,'hammer arm':None,'zap cannon':None,'wild charge':None,'solar beam':None,'gear grind':0,'magnetic flux':None,'strength':3,'mirror shot':1,'screech':None,'metal sound':None,'shift gear':3,'lock-on':None,'freeze-dry':3,'cotton guard':0,'sludge wave':3,'cut':3,'scary face':None,'extreme speed':0,'night slash':None,'sticky web':1,'earth power':2,'body slam':3,'recover':2,'rock smash':2,'charge beam':2,'charge':0,'take down':None,'electro ball':2,'confuse ray':0,'power gem':3,'thunder punch':2,'discharge':2,'light screen':0,'reflect':None,'flame burst':1,'agility':None,'retaliate':None,'flamethrower':1,'protect':3,'air slash':1,'muddy water':2,'crunch':2,'endeavor':None,'mirror coat':None,'psychic':3,'amnesia':None,'future sight':None,'slash':None,'fell stinger':3,'taunt':None,'reversal':None,'aura sphere':None}
PLANS.update({'wide guard':1,'fake out':2,'sheer cold':None,'bug buzz':None,'perish song':3,'waterfall':0})
PLANS.update({'hyper beam':None,'horn drill':None,'mega drain':0,'rock slide':None,'rock climb':3})
PLANS.update({'curse':None})
PLANS.update({'explosion':None})
def resolve(text):
 clean=' '.join(text.lower().split()).replace('rertaliate','retaliate')
 compact=''.join(clean.split())
 plans=dict(PLANS)
 if 'comfey' in clean:
  # Terrain-gate support build: retain Grass Knot and Synthesis.
  plans.update({'petal dance':None,'aromatherapy':2,'grassy terrain':0,'play rough':None})
 if any(n in clean for n in ('fennekin', 'braixen', 'delphox')):
  # The WTC gift's fourth slot is Psychic Terrain; never overwrite it.
  plans.update({'psybeam':0,'fire spin':None,'lucky chant':None,
                'light screen':None,'psyshock':0,'flamethrower':1,
                'will-o-wisp':2,'psychic':0,'sunny day':None,
                'magic room':None,'fire blast':None,'mystical fire':None,
                'future sight':None,'shadow ball':None,'role play':None,
                'switcheroo':None})
 if 'walrein' in clean:
  # This utility carrier must retain Blizzard, Dive, Surf, and Rest.
  plans['ice fang']=None
 if '--expected-move' in sys.argv:
  expected=sys.argv[sys.argv.index('--expected-move')+1].lower()
  replacement=int(sys.argv[sys.argv.index('--replace-slot')+1]);assert 0<=replacement<=3
  plans[expected]=replacement
 if 'altaria' in clean or 'swablu' in clean:
  plans.update({'dragon breath':None,'dragonbreath':None,'sky attack':None,'perish song':2,'moonblast':3})
 if 'honedge' in clean or 'doublade' in clean:
  plans.update({'iron defense':None,'power trick':None,'night slash':None,'iron head':0,'sacred sword':1})
 if 'gyarados' in clean:
  plans.update({'dragon rage':None,'hydro pump':None,'crunch':2,'dragon dance':3,'hurricane':None,'rain dance':None,'hyper beam':None})
 matches=sorted([(n,i) for n,i in plans.items() if ('learn'+n.replace(' ','')) in compact],key=lambda a:len(a[0]),reverse=True)
 if not matches:
  # Stop at the OCR line boundary so party labels/levels are not appended to
  # a slightly misread move name (e.g. "learnklaterfall" followed by "Lv.75").
  m=re.search(r'learn(?!ed\b)[ \t]*([a-z -]+)',text.lower())
  if m:
   attempted=m[1].replace(' ','').strip()
   ranked=sorted([(difflib.SequenceMatcher(None,attempted,n.replace(' ','')).ratio(),n,i) for n,i in plans.items()],reverse=True)
   if ranked[0][0]>=.83:matches=[(ranked[0][1],ranked[0][2])]
 if not matches:return False
 name,idx=matches[0]
 # Bag teaching also shows other party names; only match the learning actor.
 if re.search(r'excadrill is trying to',clean) and name=='earthquake':idx=0
 if re.search(r'excadrill is trying to',clean) and name=='rock slide':idx=2
 if name in ['crunch','fell stinger'] and 'drapion is trying to' in clean:idx=None
 if name=='rock smash':
  actor=re.search(r'(drapion|nidoqueen) is trying to',clean)
  if actor:idx=3 if actor[1]=='drapion' else 1
 if name=='confuse ray' and ('hexan' in clean or 'cryogonal' in clean):idx=None
 if '--expected-move' in sys.argv:
  expected=sys.argv[sys.argv.index('--expected-move')+1].lower()
  assert name==expected, ('Unexpected learning move',name,expected)
  idx=int(sys.argv[sys.argv.index('--replace-slot')+1]);assert 0<=idx<=3
 print('PLANNED MOVE',name,'replace',idx,flush=True)
 if idx is None:
  act('c','wait:0.5','c','wait:0.5','x','wait:0.5','c','wait:0.5','c','wait:0.5')
 else:
  # Observe each prompt: fast-key batches can skip a confirmation frame.
  for _ in range(14):
   screen=read().lower()
   if any(word in screen for word in ['power','accuracy','category']) and 'teachwhichmove' not in re.sub('[^a-z]','',screen):break
   rows=[line.strip(' •›>') for line in screen.splitlines()]
   if 'yes' in rows or 'no' in rows:
    assert any(word in ' '.join(screen.split()) for word in ['forget','delete','make room']),('Unexpected learning choice',screen)
    subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
   else:
    assert any(word in screen for word in ['learn','move','forget','delete','four','4']),('Learning dialogue review',screen)
    act('c','wait:.5')
  else:raise SystemExit('Learning grid timeout')
  act(*(['down:.12']*idx),'c','wait:.6')
  for _ in range(12):
   screen=read().lower()
   if 'learned' in screen:
    act('c','wait:.5');break
   assert not any(line.strip(' •›>') in ['yes','no'] for line in screen.splitlines()),('Unexpected post-selection choice',screen)
   act('c','wait:.5')
  else:raise SystemExit('Learning result timeout')
 print(read(),flush=True)
 return True
if __name__=='__main__':
 if not resolve(read()):raise SystemExit('Unknown learning state')
