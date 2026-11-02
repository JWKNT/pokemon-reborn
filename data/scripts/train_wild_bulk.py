"""Repeat only two reviewed weak wild matchups; stop on any unverified outcome.
Start in a safe horizontal grass strip, with the chosen Pokemon already leading.
"""
from play import *
import re,difflib
from PIL import Image
actor=sys.argv[1];slot=int(sys.argv[2]);count=int(sys.argv[3]);assert 1<=count<=16
hunter=sys.argv[sys.argv.index("--hunter")+1] if "--hunter" in sys.argv else None
participant=sys.argv[sys.argv.index("--participant")+1] if "--participant" in sys.argv else None
log=ROOT/'work'/f'bulk-{actor.lower()}-{int(time.time())}.json';wins=[]
pp_request=ROOT/'work/restore-training-pp'
if pp_request.exists():
 subprocess.run([sys.executable,str(ROOT/'scripts/field_medicine.py'),'Max Elixir',actor],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
 pp_request.unlink()

for i in range(count+5):
 if len(wins)>=count:break
 if hunter and '--relead-hunter' in sys.argv:
  subprocess.run([sys.executable,str(ROOT/'scripts/party_front.py'),hunter],check=True)
 targets='Meditite,Mienfoo' # Machoke can make Shadow Ball fail completely on Rocky Field.
 if '--targets' in sys.argv:targets=sys.argv[sys.argv.index('--targets')+1]
 if '--also-boldore' in sys.argv:targets+=',Boldore'
 subprocess.run([sys.executable,str(ROOT/'scripts/hunt_target.py'),targets,*(['--expire-repel'] if '--expire-repel' in sys.argv else []),*(['--dense-horizontal'] if '--dense-horizontal' in sys.argv else []),*(['--grass-pair'] if '--grass-pair' in sys.argv else (['--right-wall'] if '--right-wall' in sys.argv else (['--vertical'] if '--vertical' in sys.argv else [])))],check=True)
 text=read();low=text.lower();foe=next((n for n in (targets.split(',') if '--flex-targets' in sys.argv else ['Meditite','Mienfoo','Machoke']) if n.lower() in low),None)
 if foe is None and '--flex-targets' in sys.argv:
  matches=[n for n in targets.split(',') if any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.82 for w in re.findall('[a-z]+',low))]
  if len(matches)==1:foe=matches[0]
 if foe is None and 'boldore' in low:
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'Swampert','1','--foes','Boldore','--turns','1','--wild','--watch','--min-hp','.65'],check=True)
  text=read();low=text.lower()
  if re.search(r'\bfight\b|\bhp\b|\byes\b|\bno\b|\bpp:',low) or len(text.splitlines())>4:raise SystemExit('Surviving Boldore / battle review: '+text)
  subprocess.run([sys.executable,str(ROOT/'scripts/close_wild_music.py'),'Boldore'],check=True)
  print('NON-STURDY BOLDORE DEFEATED',flush=True);continue
 if foe is None:raise SystemExit('Hunt stopped without an approved opponent: '+text)
 began=time.time()
 if hunter:
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),hunter,'0','--foes',foe,'--turns','0'],check=True)
  if participant:subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),participant],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),actor],check=True)
 outfile=ROOT/'work'/f'bulk-{actor.lower()}-battle.log'
 heal_item=sys.argv[sys.argv.index('--heal-item')+1] if '--heal-item' in sys.argv else 'Hyper Potion'
 selected_slot=slot
 if '--foe-slots' in sys.argv:
  reviewed_slots=json.loads(sys.argv[sys.argv.index('--foe-slots')+1]);selected_slot=int(reviewed_slots.get(foe,slot))
  assert 0<=selected_slot<4
  print('REVIEWED TRAINING MATCHUP',foe,'move slot',selected_slot,flush=True)
 recover=[]
 if '--recover-slot' in sys.argv:
  recover_slot=int(sys.argv[sys.argv.index('--recover-slot')+1]);assert 0<=recover_slot<4
  recover_below=float(sys.argv[sys.argv.index('--recover-below')+1]) if '--recover-below' in sys.argv else .6
  assert 0<recover_below<1
  recover=['--recover-below',str(recover_below),'--recover-slot',str(recover_slot)]
 # Reviewed low-level Opal Rattata can use Endeavor while switching. Healing
 # repeatedly does not beat Endeavor; survive its resisted ordinary attacks
 # and finish with the already reviewed one-hit KO instead.
 opal_rat='--ev-ledger' in sys.argv and foe=='Rattata' and actor=='Excadrill'
 with outfile.open('w') as f:subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),actor,str(selected_slot),'--foes',foe,'--watch','--wild','--turns','3','--min-hp','.12' if opal_rat else '.4','--heal-below','0' if opal_rat or recover else '.6','--heal-item',heal_item]+recover,stdout=f,stderr=subprocess.STDOUT,check=True)
 if any(k in outfile.read_text() for k in ['Traceback','BAG REVIEW','LOSS REVIEW','LOW HP REVIEW']):raise SystemExit('Training policy stopped; do not credit a KO')
 text=read();low=text.lower()
 # A cleared HUD in an open bag is not an overworld victory.
 if len(text.splitlines())>4 or re.search(r'\bhp\b|\bfight\b|pp:|close bag|sort',low):raise SystemExit('No verified overworld after training; do not credit a KO: '+text)
 rows=[json.loads(l) for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()];rows=[r for r in rows if r['epoch']>=began]
 faint=[r for r in rows if 'fainted' in ' '.join(r['text']).lower()]
 if not faint:
  used=any(re.sub('[^a-z]','',actor.lower())+'used' in re.sub('[^a-z]','', ' '.join(r['text']).lower())for r in rows)
  # Turbo can advance directly from damage to the EXP award between frames.
  # Named public EXP text proves the attack resolved successfully; native EVs
  # must still be reconciled after the block before crediting its total.
  exp_award=any(actor.lower() in ' '.join(r['text']).lower() and re.search(r'gained\s+\d+\s+exp', ' '.join(r['text']),re.I) for r in rows)
  used=used or exp_award
  escaped=any(any(z in ' '.join(r['text']).lower()for z in ['fled','ran away','got away','u-turn','teleport'])for r in rows)
  if '--ev-ledger' not in sys.argv or (not used and foe not in ['Rhyhorn','Rhydon','Boldore','Donphan','Meditite','Rockruff','Rattata','Bidoof','Patrat','Zigzagoon','Meowth','Spinarak','Stunky','Pidgey','Pidgeotto','Noibat','Woobat']) or escaped:raise SystemExit('No faint evidence; do not credit training EVs')
  print('HUD CLEARED AFTER ATTACK — provisional KO, requires saved EV reconciliation',flush=True)
 if re.search(r'\bfight\b|\bhp\b|\byes\b|\bno\b|\bpp:',low):raise SystemExit('Battle completion requires review: '+text)
 if any(actor.lower() in ' '.join(r['text']).lower().split('fainted')[0][-35:] and 'wild' not in ' '.join(r['text']).lower() for r in faint):raise SystemExit('Own faint requires review')
 from bgm_span import append_span,wild_track
 end=time.time();last_hp=[r['epoch'] for r in rows if any('hp' in z.lower() for z in r['text'])];victory=faint[-1]['epoch'] if faint else ((last_hp[-1]+1) if last_hp else end-3)
 append_span(began-3,victory,wild_track());append_span(victory,end,'Victory!')
 wins.append({'foe':foe,'start_epoch':began,'end_epoch':end,'faint_evidence':bool(faint),'ev_reconciliation_required':not bool(faint)});log.write_text(json.dumps(wins,indent=2));print('TRAINING WIN / EV CHECK PENDING' if '--ev-ledger' in sys.argv else 'VERIFIED TRAINING WIN',len(wins),'of',count,foe,flush=True)
print('BULK TRAINING COMPLETE' if len(wins)==count else 'BATCH LIMIT REVIEW',len(wins),log,flush=True)
