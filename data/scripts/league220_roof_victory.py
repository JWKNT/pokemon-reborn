"""Close an observed ordinary victory, then its source-reviewed linear tail.

Normal UI only. Requires actual victory before inputs, one installed battle,
no later choice/battle, and clears the battle HUD before the existing scene tool.
"""
import json,re,subprocess,sys
from pathlib import Path
from play import read,act,ROOT
mid,eid,page=map(int,sys.argv[1:4])
e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(mid),str(eid)],stderr=subprocess.DEVNULL))
cs=e['pages'][page]['list'];hits=[i for i,c in enumerate(cs)if any(k in str(c['parameters'])for k in ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle'])]
assert (mid,eid,page)==(573,30,0) and len(hits)==2, 'Reviewed rooftop two-battle chain only'
assert 'Eustace' in str(cs[hits[-1]]['parameters'])
assert not any(c['code'] in [102,103,104,301] or any(k in str(c['parameters'])for k in ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle'])for c in cs[hits[-1]+1:]), 'Tail must be linear'
t=read();assert re.search(r'de.?feated|for winning',t,re.I), 'Public victory required'
for _ in range(12):
 print(t,flush=True)
 hud=r'\bhp\b|for winning|l[uvw][.\s]?\d{1,3}|\d+\s*/\s*\d+'
 if not re.search(hud,t,re.I):
  act('wait:1');t=read()
  if not re.search(hud,t,re.I):break
 act('c','wait:.6');t=read()
else:raise SystemExit('Victory HUD did not clear; review')
subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),str(mid),str(eid),'--source-page',str(page),'--after-last-battle','--past-battle','--burst'],check=True)
