from play import *
newmove='False Swipe';replacement=0
from learning import resolve,PLANS
PLANS[newmove.lower()]=replacement
for _ in range(12):
 t=read();print(t,flush=True)
 if 'trying to learn' in ' '.join(t.lower().split()):
  if not resolve(t):raise SystemExit('Learning prompt review')
  break
 if any(s in t.lower() for s in ['not compatible','already knows','not learn']):raise SystemExit('Teaching rejected')
 act('c','wait:.4')
else:raise SystemExit('Learning prompt timeout')
for _ in range(12):
 t=read().lower()
 if 'teach which' in t or sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3:break
 if 'yes' in t.splitlines() or 'no' in t.splitlines():raise SystemExit('Unexpected post-learning choice')
 act('c','wait:.4')
else:raise SystemExit('Teaching completion timeout')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
