from play import *
from locate import locate
import nav
m,x,y=locate(329)
if m!=329:raise SystemExit('Main Sanctum not reached')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches']['528']=True;p.write_text(json.dumps(v))
def run(*a):subprocess.run([sys.executable,str(ROOT/'scripts'/a[0]),*a[1:]],check=True)
run('field_medicine.py','Lemonade','Ampharos');act('c','wait:0.5','c','wait:1');print(read(),flush=True)
run('overworld.py');nav.save();print(read(),flush=True)
