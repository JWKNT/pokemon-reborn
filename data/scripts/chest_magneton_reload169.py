"""Reload the normal Frey victory checkpoint and take its reviewed route promptly."""
from play import *
rows=snap();assert 'continue' in ' '.join(x['text']for x in rows).lower()
path=json.loads((ROOT/'work/169-magneton-route.json').read_text())
act('c:.12','wait:3')
seq=[]
for step in path:
 assert not step['action']
 jump=step['key'].startswith('jump:');key=step['key'].removeprefix('jump:')
 seq += [key+':.08','wait:.35' if jump else 'wait:.075']
act(*seq,'right:.08','wait:.6')
print(read(),flush=True)
# Leave any battle/dialogue untouched. Otherwise freeze a real menu promptly.
rows=snap()
if not any(x['y']>.72 and len(x['text'])>10 for x in rows):
 from chest_safe_pause import finish_bag_entry
 act('x:.12','wait:.3','c:.12','wait:1.2');finish_bag_entry();print('BAG PAUSED',flush=True)
