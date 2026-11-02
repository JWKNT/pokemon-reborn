"""Reviewed Indra matchups; UI-only, bounded, stops for difficult normal tanks."""
from play import *
import re,difflib
plan={
 'scizor':('Arcanine',1),'talonflame':('Ampharos',2),'porygon-z':('Mienshao',0),
 'empoleon':('Mienshao',0),'simipour':('Ampharos',2),'wailord':('Ampharos',2),
 'ribombee':('Arcanine',1),'ninjask':('Arcanine',0),'dedenne':('Swampert',2),
 'hawlucha':('Swoobat',3),'lilligant':('Arcanine',1),'flygon':('Swampert',2),
 'toucannon':('Ampharos',2),'dusknoir':('Cofagrigus',1),
 'dragonite':('Cofagrigus',1),'ursaring':('Mienshao',0),'snorlax':('Mienshao',0),'blissey':('Mienshao',0),'sawsbuck':('Arcanine',1),
 'tsareena':('Arcanine',1),'mismagius':('Arcanine',2),'mienshao':('Cofagrigus',1),
 'carbink':('Swampert',2),'klinklang':('Mienshao',0),'donphan':('Swampert',2),
 'castform':('Mienshao',0),'swanna':('Ampharos',2),'amoonguss':('Arcanine',1),
 'musharna':('Arcanine',2),'bewear':('Arcanine',1)}
def run(s,*a):
 p=subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],capture_output=True,text=True)
 print(p.stdout,flush=True)
 if p.returncode:raise SystemExit(p.stderr or 'Helper review')
 return p.stdout
for stage in range(20):
 t=read().lower()
 if 'fight' not in t and not any(z in t for z in ['change pok','switch your','choose a pok']):
  run('battle_batch','Arcanine',0,'--foes',','.join(plan),'--turns',0)
  t=read().lower()
 r=snap();foe=' '.join(x['text'].lower() for x in r if x['y']<.37)
 match=[n for n in plan if n.replace('-','') in re.sub('[^a-z]','',foe)]
 if not match:match=[n for n in plan if any(difflib.SequenceMatcher(None,n,w.strip('.,!?')).ratio()>=.8 for w in foe.split())]
 if len(match)!=1:raise SystemExit('Indra matchup review: '+foe)
 n=match[0];actor,slot=plan[n]
 if n=='porygon-z':raise SystemExit('Specs Porygon-Z: full Cofagrigus Destiny Bond trade required; never paid Mienshao switch')
 if n=='musharna':raise SystemExit('Musharna: reviewed Trick Room/Destiny Bond trade required')
 if n=='amoonguss':raise SystemExit('Amoonguss: reviewed Calm Mind/status cure plan required')
 prompt=' '.join(x['text'].lower() for x in r if x['y']>.72)
 if not any(difflib.SequenceMatcher(None,actor.lower(),w.strip('.,!?')).ratio()>=.78 for w in prompt.split()):run('battle_switch',actor)
 if n in ['dragonite']:
  out=run('battle_batch',actor,2,'--foes',n,'--turns',1,'--min-hp',.5)
  if 'fight' in read().lower():out+=run('battle_batch',actor,1,'--foes',n,'--turns',5,'--min-hp',.35)
 else:out=run('battle_batch',actor,slot,'--foes',n,'--turns',6,'--min-hp',.5)
 t=read().lower()
 if 'change pok' in t or 'switch your' in t:
  m=re.findall(r'send\s*in\s*([\w-]+)',out.lower())
  if not m:raise SystemExit('Upcoming foe review: '+out[-500:])
  choices=difflib.get_close_matches(m[-1],plan,n=1,cutoff=.75)
  if not choices:raise SystemExit('Upcoming foe review: '+out[-500:])
  target=plan[choices[0]][0]
  if target==actor:act('x','wait:1')
  else:run('battle_switch',target)
  continue
 if 'VICTORY OVERWORLD' in out:print('INDRA VICTORY',flush=True);break
 if 'LOW HP REVIEW' in out:raise SystemExit('Low health needs an explicit healing decision')
 if 'fight' in t and any(n in t for n in plan):continue
 raise SystemExit('Battle state review')
else:raise SystemExit('Battle stage limit')
