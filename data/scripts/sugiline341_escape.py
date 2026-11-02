"""Normal walking from the publicly observed frozen coordinate popup, no runtime reads."""
from play import *
from route_readonly import route
rows=snap();text=' '.join(r['text'] for r in rows)
assert '13' in text and '37' in text and '660' in text and 'map' in text.lower(),text
v=json.loads((ROOT/'work/341-map660.json').read_text());v['position']=[13,37]
path=route(v,(14,9));assert all(k in ['up','down','left','right'] for k in path)
print('REVIEWED WALK',len(path),flush=True)
act('c',*[k+':.12' for k in path],'wait:.2','d:1.0','wait:.3')
print(read(),flush=True)
