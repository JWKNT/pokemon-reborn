"""Buy a reviewed BP-store bundle through visible dialogue and the one-digit UI."""
from play import *
index,count,token=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3].lower()
assert 0<=index<=20 and 1<=count<=9
for _ in range(8):
 t=read();print(t,flush=True)
 if 'what would you like today' in t.lower():break
 if not any(s in t.lower() for s in ['obtained','obrtained','aster put','anything else','you have','welcome','here you can','points for','mints']):
  act('wait:.8');t=read()
 assert any(s in t.lower() for s in ['obtained','obrtained','aster put','anything else','you have','welcome','here you can','points for','mints']), 'Unexpected store screen'
 act('c','wait:.35')
else:raise SystemExit('Store menu not reached')
act(*[v for _ in range(index) for v in ('down:.12','wait:.13')],'wait:.2');t=read();print(t,flush=True)
assert re.sub('[^a-z]','',token) in re.sub('[^a-z]','',t.lower()),'Requested product not visible'
act('c','wait:.4');t=read();assert 'how many' in t.lower(),t
act('c','wait:.3',*[v for _ in range(count) for v in ('up:.12','wait:.13')],'wait:.2');snap()
act('c','wait:.6');t=read();print(t,flush=True)
assert 'obtained' in t.lower() or 'obrtained' in t.lower(),'Purchase receipt requires review'
