"""Run an explicit, reviewed trainer matchup plan through ordinary battle UI.
Stops on unknown foes, low health, learning, losses, or unexpected menus.
"""
from play import *
import difflib,re
plan=json.loads(pathlib.Path(sys.argv[1]).read_text());actor=plan['lead'];matchups=plan['foes'];log=pathlib.Path(sys.argv[2]);began=time.time()
for phase in range(10):
 choices={n:p for n,p in matchups.items() if p['actor']==actor}
 if not choices:raise SystemExit('No plan for active actor')
 slots={n.lower():p['slot'] for n,p in choices.items()}
 recover=plan.get('recover',{}).get(actor)
 heal=plan.get('heal',{}).get(actor)
 extra=(['--stop-after-battle'] if '--stop-after-battle' in sys.argv else [])+(['--recover-below',str(recover['below']),'--recover-slot',str(recover['slot'])] if recover else [])
 if plan.get('opening_moves'):
  # A hard switch starts another batch, but does not make an opening move
  # new again. Preserve observed uses across phases and resumed drivers.
  history=log.read_text() if log.exists() else ''
  pending={name:slot for name,slot in plan['opening_moves'].items()
           if f'REVIEWED OPENING MOVE {name} ' not in history}
  if pending:extra+=['--openers',json.dumps(pending)]
 if '--world-pause' in sys.argv:extra+=['--world-pause','--stop-phrase','saphira']
 if heal:extra+=['--heal-below',str(heal['below']),'--heal-item',heal['item']]
 with log.open('a') as out:
  rc=subprocess.call([sys.executable,str(ROOT/'scripts/battle_batch.py'),actor,str(next(iter(slots.values()))),'--foes',','.join(slots),'--foe-slots',json.dumps(slots),'--watch','--stay','--turns','12','--min-hp',str(plan.get('min_hp',.5))]+extra,stdout=out,stderr=subprocess.STDOUT)
 t=read();low=t.lower();print(t,flush=True)
 if not any(s in low for s in ['change pok','switch your']):
  if not any(s in low for s in ['hp','fight','yes','choose a pok','pp:']):print('BATTLE FINISHED OR OVERWORLD REVIEW',flush=True);break
  if 'fight' in low:
   enemy=' '.join(x['text'].lower()for x in snap()if x['y']<.37).replace('nin jask','ninjask')
   hits=[n for n in matchups if any(difflib.SequenceMatcher(None,n.lower(),w.strip('.,')).ratio()>=.78 for w in enemy.split())]
   if len(hits)==1 and matchups[hits[0]]['actor']!=actor:
    nxt=matchups[hits[0]]['actor'];print('REVIEWED SWITCH AT COMMAND',hits[0],nxt,flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),nxt],check=True);actor=nxt;continue
  raise SystemExit('Battle requires review')
 upcoming=None
 for line in (ROOT/'recordings/screens.jsonl').read_text().splitlines()[::-1]:
  x=json.loads(line)
  if x['epoch']<began:break
  text=' '.join(x['text']).lower().replace('nin jask','ninjask')
  if 'send in' not in text:continue
  tail=text.split('send in',1)[1];words=re.findall('[a-z-]+',tail)
  hits=[n for n in matchups if any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.78 for w in words)]
  if len(hits)==1:upcoming=hits[0]
  break
 if not upcoming:
  print('INCOMING TEXT OBSCURED; decline free switch, verify actual next command',flush=True)
  act('x','wait:.5')
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
  continue
 nxt=matchups[upcoming]['actor'];print('PLANNED SWITCH',upcoming,nxt,flush=True)
 if nxt==actor:act('x','wait:1')
 else:
  act('c','wait:0.7')
  if subprocess.call([sys.executable,str(ROOT/'scripts/party_pick.py'),nxt]):raise SystemExit('Party selection review')
  actor=nxt
else:raise SystemExit('Phase limit')
