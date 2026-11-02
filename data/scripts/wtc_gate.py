"""Activate a simple installed WTC panel; only commit notes after matching its real text."""
from play import *
from locate import locate
import difflib
mid,eid=map(int,sys.argv[1:3]);actual=locate(mid);assert actual[0]==mid
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(actual[1]),str(actual[2])],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];cs=e['list']or[]
assert not any(c['code']in[102,201,355,655]for c in cs),'Not a simple shutter/gate panel'
texts=[c['parameters'][0]for c in cs if c['code']==101];assert texts,'Already open or wrong layer'
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(eid),'talk'],check=True)
t=' '.join(read().upper().split());assert any(difflib.SequenceMatcher(None,x.upper(),t).ratio()>.55 or x.upper()in t for x in texts),('Panel confirmation not seen',t,texts)
subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),str(mid),str(eid)],check=True)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text())
for c in cs:
 if c['code']==121:
  a=c['parameters'];assert a[0]==a[1];s['switches'][str(a[0])]=a[2]==0
 if c['code']==122:
  a=c['parameters'];assert a[0]==a[1] and a[2]==0 and a[3]==0
  s.setdefault('variables',{})[str(a[0])]=a[4]
p.write_text(json.dumps(s));print('OBSERVED PANEL ACTIVATION',mid,eid,texts,flush=True)
