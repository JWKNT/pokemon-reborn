"""Enter the source-reviewed wild Arceus after the completed final gauntlet."""
from play import *
assert json.loads((ROOT/'notes/active-league-chain.json').read_text())['status']=='completed'
p=ROOT/'work/394-arceus-capture.json';assert not p.exists()
(ROOT/'notes/battle-control.json').write_text(json.dumps(dict(stop=False,expected_foes=['Arceus']),indent=2)+'\n')
p.write_text(json.dumps(dict(species='Arceus',session=394,start_epoch=time.time(),event=301),indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'898','301','talk'],check=True)
t=read();assert 'arceus' in t.lower(),t
act('c','wait:3')
subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
