"""Final reviewed Speed boost, heal, own stats proof and guaranteed five-Hex sweep."""
import json,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
v=json.loads((ROOT/'work/ricardo-speed2.json').read_text());assert v['error']=='ValueError: Capture restarted; stop and inspect, never repeat pending action'
assert any('Speed rose sharply' in line for c in v['literal_message_candidates'] for line in c['lines'])
for label,item,threshold in [('speed3','X Speed',93),('heal','Ultra Potion',1)]:
 out=ROOT/'work'/('ricardo-final-'+label+'.json')
 subprocess.run([sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','ricardo','--min-hp',str(threshold),'--item',item,'--output',str(out)],check=True)
 r=json.loads(out.read_text());assert r['final_classification']=='fresh_expected_command'
assert r['final_hp_proof']['hp']>=76
from play import read,act,snap
from agate_public_action import inspection_guard,command_guard
act('q:.12','wait:.6');rows=snap();proof=inspection_guard(rows)
text=proof['inspection_text'];assert re.search(r'Sp[. ]?Attack\s*:\s*840\b',text,re.I),text
assert re.search(r'Speed\s*:\s*272\b',text,re.I),text
assert proof['hp']>=76
(ROOT/'work/ricardo-presweep-own-stats.json').write_text(json.dumps({'epoch':time.time(),'public_rows':rows,'proof':proof},indent=2)+'\n')
act('x:.12','wait:.6');rows=snap();command_guard(rows,['Slurpuff'],'ricardo',captured_at=time.time(),now=time.time())
subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'Cofagrigus','1','--foes','Slurpuff,Minior,Scolipede,Aggron,Blaziken','--stay-team-reviewed','--watch','--turns','5','--min-hp','.30','--stop-after-victory'],check=True)
