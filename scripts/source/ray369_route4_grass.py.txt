"""Use the observed Route4 marker; stop on encounter or Repel prompt."""
from play import *
from ray368_marker import marker
assert 'Reborn Region' in read();assert marker()['grid'] in [[13,2],[12,4]]
act('x','wait:1.2','x','wait:1.2','x','wait:1.2')
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'412,12,17'],check=True)
for i in range(100):
 t=read();print(i,t.replace('\n',' | '),flush=True)
 if any(re.search(r'\b'+z+r'\b',t.lower()) for z in ['fight','hp','wild','repel','yes','no']):break
 act('up:.12','wait:.2','down:.12','wait:.5')
else:raise SystemExit('Bounded grass search finished')
if 'rayquaza' in t.lower():
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/capture_bounded.py'),'Mawile','Rayquaza','--ball','Premier Ball','--throws','4','--total-hp','404','--heal-below','170'],check=True)
