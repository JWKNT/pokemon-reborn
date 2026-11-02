"""Route explicit known map/coordinates; no saving. Stop on dialogue/battle."""
from nav import *
# Each JSON step: [map,startx,starty,destx,desty, optional key actions]
steps=json.loads(pathlib.Path(sys.argv[1]).read_text())
for mid,sx,sy,tx,ty,*tail in steps:
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(sx),str(sy)],stderr=subprocess.DEVNULL))
 path=route(v,(tx,ty));print('ROUTE',mid,[sx,sy],'→',[tx,ty],len(path),'tiles',flush=True)
 # Batch up to 3 direction-runs then inspect, avoiding per-tile round trips.
 groups=[(key,len(list(g))) for key,g in groupby(path)]
 for j in range(0,len(groups),3):
  seq=[]
  for key,n in groups[j:j+3]:
   if key.startswith('jump:'):seq.extend([key[5:],'wait:0.9']*n)
   else:seq.append(f'{key}:{n*.1+.02:.3f}')
  act(*seq);rr=snap();txt=' '.join(t['text'] for t in rr)
  if any(w in txt.lower() for w in [' hp','fight','wild ']) or any(t['y']>.73 and len(t['text'])>22 for t in rr):
   print('INTERRUPTED',txt,flush=True);sys.exit(2)
 if tail:act(*tail[0]);print(read(),flush=True)
print('QUEUE DONE',flush=True)
