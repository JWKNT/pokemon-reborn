"""Complete two reviewed noncombat Santiago pages from a verified quest checkpoint."""
from nav import *
from locate import locate
for page,label in [(2,'League220-RoofUnlockedConfirmed')]:
 mid,x,y=locate(532);assert mid==532
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'532',str(x),str(y)],stderr=subprocess.DEVNULL))
 e=v['events']['8'];assert not any('pbTrainerBattle' in str(c['parameters'])for c in e['list'])
 assert any(c['code']==123 for c in e['list']) if page==1 else any(c['code']==121 and c['parameters'][:2]==[713,713] for c in e['list'])
 opts=[]
 for dx,dy,k in [(0,1,'up'),(0,-1,'down'),(1,0,'left'),(-1,0,'right')]:
  p=(e['x']+dx,e['y']+dy)
  try:opts.append((len(route(v,p)),p,k))
  except ValueError:pass
 assert opts,'No source-reviewed non-x8 approach'
 _,p,k=min(opts)
 subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'532,{p[0]},{p[1]},{k},c,wait:1'],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),'532','8','--source-page',str(page),'--burst'],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
 if page==2:assert json.loads((ROOT/'notes/navigation-state.json').read_text())['switches']['713'] is True
