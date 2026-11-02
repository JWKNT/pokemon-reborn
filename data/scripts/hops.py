from nav import *
# Each waypoint is immediately before a known, observed map doorway.
for spec in sys.argv[1:]:
 x,y,key=spec.split(',');save()
 result=subprocess.run([sys.executable,str(ROOT/'scripts/nav.py'),x,y,'--go'])
 if result.returncode: sys.exit(result.returncode)
 act(key,'wait:2');r=snap()
 print('HOP',spec,' '.join(a['text'] for a in r),flush=True)
 if any(a['y']>.73 and len(a['text'])>20 for a in r):sys.exit(2)
