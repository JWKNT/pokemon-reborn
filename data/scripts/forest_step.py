"""Walk one preplanned forest stage; update only the navigation model afterward."""
from play import *
i=int(sys.argv[1]);goals=[(30,16),(11,27),(37,22),(15,30),(52,33),(41,26),(51,16),(41,26)]
assert 0<=i<8
x,y=goals[i]
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'234,{x},{y}'],check=True)
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v.setdefault('variables',{})['145']=i+1;p.write_text(json.dumps(v));print('Forest stage reached',i+1,flush=True)
