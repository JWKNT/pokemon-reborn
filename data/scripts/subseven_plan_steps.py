"""Compile an offline, inspected Subseven plan into existing guarded UI calls."""
import json,itertools,sys
from pathlib import Path
x=json.loads(Path(sys.argv[1]).read_text());out=[];anchor=None
def group(a):
 if a[0]=='phase':return(a[0],a[4],a[5])
 if a[0]=='walk':return(a[0],)
 return tuple(a)
for key,g in itertools.groupby(x['actions'],key=group):
 actions=list(g);a=actions[-1]
 if a[0]=='walk':out.append(['q',f'871,{a[2]},{a[3]}'])
 elif a[0]=='phase':
  out.append(['subseven_phase_walk',a[4],a[5],a[2],a[3]]);anchor=(a[4],a[5]) if abs(a[2]-a[4])+abs(a[3]-a[5])<=8 else None
 elif a[0]=='transfer':out.append(['eventq',871,a[1],'enter'])
 elif a[0]=='statue':
  if anchor:out.append(['subseven_statue_activate',*anchor,a[1],a[2],a[3]])
  else:out.append(['eventq',871,a[1],'talk'])
 else:raise ValueError(a)
Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
