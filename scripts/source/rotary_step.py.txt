"""Cross a reviewed rotary and update navigation notes only after UI verification.
Args: MAP SX SY KEY TX TY SWITCH VALUE (true/false)
"""
from play import *
from locate import locate
m,sx,sy=map(int,sys.argv[1:4]);key=sys.argv[4];tx,ty,sw=map(int,sys.argv[5:8]);value=sys.argv[8]=='true'
assert key in ['up','down','left','right']
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{sx},{sy}'],check=True)
act(key,'wait:1.8')
actual=locate(m);print('ROTARY',actual,'EXPECTED',(m,tx,ty),flush=True)
if actual!=(m,tx,ty):raise SystemExit('Unexpected rotary destination')
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('switches',{})[str(sw)]=value;p.write_text(json.dumps(s))
