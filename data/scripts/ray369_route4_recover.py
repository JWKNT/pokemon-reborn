"""Return through the south gate, then use the eastern Route4 gate."""
from play import *
from ray368_marker import marker
for args in [('418','413'),('413','418','--arrival','17','7'),('418','412')]:
 subprocess.run([sys.executable,str(ROOT/'scripts/city_enter.py'),*args],check=True)
act('x','wait:1.2','c','wait:1.2');assert 'Field Notes' in read()
act('down','wait:.15','down','wait:.15','down','wait:.15','c','wait:1.2','left','wait:.2','left','wait:.3')
assert 'Reborn Region' in read()
print('PUBLIC MARKER',marker(),flush=True)
