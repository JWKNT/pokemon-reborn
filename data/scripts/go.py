from nav import *
goal=tuple(map(int,sys.argv[1:3]));expected=None
for attempt in range(4):
 r=snap();s=' '.join(a['text'] for a in r).lower()
 if any(t in s for t in [' hp','fight','pokedex','pokédex','choose','select floor']) or any(a['y']>.73 for a in r):
  print('Review screen:',s,flush=True);raise SystemExit(2)
 act('d','wait:1','c','wait:1','c');v=loadmap()
 if expected is None:expected=v['map']
 if v['map']!=expected:raise SystemExit('Map changed; review')
 print('Verified',v['map'],v['position'],flush=True)
 if tuple(v['position'])==goal:
  if '--then' in sys.argv:act(*sys.argv[sys.argv.index('--then')+1:]);print(read(),flush=True)
  raise SystemExit(0)
 rc=subprocess.run([sys.executable,str(ROOT/'scripts/nav.py'),*map(str,goal),'--go']).returncode
 if rc:raise SystemExit(rc)
raise SystemExit('Route did not arrive after retries')
