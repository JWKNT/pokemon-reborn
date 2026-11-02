from nav import *
v=loadmap();x,y=map(int,sys.argv[1:3]);opts=[]
for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
 try:
  p=(x+dx,y+dy);opts.append((len(route(v,p)),p,k))
 except ValueError:pass
if not opts:raise SystemExit('No accessible side')
_,p,k=min(opts);print('APPROACH',p,'FACE',k,flush=True)
rc=subprocess.run([sys.executable,str(ROOT/'scripts/nav.py'),str(p[0]),str(p[1]),'--go']).returncode
if rc:raise SystemExit(rc)
if any(a in sys.argv for a in ['--item','--touch','--cut']):
 act('d','wait:1','c','wait:1','c');fresh=loadmap()
 if fresh['map']!=v['map'] or tuple(fresh['position'])!=p:raise SystemExit('Position differs; replan')
 if '--item' in sys.argv:
  if not any(e['x']==x and e['y']==y and 'pbItemBall' in str(e['list']) for e in fresh['events'].values()):raise SystemExit('No active item at target')
  act(k,'c','wait:0.8','x:2.5','wait:0.5')
 elif '--cut' in sys.argv:
  if not any(e['x']==x and e['y']==y and 'pbCut' in str(e['list']) for e in fresh['events'].values()):raise SystemExit('No Cut tree at target')
  act(k,'c','wait:0.7','c','wait:0.7','c','wait:0.7','c','wait:3')
 else:act(k,'wait:1')
 print(read(),flush=True)
