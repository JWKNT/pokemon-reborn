"""Known Route 2 approach; input only, stops on unexpected route/dialog."""
from play import *
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'358,25,41,left,c,wait:.8'],check=True)
t=read().lower();print(t,flush=True)
if 'spores drip' not in t:raise SystemExit('Powder tree interaction review')
for _ in range(6):
 act('c','wait:.6');t=read().lower();print(t,flush=True)
 if 'sleep powder obtained' in t or 'sleep pouder obtained' in t:
  act('c','wait:.6')
  p=ROOT/'notes/navigation-state.json';x=json.loads(p.read_text());x.setdefault('switches',{}).update({'410':True,'464':True,'463':False});p.write_text(json.dumps(x));break
else:raise SystemExit('Powder acquisition review')
