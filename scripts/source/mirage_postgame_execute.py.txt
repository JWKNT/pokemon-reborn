"""Execute a reviewed static linked-block solution with per-push pixel checks."""
import itertools,json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=Path(sys.argv[1]).resolve();v=json.loads(p.read_text());start=int(sys.argv[2]);label=sys.argv[3]
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
at=start
for (eid,direction),seq in itertools.groupby(v['steps'][start:],lambda z:(z.get('event',v['event']),z['direction'])):
 n=len(list(seq));print('PUSH GROUP',at,eid,direction,n,flush=True)
 run('mirage_postgame_push',v['map'],eid,direction,n,'--plan-start',at,'--plan',p);at+=n
if v['event'] in [23,147,149]:
 event,page,stage={23:(244,2,1),147:(107,2,2),149:(245,1,3)}[v['event']]
 run('linear_dialog',880,event,'--source-page',page)
 run('checkpoint',label)
 n=json.loads((R/'notes'/f'{label}-navigation.json').read_text());assert n['variables']['646']==stage
else:
 if v['event']==157:run('linear_dialog',880,246,'--source-page',3)
 run('checkpoint',label)
 n=json.loads((R/'notes'/f'{label}-navigation.json').read_text());assert n['switches'][str({157:1760,233:1761}[v['event']])]
print('PUZZLE EXECUTION COMPLETE',label,flush=True)
