"""One reviewed visible-map interception flight, leaving a fresh map marker."""
from play import *
assert 'Reborn Region' in read()
act('x','wait:1.2','x','wait:1.2','x','wait:1.2')
t=read();assert len(t.replace('Pokemon Reborn','').strip())<8 and not re.search(r'\b(?:hp|yes|no|fight)\b',t.lower()),t
subprocess.run([sys.executable,str(ROOT/'scripts/fly_to.py'),sys.argv[1],'--carrier','Zapdos'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/ray369_map_after_fly.py')],check=True)
