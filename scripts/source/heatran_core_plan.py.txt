"""Read-only candidate planner for the monotone Ametrine Core crystal puzzle."""
import json,subprocess,sys
from pathlib import Path
import surface_readonly as surface
from surface_readonly import surface_plan
# A candidate pass asks many goals on one unchanged map. Reuse the two
# pure ground/water graphs, keyed by complete planning data and nav timestamp.
_original_route=surface.route
_graphs={}
def cached_route(v,goal,return_graph=False):
 if not return_graph:return _original_route(v,goal,return_graph)
 key=(repr(v),(surface.ROOT/"notes/navigation-state.json").stat().st_mtime_ns)
 if key not in _graphs:
  if len(_graphs)>8:_graphs.clear()
  _graphs[key]=_original_route(v,goal,return_graph)
 return _graphs[key]
surface.route=cached_route
R=Path(__file__).resolve().parents[1]
def approach(v,e):
 out=[]
 for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
  p=(e['x']+dx,e['y']+dy)
  try:r=surface_plan(v,p);out.append((sum(1 if ':'not in a['key'] else 3 for a in r),p))
  except ValueError:pass
 return min(out) if out else None
def candidates(v):
 out=[]
 for k,e in v['events'].items():
  cs=e['list'];text=str(cs)
  kind='crystal' if 'The Key reacted to the Crystal!'in text else 'rock' if 'Kernel.pbRockSmash'in text else None
  if not kind:continue
  a=approach(v,e)
  if a:out.append({'event':int(k),'kind':kind,'cost':a[0],'approach':a[1],'switches':[c['parameters']for c in cs if c['code']==121]})
 return sorted(out,key=lambda a:a['cost'])
if __name__=='__main__':
 v=json.load(open(sys.argv[1]));print(json.dumps(candidates(v),indent=2))
