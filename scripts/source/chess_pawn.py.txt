from nav import *
from locate import locate
m,eid,n=map(int,sys.argv[1:4]);promotion=sys.argv[4] if len(sys.argv)>4 else None
for i in range(n):
 mm,sx,sy=locate(m);assert mm==m
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(sx),str(sy)],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];x,y=e['x'],e['y'];assert 'pbPushThisObject(8)' in str(e['list'])
 options=[]
 for px,py,d in [(x-1,y,'right'),(x+1,y,'left'),(x,y+1,'up')]:
  try:options.append((len(route(v,(px,py))),px,py,d))
  except ValueError:pass
 _,px,py,d=min(options)
 subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{px},{py}'],check=True)
 act(d,'c','wait:0.6');t=read();print(t,flush=True)
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('positions',{}).setdefault(str(m),{})[str(eid)]=[x,y-1];p.write_text(json.dumps(s))
 if i==n-1 and promotion:
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Bishop|Knight|Rook|Queen',promotion],check=True)
  s=json.loads(p.read_text());s['variables']['154']=['Bishop','Knight','Rook','Queen'].index(promotion)+1;p.write_text(json.dumps(s))
print('PAWN ROUTE DONE',flush=True)
