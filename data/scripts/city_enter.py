"""Select a simple installed city doorway to a requested map and verify transfer."""
from nav import *
from locate import locate
m,n=map(int,sys.argv[1:3]);arrival=tuple(map(int,sys.argv[4:6])) if len(sys.argv)>3 and sys.argv[3]=='--arrival' else None
a,x,y=locate(m);assert a==m
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),str(x),str(y)],stderr=subprocess.DEVNULL));opts=[]
for eid,e in v['events'].items():
 cs=e['list']or[];ds=[tuple(c['parameters'][1:4])for c in cs if c['code']==201 and c['parameters'][0]==0]
 if not ds or any(d[0]!=n for d in ds):continue
 if arrival and not any(d[1:]==arrival for d in ds):continue
 if any(c['code']in[102,103,104,301]or any(w in str(c.get('parameters'))for w in ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle'])for c in cs):continue
 sides=[]
 for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
  try:sides.append(len(route(v,(e['x']+dx,e['y']+dy))))
  except ValueError:pass
 if sides:opts.append((min(sides),int(eid)))
assert opts,('No simple reviewed doorway',m,n)
_,eid=min(opts);print('CITY DOOR',m,eid,'->',n,flush=True)
for attempt in range(30):
 began=time.time();rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),str(m),str(eid),'enter'])
 if rc==0:break
 # A held approach can cross the doorway before q.py's last coordinate check.
 # Accept only an observed arrival on the explicitly requested destination.
 if locate()[0]==n:
  print('Doorway crossed during approach; destination verified',flush=True)
  break
 text=read().lower()
 if m in [570,531,533] and 'fight' in text and 'hp' in text and 'cofagrig' in text:
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(began)],check=True);continue
 raise SystemExit('City doorway interruption requires review: '+text)
else:raise SystemExit('City doorway escape retry bound')
actual=locate(n);assert actual[0]==n,actual
print('CITY TRANSFER VERIFIED',actual,flush=True)
