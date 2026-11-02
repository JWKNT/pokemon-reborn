"""Bounded Thursday JB v4 plan from installed roster and public battle UI."""
from play import *
import difflib,re
began=json.loads((ROOT/'work/active-trainer-music.json').read_text())['start_epoch']
actor=sys.argv[1] if len(sys.argv)>1 else 'Zapdos'
names=['Greninja','Delphox','Chesnaught','Goodra']
matchups={'Greninja':('Zapdos',1),'Delphox':('Swampert',0),'Chesnaught':('Zapdos',0),'Goodra':('Mawile',0)}
mega=False

def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def named(t):
 hits=[n for n in names if any(difflib.SequenceMatcher(None,n.lower(),w.lower()).ratio()>=.8 for w in re.findall('[A-Za-z]+',t))]
 assert len(hits)==1,('Opponent ambiguity',t,hits)
 return hits[0]
for phase in range(16):
 rows=snap();t=' '.join(v['text'] for v in rows);low=t.lower();print('JB PHASE',phase,actor,t,flush=True)
 if re.search(r'de.?feated|for winning',low):print('JB VICTORY',flush=True);break
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
 foe=named(' '.join(v['text'] for v in rows if v['y']<.37))
 expected,slot=matchups[foe];assert actor==expected,('Unexpected matchup',actor,foe)
 if actor=='Mawile' and not mega:
  run('battle_move',slot,'--mega','--watch');mega=True;run('battle_ready')
 else:
  run('battle_batch',actor,slot,'--foes',foe,'--turns',4,'--watch','--min-hp',.30,'--stop-after-victory')
else:raise SystemExit('JB phase limit')
