"""Play one bounded Rocket Hideout arrow route, checking actual landings."""
from glitch_spinner_plan import *
from locate import locate,capture_ready
tx,ty=map(int,sys.argv[1:3]);last=None;stalls=0
for _ in range(80):
 t=read().lower()
 if 'fight' in t or ' hp' in ' '.join(t.split()):raise SystemExit('Spinner battle review')
 compact=''.join(t.split())
 if 'repel' in compact and any(w in compact for w in ['woreoff','uoreoff']):
  subprocess.run([sys.executable,str(ROOT/'scripts/renew_repel.py')],check=True)
 m,x,y=locate(448);assert m==448
 if (x,y)==(tx,ty):print('SPINNER ROUTE COMPLETE',x,y,flush=True);break
 stalls=stalls+1 if last==(x,y) else 0;last=(x,y)
 if stalls>=3:raise SystemExit('Spinner landing review')
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'448',str(x),str(y)],stderr=subprocess.DEVNULL))
 steps=spinner_plan(v,(tx,ty));chunk=[]
 for s in steps:
  if ':'in s['key']:
   if not chunk:chunk.append(s)
   break
  chunk.append(s)
  if len(chunk)>=24:break
 seq=[]
 for s in chunk:
  if s['key'].startswith('spin:'):seq += [s['key'].split(':')[-1]+':.12',f"wait:{max(3,1+s['forced_tiles']*.25):.2f}"]
  else:seq.append(s['key']+':.12')
 print('SPINNER',chunk[0]['from'],'→',chunk[-1]['to'],len(chunk),'inputs',flush=True)
 try:act(*seq)
 except subprocess.CalledProcessError as e:
  if e.returncode!=2:raise
  capture_ready();continue
 r=snap();t=' '.join(z['text']for z in r).lower();compact=''.join(t.split())
 if 'repel'in compact and any(w in compact for w in ['woreoff','uoreoff']):continue
 if any(w in t for w in ['fight',' hp','yes','no'])or any(z['y']>.73 and len(z['text'])>22 for z in r):raise SystemExit('Spinner scene review: '+t)
else:raise SystemExit('Spinner route limit')
