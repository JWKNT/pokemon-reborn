"""Execute a reviewed, resumable map786 boulder route with normal controls."""
from play import *
from itertools import groupby
plan=json.loads(pathlib.Path(sys.argv[1]).read_text());eid=int(sys.argv[2]);prefix=sys.argv[3]
assert plan['map']==786 and eid in [40,41,63,64,100,116] and re.fullmatch(r'[A-Za-z0-9-]+',prefix)
s=json.loads((ROOT/'notes/navigation-state.json').read_text());current=s['positions']['786'][str(eid)]
pushes=[p for p in plan['pushes'] if p['event']==eid]
if current!=plan['initial'][str(eid)]:
 matches=[i for i,p in enumerate(pushes) if p['box_to']==current]
 assert len(matches)==1,('Ambiguous resume',current)
 pushes=pushes[matches[0]+1:]
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
for i,(direction,items) in enumerate(groupby(pushes,lambda p:p['direction']),1):
 group=list(items);run('victory_boulder_push',786,eid,direction,len(group))
 if i%3==0:
  run('checkpoint',f'{prefix}-{i}')
  s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['positions']['786'][str(eid)]==group[-1]['box_to']
run('checkpoint',prefix+'-done')
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['positions']['786'][str(eid)]==plan['goals'][str(eid)]
print('BOULDER GOAL VERIFIED',eid,plan['goals'][str(eid)],flush=True)
run('party_open')
