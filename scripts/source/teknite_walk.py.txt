"""Normal Teknite navigation with public wild interruptions fled and replanned.
Only reviewed Teknite maps with no trainer encounters may use this wrapper.
"""
from play import *
m=int(sys.argv[1]);assert m in [638,639,640,641,643,644,646,647,648,650]
for retry in range(20):
 started=time.time()
 rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),*sys.argv[1:]],env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84',REBORN_COORD_CACHE='1'))
 if rc==0:break
 if rc!=2:raise SystemExit(rc)
 t=read().lower()
 assert any(z in t for z in ['wild','fight',' hp']), 'Non-battle route interruption: '+t
 subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(started)],check=True)
else:raise SystemExit('Wild route retry limit')
