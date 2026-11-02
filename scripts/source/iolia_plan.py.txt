"""Read-only combined valley planner; prints reachable event approaches."""
from nav import *
OFF={333:0,334:42,335:65}
def combined(mid,x,y,extra=None,erased=()):
 maps={m:json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0',json.dumps(extra or {})],stderr=subprocess.DEVNULL)) for m in OFF}
 w=60;h=125;v=dict(maps[333]);v['height']=h;v['map']=999;v['position']=[x,y+OFF[mid]];v['data']={'dims':[w,h,3],'data':[0]*(w*h*3)};v['events']={}
 for m,a in maps.items():
  for z in range(3):
   src=a['data']['data'][w*a['height']*z:w*a['height']*(z+1)];start=w*h*z+w*OFF[m];v['data']['data'][start:start+len(src)]=src
  for eid,e in a['events'].items():
   if (m,int(eid)) in erased:continue
   ee=dict(e);ee['y']+=OFF[m];v['events'][f'{m}:{eid}']=ee
 return v
if __name__=='__main__':
 mid,x,y=map(int,sys.argv[1:4]);extra=json.loads(sys.argv[4]) if len(sys.argv)>4 else {};erased=[tuple(x) for x in json.loads(sys.argv[5])] if len(sys.argv)>5 else []
 v=combined(mid,x,y,extra,erased);d=route(v,None)
 out=[]
 for k,e in v['events'].items():
  st=str(e['list'])
  if not any(t in st for t in ['Key reacted','pbRockSmash','201','pbTrainer','CRYSTALPLUG','DUSKSTONE']):continue
  opts=[(d[p],p) for p in [(e['x']+1,e['y']),(e['x']-1,e['y']),(e['x'],e['y']+1),(e['x'],e['y']-1)] if p in d]
  if not opts:continue
  n,p=min(opts);m=int(k.split(':')[0]);out.append((n,k,(e['x'],e['y']-OFF[m]),(p[0],p[1]-OFF[m]),e['name'],st[:180]))
 for row in sorted(out):print(row)
 print('REACHABLE',len(d))
