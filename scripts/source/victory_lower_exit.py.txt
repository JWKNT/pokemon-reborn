"""Normal lower doorway crossing out of map784, beginning in Party."""
from nav import *
from hazard_position import party_position
m,sx,sy=party_position();assert m==784
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'784',str(sx),str(sy)],stderr=subprocess.DEVNULL));e=v['events']['12']
assert any(c['code']==201 and c['parameters'][1:4]==[786,77,71] for c in e['list'])
p=route(v,(55,71));assert len(p)<50 and not any(k.startswith('jump:') for k in p)
print('LOWER EXIT',p,flush=True)
act('x','wait:.8','x','wait:.2',*[k+':.12' for k in p],'down:.12','wait:1')
t=read().lower();assert not any(w in t for w in ['fight','repel','used ','yes','no']),t
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Upper190-entry'],check=True)
s=json.loads((ROOT/'notes/Upper190-entry-status.json').read_text());assert s['map']==786,(s['map'],s['position'])
subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True)
