"""Plan and execute one explicit mirror destination, verified by public frames."""
import subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
eid,x,y=map(int,sys.argv[1:]);assert eid in [72,73,74,75,95] and 17<=x<=28 and 59<=y<=68
p=R/'work'/f'prisma-plan-{eid}-{x}-{y}-{int(time.time())}.json'
with p.open('w') as f:subprocess.run([sys.executable,str(R/'scripts/prisma_push_plan.py'),str(eid),str(x),str(y)],stdout=f,check=True)
v=json.loads(p.read_text());assert len(v['pushes'])<=24
print('BOUNDED MIRROR PLAN',eid,v['from'],'->',v['to'],len(v['pushes']),'pushes',flush=True)
subprocess.run([sys.executable,str(R/'scripts/prisma_execute_push_plan.py'),str(p)],check=True)
