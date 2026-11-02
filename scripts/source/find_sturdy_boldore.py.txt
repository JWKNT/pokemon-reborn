"""Check bounded Boldore encounters with one Earthquake; stop at any survivor.
Reviewed for Swampert70 versus Cascade Boldore50–55. Never throws balls blindly.
"""
from play import *
from bgm_span import append_span,wild_track
for attempt in range(8):
 if attempt or '--already-found' not in sys.argv:subprocess.run([sys.executable,str(ROOT/'scripts/hunt_target.py'),'Boldore','--grass-pair'],check=True)
 t=read();low=t.lower()
 if 'boldore' not in low:raise SystemExit('Hunt prompt review: '+t)
 began=time.time()-3
 with (ROOT/'work'/f'boldore-check-{int(began)}.log').open('w') as f:
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'Swampert','1','--foes','Boldore','--turns','1','--wild','--watch','--min-hp','.65'],stdout=f,stderr=subprocess.STDOUT,check=True)
 t=read();low=t.lower()
 if any(z in low for z in ['fight',' hp','choose a pok','pp:','yes']):print('SURVIVING BOLDORE / BATTLE REVIEW',t,flush=True);break
 if len(t.splitlines())>4:raise SystemExit('Outcome review: '+t)
 rows=[json.loads(l) for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()];rows=[x for x in rows if x['epoch']>=began];hp=[i for i,x in enumerate(rows) if any('hp' in s.lower() for s in x['text'])]
 end=next((x['epoch'] for x in rows[hp[-1]+1:] if len(x['text'])<4),time.time()) if hp else time.time()
 append_span(began,end-2,wild_track());append_span(end-2,end+3,'Victory!')
 print('NON-STURDY BOLDORE DEFEATED; CONTINUING',attempt+1,flush=True)
else:raise SystemExit('Eight Boldore checks completed; review supplies')
