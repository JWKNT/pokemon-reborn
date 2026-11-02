"""Register the owned Good Rod through the normal Bag menu."""
from play import *
if '--bag-open' not in sys.argv:act('x','wait:.5','c','wait:1.5')
t=read().lower()
if 'cancel' in t and t.count('hp')>=5:act('x','wait:1','down','c','wait:1.5');t=read().lower()
assert 'sort' in t or 'close bag' in t or sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3,t
for _ in range(9):
 t=read().lower()
 if 'key items' in t:break
 act('right','wait:.4')
else:raise SystemExit('Key Items not found')
subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),'Good Rod','--single-step'],check=True)
act('c','wait:.5');t=read().lower();assert 'register' in t and 'favorite' in t,t
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Use|Register|Favorite|Cancel','Register'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
