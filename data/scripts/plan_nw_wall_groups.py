"""Offline physical-wall proofs for bounded NW pushes; never imports controls."""
import ast,json,heapq,re,subprocess,copy,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ns=dict(ROOT=R,json=json,heapq=heapq,re=re)
t=ast.parse((R/'scripts/nav.py').read_text());f=next(x for x in t.body if isinstance(x,ast.FunctionDef)and x.name=='route')
s=ast.unparse(f).replace('graph = {}','jumps = {}; graph = {}').replace('native_jump = terrain(n) == 1','native_jump = False');exec(s,ns)
v=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'784','85','22'],stderr=subprocess.DEVNULL))
steps=sum([json.loads((R/f'work/192-nw-{part}-plan.json').read_text())['pushes']for part in ['upper','lower']],[])
out=[];index=1
for (eid,direction),group in itertools.groupby(steps,lambda p:(p['event'],p['direction'])):
 group=list(group);e=v['events'][str(eid)];vv=copy.deepcopy(v);vv['events'].pop(str(eid));g=ns['route'](vv,None,True);end=tuple(group[-1]['box_to']);blocked={(a['x'],a['y'])for a in vv['events'].values()if not a['through']}
 cur=(e['x'],e['y']);valid=not any(k==direction for k,n in g.get(end,[]))
 for p in group:
  dest=tuple(p['box_to']);valid=valid and (direction,dest)in g.get(cur,[]) and dest not in blocked;cur=dest
 out.append(dict(start=index,count=len(group),event=eid,direction=direction,box_from=[e['x'],e['y']],box_to=list(end),wall_burst=valid))
 e.update(x=end[0],y=end[1]);index+=len(group)
(R/'work/194-nw-push-groups.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
