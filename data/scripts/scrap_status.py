"""Read-only reachability report from observed native coordinates and installed map."""
from nav import *
from locate import locate
m,x,y=locate(int(sys.argv[1]) if len(sys.argv)>1 else None)
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(x),str(y)],stderr=subprocess.DEVNULL))
for eid,e in v['events'].items():
 cs=e['list']or[];text=str(cs)
 if not (any(c['code']==201 for c in cs) or 'pbRockSmash' in text or 'Full steam ahead?' in text or 'pbItemBall' in text):continue
 opts=[]
 for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  try:opts.append((len(route(v,(e['x']+dx,e['y']+dy))),(e['x']+dx,e['y']+dy),k))
  except ValueError:pass
 if opts:print(eid,e['name'],(e['x'],e['y']),min(opts),[c['parameters'] for c in cs if c['code']in[121,122,201]],flush=True)
print('POSITION',m,x,y,flush=True)
