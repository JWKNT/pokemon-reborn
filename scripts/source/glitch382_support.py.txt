"""Four explicit bench supplies behind Cresselia against reviewed Carbink only."""
from play import *
import re
steps=[('Full Heal','Latias'),('Bubble Tea','Latias'),('Bubble Tea','Kyogre'),('Bubble Tea','Kyogre')]
def hp():
 t=read();print(t,flush=True)
 assert 'fight' in t.lower() and 'carbink' in t.lower() and 'cresselia' in t.lower(),'Support matchup changed'
 h=re.search(r'(\d+)\s*[/F]\s*639',t);assert h,'Fresh own HP required'
 return int(h[1])
journal=ROOT/'work/glitch382-support.json'
j=json.loads(journal.read_text()) if journal.exists() else dict(done=0,pending=None)
assert not j['pending'],'Interrupted item needs public review'
for index,(item,name) in list(enumerate(steps))[j['done']:]:
 health=hp()
 if health<350:
  assert health>180,'Unsafe support HP; review before another move'
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),'3','--watch'],check=True)
  assert hp()>health,'Moonlight did not improve health'
 j['pending']=[item,name];journal.write_text(json.dumps(j))
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_item.py'),item,name],check=True)
 j.update(done=index+1,pending=None);journal.write_text(json.dumps(j))
print('EXPLICIT BENCH SUPPLIES COMPLETE',flush=True)
