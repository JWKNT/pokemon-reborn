# Queue steps written as MAP,X,Y,action,...; actual coordinates read in-game.
import json,sys,pathlib,subprocess
p=pathlib.Path(__file__).resolve().parent.parent/'notes/route-next.json'
steps=[]
for s in sys.argv[1:]:
 a=s.split(','); m,x,y=map(int,a[:3]);steps.append([m,0,0,x,y,a[3:]])
p.write_text(json.dumps(steps))
raise SystemExit(subprocess.call([sys.executable,str(p.parent.parent/'scripts/queue_route.py'),str(p)]))
