from play import *
_play_act=act
def act(*keys):
 # Let repeated grid arrows settle, as in the verified PC/party picker helpers.
 _play_act(*[v for k in keys for v in ((k,'wait:.15') if k.startswith(('up','down','left','right')) else (k,))])
a,b=map(int,sys.argv[1:3]);assert 0<=a<6 and 0<=b<6 and a!=b
if '--party-open' not in sys.argv:
 subprocess.run([sys.executable,str(ROOT/'scripts/party_open.py')],check=True)
t=read().lower()
if not ('cancel' in t and t.count('hp')>=5):raise SystemExit('Party entry review')
act(*(['down:0.12']*(a//2)),*(['right:0.12'] if a%2 else []),'a','wait:0.4')
seq=[]
if b%2!=a%2:seq.append('right' if b%2 else 'left')
seq+=['down' if b//2>a//2 else 'up']*abs(b//2-a//2)
act(*[k+':0.12' for k in seq],'c','wait:1.2');print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
