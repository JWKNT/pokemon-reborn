"""Exchange known Box0 slot10 Ampharos with current party slot3 Drapion, UI only."""
from play import *
import re
t=read().lower()
if 'organize' in t and 'move pok' in t:
 act('c','wait:1.2');t=read().lower()
if not re.search(r'box\s*1',t):raise SystemExit('Fresh Box1 cursor0 required: '+t)
act(*(['right:.05']*4),'down:.05','wait:.4');t=read();print(t,flush=True)
if 'ampharos' not in t.lower():raise SystemExit('Box10 Ampharos selection review')
act('a','wait:.5',*(['down:.05']*4),'left:.05','c','wait:.7','down:.05','right:.05','a','wait:.8');t=read();print(t,flush=True)
if 'drapion' not in t.lower():raise SystemExit('Held swapped Drapion review')
act('x','wait:.6',*(['right:.05']*4),'down:.05','a','wait:.7');t=read();print(t,flush=True)
if 'drapion' not in t.lower():raise SystemExit('Drapion replacement box slot review')
act('x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
act('x','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
print('AMPHAROS PARTY / DRAPION BOX10 EXCHANGE COMPLETE',flush=True)
