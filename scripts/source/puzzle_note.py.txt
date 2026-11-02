"""Track an actually pressed library monitor in navigation notes; never writes game data."""
import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent.parent
f=root/'notes/navigation-state.json';s=json.loads(f.read_text());v=s.setdefault('variables',{});sw=s.setdefault('switches',{})
for n in [97,98,99,100,101,102,103,319,320]:v.setdefault(str(n),0)
e=json.loads(subprocess.check_output(['ruby',str(root/'scripts/event_dump.rb'),'182',sys.argv[1]],stderr=subprocess.DEVNULL))
def valid(c):
 return (not c['switch1_valid'] or sw.get(str(c['switch1_id']),False)) and (not c['switch2_valid'] or sw.get(str(c['switch2_id']),False)) and (not c['variable_valid'] or v.get(str(c['variable_id']),0)>=c['variable_value'])
p=next(p for p in reversed(e['pages']) if valid(p['condition']))
branches={}
for c in p['list']:
 code,i,a=c['code'],c['indent'],c['parameters'];parent=all(branches.get(j,True) for j in range(i))
 if code==111:
  if not parent:branches[i]=False;continue
  assert a[0]==1 and a[2]==0,a
  x=v.get(str(a[1]),0);y=a[3];branches[i]=[x==y,x>=y,x<=y,x>y,x<y,x!=y][a[4]]
 elif code==411:branches[i]=not branches[i]
 elif code==412:branches.pop(i,None)
 elif parent and code==122:
  assert a[3]==0 and a[2] in [0,1,2],a
  for n in range(a[0],a[1]+1):v[str(n)]=a[4] if a[2]==0 else v.get(str(n),0)+(a[4] if a[2]==1 else -a[4])
 elif parent and code==121:
  for n in range(a[0],a[1]+1):sw[str(n)]=a[2]==0
f.write_text(json.dumps(s));print('MONITOR',sys.argv[1],{k:v[k] for k in ['97','98','99','100','101','102','103','319','320']})
