"""Bounded normal-UI policy for the reviewed Friday Will version4 team.

Never inspects live AI logs. Requires the established five-member core and an
Arcanine lead. Accepts losses; all attempts remain in the journey recording.
"""
from play import *
import difflib

foes=['Swampert','Gardevoir','Charizard','Sceptile']
party=['Arcanine','Mienshao','Swampert','Klinklang','Ampharos','Drilbur']
statepath=ROOT/'work/will-practice-state.json'
saved=json.loads(statepath.read_text()) if '--resume' in sys.argv else {}
counts={tuple(k.split('|')):v for k,v in saved.get('counts',{}).items()};opener=saved.get('opener',False);foe=saved.get('foe','Swampert');actor=saved.get('actor','Arcanine');limit=time.time()+900

def run(script,*args):
 print('POLICY',script,*args,flush=True)
 rc=subprocess.call([sys.executable,str(ROOT/'scripts'/(script+'.py')),*map(str,args)])
 if rc and script=='battle_ready':
  current=read().lower()
  if 'change pok' in current or 'switch your' in current:return
 if rc:raise SystemExit('Helper stopped for review: '+script)

def name_in(text,names):
 text=text.lower().replace('klink lang','klinklang').replace('suampert','swampert')
 scores=[(max([difflib.SequenceMatcher(None,n.lower(),w.strip('.,!?')).ratio() for w in text.split()] or [0]),n) for n in names]
 score,n=max(scores)
 return n if score>=.78 else None

def move(slot):run('battle_move',slot,'--watch')

for turn in range(60):
 assert time.time()<limit,'Practice time budget reached; inspect current UI'
 rows=snap();t='\n'.join(v['text']for v in rows);low=t.lower()
 statepath.write_text(json.dumps({'counts':{'|'.join(k):v for k,v in counts.items()},'opener':opener,'foe':foe,'actor':actor,'epoch':time.time()},indent=2))
 print('STATE',turn,t.replace('\n',' | '),flush=True)
 if re.search(r'de.?feated|for winning',low):
  print('VICTORY ANCHOR',flush=True);break
 if 'out of usable' in low or 'blacked out' in low:
  raise SystemExit('Practice loss: keep recording and review recovery')
 if 'trying to learn' in low:
  run('learning');continue
 if re.search(r'\ble[vw]el\s*\d+\s*[!i]', ' '.join(low.split())) or 'max. hp' in low or 'max.hp' in low:
  act('c:0.08','wait:.3');continue
 if 'about to send in' in ' '.join(low.split()) or 'change pok' in low:
  nextfoe=name_in(' '.join(v['text']for v in rows if v['y']>.72),foes)
  if not nextfoe:
   recent=[json.loads(l) for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()][-60:]
   hint=next((r for r in reversed(recent) if 'about to send in' in ' '.join(r['text']).lower()),None)
   if hint:nextfoe=name_in(' '.join(hint['text']).lower().split('about to send in',1)[1],foes)
  assert nextfoe,'Next foe needs review'
  foe=nextfoe
  wanted={'Gardevoir':'Ampharos','Charizard':'Klinklang' if counts.get(('Ampharos','Gardevoir'),0)>0 else 'Ampharos','Sceptile':'Arcanine'}.get(foe)
  assert wanted,'Unexpected free-switch foe'
  if wanted==actor:run('choose_dialog','Yes|No','No');run('battle_ready')
  else:run('battle_switch',wanted);actor=wanted
  continue
 if 'cancel' in low and low.count('hp')>=5:
  wanted={'Swampert':'Swampert' if actor=='Mienshao' else 'Arcanine','Gardevoir':'Klinklang' if actor=='Ampharos' else 'Ampharos','Charizard':'Ampharos' if actor=='Klinklang' else 'Arcanine','Sceptile':'Arcanine'}[foe]
  run('party_pick',wanted);actor=wanted;continue
 if 'fight' not in low:
  run('battle_ready');continue
 actor=name_in(' '.join(v['text']for v in rows if v['y']>.72 and v['x']<.5),party)
 enemy=name_in(' '.join(v['text']for v in rows if v['y']<.37),foes)
 assert actor and enemy,('Command matchup needs review',t)
 foe=enemy;key=(actor,foe);n=counts.get(key,0);counts[key]=n+1
 assert n<7,'Matchup action budget reached'
 if foe=='Swampert':
  if actor=='Arcanine' and not opener:
   opener=True;run('battle_switch','Mienshao');actor='Mienshao'
  elif actor=='Mienshao':move(2 if n==0 else 0)
  elif actor=='Swampert':move(1)
  elif actor=='Arcanine':move(0)
  else:raise SystemExit('Swampert actor review')
 elif foe=='Gardevoir':
  if actor=='Ampharos':
   if n==0:move(0)
   elif n==1:move(1)
   else:run('battle_switch','Klinklang');actor='Klinklang'
  elif actor=='Klinklang':move(0)
  else:raise SystemExit('Gardevoir actor review')
 elif foe=='Charizard':
  if actor=='Klinklang':
   if n==0:run('battle_item','Hyper Potion','Ampharos')
   else:move(0)
  elif actor=='Ampharos':move(1 if n==0 else 2)
  elif actor=='Arcanine':move(0)
  else:raise SystemExit('Charizard actor review')
 elif foe=='Sceptile':
  assert actor=='Arcanine','Sceptile actor review'
  hp=re.search(r'(\d+)\s*/\s*(\d+)',t)
  assert hp,'Arcanine HP needs review'
  move(3 if int(hp[1])<140 else 1)
else:raise SystemExit('Practice action budget reached')
