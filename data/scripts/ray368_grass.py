"""Approach a source-reviewed Beryl grass tile and stop on any encounter/prompt."""
from play import *
from locate import locate
t=read()
if 'Reborn Region' in t:
 for _ in range(5):
  act('x','wait:1.2');t=read()
  if not any(s in t for s in ['Reborn Region','Field Notes','Quit Game']):break
 else:raise SystemExit('Menu close review')
assert locate()[0]==525
if '--save' in sys.argv:
 label=sys.argv[sys.argv.index('--save')+1]
 subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'525,3,34'],check=True)
for i in range(100):
 t=read();print(i,t.replace('\n',' | '),flush=True)
 if any(re.search(r'\b'+z+r'\b',t.lower()) for z in ['fight','hp','wild','repel','yes','no']):
  print('ENCOUNTER OR PROMPT: inspect before acting',flush=True);break
 act('right:.12','wait:.18','left:.12','wait:.5')
else:print('Bounded grass search finished',flush=True)
