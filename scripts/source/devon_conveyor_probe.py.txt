"""Bounded field-radio-safe empirical probe; choose no subsequent route."""
from play import ROOT,act,read
from locate import locate
import json
assert locate(629)==(629,26,11)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());old=s['variables']['342'];n=(3-old)%3
if n:act(*sum((['a:.12','wait:.4']for _ in range(n)),[]))
s['variables']['342']=3;p.write_text(json.dumps(s))
act('up:.12','wait:3');print(read(),flush=True);actual=locate(629);print('TERRAIN TO EVENT PROBE END',actual,flush=True)
(ROOT/'notes/devon-629-conveyor-probe.json').write_text(json.dumps({'start':[629,26,11],'radio':3,'input':'up:.12','observed_end':actual},indent=2)+'\n')
