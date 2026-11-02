"""Approach the source-reviewed entry rock through normal controls."""
from nav import *
from hazard_position import party_position
m,x,y=party_position();assert m==784
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'784',str(x),str(y)],stderr=subprocess.DEVNULL))
e=v['events']['123'];assert (e['x'],e['y'])==(53,29) and 'pbRockSmash' in str(e['list'])
p=route(v,(53,30));assert len(p)<50 and not any(k.startswith('jump:') for k in p)
print('ROCK SMASH APPROACH',p,flush=True)
act('x','wait:.8','x','wait:.2',*[k+':.12' for k in p],'up:.12','c','wait:.7','c','wait:.7','c','wait:.7','c','wait:2')
print(read(),flush=True)
