"""Activate a reviewed statue while phased, without walking onto its event.
Approach from two tiles away so the final normal step sets the correct facing;
confirm is then sent separately. All positions are public coordinate checks.
"""
from play import *
from locate import locate
oldx,oldy,eid,px,py=map(int,sys.argv[1:6])
e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),'871',str(eid)],stderr=subprocess.DEVNULL))
cs=e['pages'][0]['list'];ex,ey=e['x'],e['y']
assert abs(ex-px)+abs(ey-py)==1
assert any(c['code']==122 and c['parameters'][:2]==[629,629] for c in cs)
assert not any(c['code'] in [102,103,104,301] for c in cs)
bx,by=2*px-ex,2*py-ey
assert abs(bx-oldx)+abs(by-oldy)<=8 and abs(px-oldx)+abs(py-oldy)<=8, 'Approach exceeds current phase radius'
for x,y in [(bx,by),(px,py)]:
 subprocess.run([sys.executable,str(ROOT/'scripts/subseven_phase_walk.py'),str(oldx),str(oldy),str(x),str(y)],check=True)
act('c','wait:1')
t=read();assert not re.search(r'\bhp\b|fight|yes|no',t,re.I),t
actual=locate(871);assert actual==(871,px,py),actual
print('STATUE CONFIRM FROM VERIFIED FACING',eid,'new origin',ex,ey,flush=True)
