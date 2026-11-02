from nav import *
from locate import locate
m,x,y=locate(805);assert m==805 and y>=66
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'805',str(x),str(y)],stderr=subprocess.DEVNULL))
p=route(v,(49,62));assert len(p)<=30 and all(k in ['up','down','left','right']for k in p)
print('CONTINUOUS EXIT',p,flush=True)
act(*[k+':.12'for k in p],'right:.18','c','wait:.8')
print(read(),flush=True)
