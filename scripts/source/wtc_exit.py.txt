"""Execute a simple WTC door and verify its installed destination; reset map positions.
The installed onMapChange clears moved events, so old coordinate notes cannot carry
between visits. Story autoruns are left for review if they block coordinates.
"""
from play import *
from locate import locate
mid,eid=map(int,sys.argv[1:3]);actual=locate(mid);assert actual[0]==mid
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(actual[1]),str(actual[2])],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
cs=e['list']or[];dest={tuple(c['parameters'][1:4])for c in cs if c['code']==201 and c['parameters'][0]==0}
assert len(dest)==1 and not any(c['code']in[102,355,655]for c in cs),'Not a simple door'
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),'enter'],check=True)
new=next(iter(dest));assert locate(new[0])==new,'Door destination review'
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.get('positions',{}).pop(str(new[0]),None);p.write_text(json.dumps(s));print('WTC DOOR AND FRESH MAP VERIFIED',mid,eid,new,flush=True)
