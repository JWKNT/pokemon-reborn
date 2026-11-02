"""Normal Calcenon gate route to Route4; stop on the visible region marker."""
from play import *
from ray368_marker import marker
assert 'Reborn Region' in read()
act('x','wait:1.2','x','wait:1.2','x','wait:1.2')
subprocess.run([sys.executable,str(ROOT/'scripts/city_enter.py'),'413','418','--arrival','17','7'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/city_enter.py'),'418','412'],check=True)
act('x','wait:1.2','c','wait:1.2');assert 'Field Notes' in read()
act('down','wait:.15','down','wait:.15','down','wait:.15','c','wait:1.2','left','wait:.2','left','wait:.3')
assert 'Reborn Region' in read()
print('PUBLIC MARKER',marker(),flush=True)
