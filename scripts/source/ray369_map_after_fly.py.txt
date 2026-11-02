"""Open the visible Region Map after a verified normal Fly (Pokemon menu remembered)."""
from play import *
from ray368_marker import marker
if '--menu-open' not in sys.argv:act('x','wait:1.2')
t=read();assert ('Pokégear' in t or 'Pokegear' in t) and 'Quit Game' in t,t
act('down','wait:.2','down','wait:.2','c','wait:1.2');t=read();assert 'Field Notes' in t,t
act('down','wait:.2','down','wait:.2','down','wait:.2','c','wait:1.2','right','wait:.2','right','wait:.3')
assert 'Reborn Region' in read()
print('PUBLIC MARKER',marker(),flush=True)
