"""Normal UI EV Tuner: reviewed stat order and explicit two selected stats."""
from play import *
a,b=map(int,sys.argv[1:3]);assert a!=b and 0<=a<6 and 0<=b<6
r=read();print(r,flush=True);assert any(w in r.lower() for w in ['first','firgt']) and 'stat' in r.lower(),r
act(*[v for _ in range(a)for v in ('down:.12','wait:.14')],'c','wait:.4');r=read();print(r,flush=True);assert 'second' in r.lower(),r
act(*[v for _ in range(b)for v in ('down:.12','wait:.14')],'c','wait:.4');r=read();print(r,flush=True);assert any(w in r.lower() for w in ['swap','suap']) and 'stat' in r.lower(),r
# Long stat names paginate before the Yes/No choices on the party screen.
# Advance only this already verified swap question; generic dialogue rejects HP.
if not all(re.search(r'(?im)^\s*[ •›>]*'+label+r'\s*$',r) for label in ['Yes','No']):
 act('c','wait:.4');r=read();print(r,flush=True)
if not any(w in r.lower() for w in ['swapped','suapped']):
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
r=read();print(r,flush=True);assert any(w in r.lower() for w in ['swapped','suapped']),r
act('c','wait:.4');print(read(),flush=True)
# Installed handler displays a modal EV totals window after the result.
# Close that window before the consumable's final-use message or party menu.
act('c','wait:.4');r=read();print(r,flush=True)
if 'used your last' in r.lower():act('c','wait:.4')
