"""Bounded Sunday Fawkes v4 plan from installed roster and public battle UI."""
from play import *
import difflib,re
began=json.loads((ROOT/'work/active-trainer-music.json').read_text())['start_epoch']
actor=sys.argv[1] if len(sys.argv)>1 else 'Swampert'
names=['Dragalge','Aegislash','Typhlosion','Greninja']
matchups={'Dragalge':('Swampert',1),'Aegislash':('Volcanion',1),'Typhlosion':('Swampert',1),'Greninja':('Zapdos',1)}
mega='--mega-already' in sys.argv

def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def named(t):
 hits=[n for n in names if any(difflib.SequenceMatcher(None,n.lower(),w.lower()).ratio()>=.8 for w in re.findall('[A-Za-z]+',t))]
 assert len(hits)==1,('Opponent ambiguity',t,hits)
 return hits[0]
for phase in range(16):
 rows=snap();t=' '.join(v['text'] for v in rows);low=t.lower();print('FAWKES PHASE',phase,actor,t,flush=True)
 if re.search(r'de.?feated|for winning',low):print('FAWKES VICTORY',flush=True);break
 if 'change pok' in low or 'switch your' in low:
  from recent_incoming import recent_incoming
  foe=None
  for line in (ROOT/'recordings/screens.jsonl').read_text().splitlines()[::-1]:
   v=json.loads(line)
   if v['epoch']<began:break
   msg=' '.join(v['text']).lower()
   if 'send in' in msg:
    foe=named(msg.split('send in',1)[1]);break
  if foe is None:foe=recent_incoming(began,names)
  assert foe in matchups,('Incoming review',foe)
  nxt=matchups[foe][0]
  if nxt==actor:act('x','wait:.5')
  else:act('c','wait:1.2');run('party_pick',nxt);actor=nxt
  run('battle_ready');continue
 assert 'fight' in low and 'hp' in low,('Battle needs review',t)
 prompt=' '.join(v['text'] for v in rows if v['y']>.72 and v['x']<.5)
 assert any(difflib.SequenceMatcher(None,actor.lower(),w.lower()).ratio()>=.78 for w in re.findall('[A-Za-z]+',prompt)),('Active actor differs from training plan',actor,prompt)
 foe=named(' '.join(v['text'] for v in rows if v['y']<.37))
 expected,slot=matchups[foe];assert actor==expected,('Unexpected matchup',actor,foe)
 if actor=='Mawile' and not mega:
  run('battle_move',slot,'--mega','--watch');mega=True
  run('battle_batch',actor,slot,'--foes',','.join(names),'--turns',0,'--watch','--stop-after-victory')
 else:
  run('battle_batch',actor,slot,'--foes',foe,'--turns',4,'--watch','--min-hp',.30,'--stop-after-victory')
else:raise SystemExit('Fawkes phase limit')
