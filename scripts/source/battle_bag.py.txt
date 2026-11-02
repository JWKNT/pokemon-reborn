"""Open the battle bag from a verified command menu, regardless of cursor position."""
from play import *
from PIL import Image
t=read().lower()
if 'fight' not in t or not any(w in t.split() for w in ['bag','bae']):raise SystemExit('Battle command menu expected')
act('right:0.22','up:0.22','c','wait:1.3');print(read(),flush=True)
