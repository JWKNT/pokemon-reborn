from play import *
import re
item=sys.argv[1]
if '--bag-open' not in sys.argv:
 act('x','wait:0.5','c','wait:1.5');t=read().lower()
 if 'pokedex' in t and ('seen' in t or 'search' in t or 'exit' in t):act('x','wait:1.5','down','down','c','wait:1.5');t=read().lower()
 if 'cancel' in t and t.count('hp')>=5:act('x','wait:1.3','down','c','wait:1.5');t=read().lower()
 if 'field notes' in t or 'pulse dex' in t:act('x','wait:1.3','up','c','wait:1.5');t=read().lower()
 if not ('sort' in t or 'close bag' in t or 'close aoc' in t or sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3):raise SystemExit('Bag entry review')
for _ in range(9):
 r=snap()
 if any(v['text'].strip().lower()=='items' for v in r):break
 act('left','wait:0.4')
else:raise SystemExit('Items pocket review')
# New pickups are appended to this unsorted pocket. Approach its end, then use OCR.
act('up','wait:0.5')
subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),item],check=True)
act('c','wait:0.5');r=snap();print(' '.join(v['text'] for v in r),flush=True)
if not any(v['text'].strip(' •›>').lower() in ['use','ulse','uee','uze','lise','llse','p lise','p use'] for v in r):raise SystemExit('Use menu review')
act('c','wait:0.8');print(read(),flush=True)
act('c','wait:0.4');subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
