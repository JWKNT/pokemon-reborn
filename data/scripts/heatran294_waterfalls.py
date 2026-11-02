"""Ordinary waterfall interactions after restoring Waterfall; verify each map."""
from play import *
from locate import locate

def run(n,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{n}.py'),*map(str,a)],check=True)
assert locate(380)==(380,58,39)
act('down:.03','c','wait:.8');t=read();print(t,flush=True)
if 'yes' in t.lower() and 'no' in t.lower():
 run('choose_dialog','Yes|No','Yes');act('c','wait:5')
else:act('wait:5')
assert locate(386)[0]==386
run('surface_event',386,10,'talk')
t=read()
if 'yes' in t.lower() and 'no' in t.lower():
 run('choose_dialog','Yes|No','Yes');act('c','wait:5')
else:act('wait:5')
assert locate(387)[0]==387
run('checkpoint','Heatran294-CelestinineB2')
