"""Bounded Friday Will v4 plan for the 115+ postgame party from installed roster and public battle UI."""
from play import *
import difflib,re
began=json.loads((ROOT/'work/active-trainer-music.json').read_text())['start_epoch']
actor=sys.argv[1] if len(sys.argv)>1 else 'Amoonguss'
names=['Swampert','Sceptile','Charizard','Gardevoir']
matchups={'Swampert':('Amoonguss',2),'Sceptile':('Zapdos',0),'Charizard':('Zapdos',1),'Gardevoir':('Mawile',1)}
if os.environ.get('REBORN_WILL_GARDEVOIR_ZAPDOS')=='1':
 # Installed Will v4 Gardevoir85: Hyper Voice/Psyshock/Focus Blast/Calm Mind.
 # Reviewed Zapdos120 has Discharge1 and Roost2; avoids a PC trip for Mawile.
 matchups['Gardevoir']=('Zapdos',1)
mega=False

def run(s,*args):
 before=(ROOT/'recordings/actions.jsonl').stat().st_mtime_ns
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
 if s=='battle_batch' and (ROOT/'recordings/actions.jsonl').stat().st_mtime_ns==before:
  raise SystemExit('Battle helper requested review without choosing an action; do not repeat unchanged state')
def named(t):
 hits=[n for n in names if any(difflib.SequenceMatcher(None,n.lower(),w.lower()).ratio()>=.8 for w in re.findall('[A-Za-z]+',t))]
 assert len(hits)==1,('Opponent ambiguity',t,hits)
 return hits[0]
for phase in range(16):
 rows=snap();t=' '.join(v['text'] for v in rows);low=t.lower();print('WILL PHASE',phase,actor,t,flush=True)
 if re.search(r'de.?feated|for winning',low):print('WILL VICTORY',flush=True);break
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
 if foe=='Swampert' and actor=='Amoonguss' and any(z in low for z in ['frz','fref','frozen']):
  # Public Ice Punch freeze: preserve Amoonguss via Regenerator and use the
  # healthy Levitate Cresselia's Psychic against this lower-level Swampert.
  run('battle_switch','Cresselia');actor='Cresselia';matchups['Swampert']=('Cresselia',1)
  run('battle_ready');continue
 expected,slot=matchups[foe];assert actor==expected,('Unexpected matchup',actor,foe)
 if actor=='Mawile' and not mega:
  run('battle_move',slot,'--mega','--watch');mega=True;run('battle_ready')
 else:
  # Zapdos120 is faster and Discharge should 2HKO. A .60 threshold can
  # repeatedly Roost from the same post-Hyper-Voice HP instead of finishing.
  recovery=['--recover-below',.45,'--recover-slot',2] if foe=='Gardevoir' and actor=='Zapdos' else []
  run('battle_batch',actor,slot,'--foes',foe,'--turns',4,'--watch','--min-hp',.30,'--stop-after-victory',*recovery)
else:raise SystemExit('Will phase limit')
