"""Run a bounded offline mirror plan through public-proof normal controls."""
import json,sys,subprocess,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=Path(sys.argv[1]).resolve();assert p.is_relative_to(R/'work')
v=json.loads(p.read_text());assert len(v['pushes'])<=50
n=json.loads((R/'notes/navigation-state.json').read_text());assert n['positions']['896'][str(v['event'])]==v['from']
for d,g in itertools.groupby(v['pushes'],lambda x:x['direction']):
 group=list(g)
 args=['prisma_serra_push.py',d,str(len(group))] if v['event']==72 else ['prisma_mirror_push.py',str(v['event']),d,str(len(group))]
 subprocess.run([sys.executable,str(R/'scripts'/args[0]),*args[1:]],check=True)
 actual=json.loads((R/'notes/navigation-state.json').read_text())['positions']['896'][str(v['event'])];assert actual==group[-1]['after']
print('PUSH PLAN VERIFIED',v['event'],v['to'],flush=True)
