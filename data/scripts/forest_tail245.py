"""Advance only reviewed forest obstacle dialogue, then require stable overworld."""
from play import *
clear=0
for _ in range(16):
 rows=snap();t=' '.join(v['text'] for v in rows).lower();print(t,flush=True)
 if re.search(r'\b(fight|hp|yes|no)\b|pp:|attacked',t):raise SystemExit('Unexpected battle/choice')
 if any(x in t for x in ['heracross','pinsir','bouffalant','tauros']):
  act('c','wait:.8');clear=0
 elif any(v['y']>.73 and len(v['text'])>18 for v in rows):raise SystemExit('Unknown dialogue')
 else:
  clear+=1
  if clear>=3:break
  act('wait:.8')
else:raise SystemExit('Forest tail timeout')
