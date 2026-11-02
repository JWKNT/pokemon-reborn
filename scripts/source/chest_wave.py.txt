"""Execute a bounded reviewed matchup, then freeze the map immediately."""
import sys,subprocess,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from play import snap,act
from chest_safe_pause import classify
actor,slot,foe=sys.argv[1:4]
began=time.time()
log=ROOT/f'work/chest-{foe}-{int(time.time())}.log'
with log.open('w') as f:
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),actor,slot,'--foes',foe,'--wild','--watch','--turns','5','--min-hp','.4','--stop-phrase','saphira','--world-pause'],stdout=f,stderr=subprocess.STDOUT)
r=snap();t=' '.join(x['text'] for x in r).lower()
if classify(r)=='bag':print('ACTUAL BAG PAUSE',flush=True)
elif not any(z in t for z in ['fight','hp','choose a pok','fainted','saphira']):
 act('x:.12','wait:.3','c:.12','wait:1.5');r=snap()
 assert classify(r)=='bag','Actual Bag pause needs prompt review'
 print('ACTUAL BAG PAUSE',flush=True)
else:print('BATTLE/DIALOGUE REVIEW',t,flush=True)
print(log,flush=True)

rows=[json.loads(l) for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]
recent=[r for r in rows if r['epoch']>=began]
faints=[r for r in recent if foe.lower() in ' '.join(r['text']).lower() and 'fainte' in ' '.join(r['text']).lower()]
if faints and len(sys.argv)>4:
 from bgm_span import append_span,wild_track
 wave=int(sys.argv[4]);control=json.loads((ROOT/'notes/current-run-control.json').read_text());p=ROOT/control['active_gauntlet_journal'];j=json.loads(p.read_text());assert j['result']=='active' and wave not in [w['wave']for w in j['waves']]
 j['waves'].append({'wave':wave,'foe':foe,'result':'victory','public_evidence':faints[-1],'worker_log':str(log.relative_to(ROOT))});p.write_text(json.dumps(j,indent=2))
 append_span(began,faints[-1]['epoch'],wild_track());append_span(faints[-1]['epoch'],time.time(),'Victory!')
 print('WAVE RECORDED',wave,flush=True)
