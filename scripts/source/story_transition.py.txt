"""Play an inspected linear map scene and verify its destination before noting progress."""
from play import *
from locate import locate
mid,eid,dest,stage=map(int,sys.argv[1:5])
rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),'talk'])
if rc not in [0,2]:raise SystemExit(rc)
subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),str(mid),str(eid)],check=True)
a=locate(dest);print('SCENE DESTINATION',a,flush=True)
if a[0]!=dest:raise SystemExit('Unexpected scene destination')
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['149']=stage;p.write_text(json.dumps(s))
