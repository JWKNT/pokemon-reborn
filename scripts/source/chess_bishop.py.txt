"""Execute the inspected bishop directional-input event through the game UI."""
from nav import *
m,eid=int(sys.argv[1]),int(sys.argv[2]);diag=sys.argv[3];n=int(sys.argv[4]);assert diag in ['ul','ur','dl','dr'] and 1<=n<=3
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];x,y=e['x'],e['y'];assert any(c['code']==105 for c in e['list'])
dx=-1 if diag[1]=='l' else 1;dy=-1 if diag[0]=='u' else 1
for _ in range(n):
 from locate import locate
 mm,sx,sy=locate(m);assert mm==m
 vv=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(sx),str(sy)],stderr=subprocess.DEVNULL));opts=[]
 for px,py,face,key in [(x-dx,y,'right' if dx==1 else 'left','up' if dy==-1 else 'down'),(x,y-dy,'up' if dy==-1 else 'down','right' if dx==1 else 'left')]:
  try:opts.append((len(route(vv,(px,py))),px,py,face,key))
  except ValueError:pass
 _,px,py,face,key=min(opts)
 subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{px},{py}'],check=True)
 act(face,'c','wait:0.4',key,'wait:0.6');print(read(),flush=True)
 x+=dx;y+=dy
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('positions',{}).setdefault(str(m),{})[str(eid)]=[x,y];p.write_text(json.dumps(s))
print('BISHOP MOVED; BOARD CHECK STILL REQUIRED',x,y,flush=True)
