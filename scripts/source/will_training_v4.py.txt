"""Reviewed Friday Will v4 UI plan. No live battle-log/runtime inspection."""
from play import *
import difflib,re
began=json.loads((ROOT/'work/active-trainer-music.json').read_text())['start_epoch'];actor=sys.argv[1] if len(sys.argv)>1 else 'Cofagrigus';burned=actor!='Cofagrigus';screen=False;zard_tr=False

def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def named(text,names):
 words=re.findall('[a-z-]+',text.lower()); hits=[n for n in names if any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.78 for w in words)]
 assert len(hits)==1,('Ambiguous opponent',text,hits)
 return hits[0]
for phase in range(14):
 rows=snap();t=' '.join(v['text'] for v in rows);low=t.lower();print('PHASE',phase,actor,t,flush=True)
 if re.search(r'de.?feated|for winning',low):print('WILL VICTORY',flush=True);break
 forced='choose a pok' in low or ('cancel' in low and low.count('hp')>=5)
 offered='change pok' in low or 'switch your' in low
 if offered:
  incoming=None
  for line in (ROOT/'recordings/screens.jsonl').read_text().splitlines()[::-1]:
   v=json.loads(line)
   if v['epoch']<began:break
   msg=' '.join(v['text']).lower()
   if 'send in' in msg:
    incoming=named(msg.split('send in',1)[1],['Charizard','Sceptile','Gardevoir']);break
  if not incoming:
   from recent_incoming import recent_incoming
   incoming=recent_incoming(began,['Charizard','Sceptile','Gardevoir'])
  assert incoming,('Unknown incoming opponent',t)
  nxt={'Charizard':'Swampert','Sceptile':'Arcanine','Gardevoir':'Hexan'}[incoming]
  act('c','wait:.6');run('party_pick',nxt);actor=nxt;run('battle_ready');continue
 if forced:
  assert (actor=='Hexan' and screen) or actor=='Swampert',('Unexpected knockout',actor,t)
  nxt='Klinklang' if actor=='Hexan' else 'Cofagrigus'
  run('party_pick',nxt);actor=nxt;run('battle_ready');continue
 assert 'fight' in low and 'hp' in low and ('run' in low or 'what will' in low),('Battle requires review',t)
 foe=named(' '.join(v['text']for v in rows if v['y']<.37),['Swampert','Charizard','Sceptile','Gardevoir'])
 if foe=='Swampert':
  assert actor=='Cofagrigus'
  if not burned:run('battle_move',2,'--watch');burned=True
  run('battle_batch',actor,1,'--foes',foe,'--turns',6,'--watch','--heal-below',.38,'--heal-item','Ultra Potion','--min-hp',.15,'--stop-after-victory')
 elif foe=='Charizard':
  assert actor in ['Swampert','Cofagrigus']
  if actor=='Cofagrigus' and not zard_tr:run('battle_move',0,'--watch');zard_tr=True
  run('battle_batch',actor,2 if actor=='Swampert' else 1,'--foes',foe,'--turns',4,'--watch','--stop-after-victory')
 elif foe=='Sceptile':
  assert actor=='Arcanine'
  run('battle_batch',actor,1,'--foes',foe,'--turns',3,'--watch','--recover-below',.45,'--recover-slot',3,'--min-hp',.2,'--stop-after-victory')
 else:
  assert actor in ['Hexan','Klinklang']
  if actor=='Hexan':
   if not screen:run('battle_move',0,'--watch');screen=True
   run('battle_batch',actor,1,'--foes',foe,'--turns',3,'--watch','--stop-after-victory')
   current=read().lower()
   assert 'choose a pok' in current or ('cancel' in current and current.count('hp')>=5) or re.search(r'de.?feated|for winning',current),('Screen support needs review',current)
  else:run('battle_batch',actor,0,'--foes',foe,'--turns',1,'--watch','--stop-after-victory')
else:raise SystemExit('Will plan phase limit')
