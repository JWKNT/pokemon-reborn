"""One reviewed level75 Statuary fight using ordinary public battle controls."""
from play import *
t=read()
if 'Statuary' in t and 'battle' in t:act('c','wait:1')
else:assert 'Garchomp' in t and '75' in t,t
subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
t=read();assert 'Garchomp' in t and '75' in t and 'Volcanion' in t and 'FIGHT' in t,t
subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),'0','--watch'],check=True)
t=read();assert 'defeated' in t.lower() and 'Statuary' in t,t
act('c','wait:.4');t=read();assert 'Gar' in t,t
act('c','wait:.2','up:2.0','d:1.0','wait:.4');print(read(),flush=True)
