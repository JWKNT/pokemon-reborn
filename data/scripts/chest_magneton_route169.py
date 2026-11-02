"""Follow reviewed static ground/ledge route to Magneton; halt on public interruption."""
from play import *
from chest_safe_pause import classify,finish_bag_entry
path=json.loads((ROOT/'work/169-magneton-route.json').read_text())
assert classify(snap())=='bag'
act('x:.12','wait:1','x:.12','wait:.2')
for start in range(0,len(path),18):
 seq=[]
 for step in path[start:start+18]:
  assert not step['action']
  jump=step['key'].startswith('jump:');key=step['key'].removeprefix('jump:')
  seq += [key+':.12','wait:.70' if jump else 'wait:.10']
 act(*seq)
 rows=snap();t=' '.join(x['text']for x in rows);print('CHUNK',start,t,flush=True)
 if any(x['y']>.72 and len(x['text'])>10 for x in rows):raise SystemExit('Public interruption; no further route inputs')
act('right:.08','wait:.6')
rows=snap();print(rows,flush=True)
if not any(x['y']>.72 and len(x['text'])>10 for x in rows):
 act('x:.12','wait:.3','c:.12','wait:1.2');finish_bag_entry();print('BAG PAUSED; verify endpoint',flush=True)
