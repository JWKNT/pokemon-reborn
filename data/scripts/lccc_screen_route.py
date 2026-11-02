"""Reviewed normal walks through the Labradorra screen corridor, stages 10–20.
Only mirror a static single variable assignment after the game coordinate proves
that its player-touch tile was reached. No save, memory or battle-log reads.
"""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
steps=[(33,28,61,11),(35,29,60,12),(37,31,60,13),(39,33,60,14),(56,32,50,15),(58,28,50,16),(59,24,49,17),(61,20,50,18),(62,16,50,19),(63,12,50,20)]
statefile=ROOT/'notes/navigation-state.json'
for eid,x,y,stage in steps:
 e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),'774',str(eid)],stderr=subprocess.DEVNULL))
 p=e['pages'][0];cs=[c for c in p['list']if c['code']not in [0,108,408]]
 assert p['trigger']==1 and (e['x'],e['y'])==(x,y)
 assert all(c['code']in[250,122]for c in cs) and [c['parameters']for c in cs if c['code']==122]==[[475,475,0,0,stage]]
 state=json.loads(statefile.read_text());actual=state['variables']['475']
 if actual>=stage:continue
 assert actual==stage-1,(actual,stage)
 subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'774,{x},{y}'],check=True)
 public=json.loads((ROOT/'work/last-native-position.json').read_text())
 assert public['position']==[774,x,y]
 state=json.loads(statefile.read_text());state['variables']['475']=stage;statefile.write_text(json.dumps(state))
 print('NORMAL TOUCH VERIFIED; SOURCE ROUTE MIRROR',eid,stage,flush=True)
