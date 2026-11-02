"""Execute the walkthrough's first four Devon monitors with verified landings.
Normal native controls only. Source-driven switches below are planning notes.
Stops at the spinner entrance; rotating spinners require a separate model.
"""
from play import ROOT,read,act
from locate import locate
import subprocess,json,sys

def run(s,*args):
    subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
def state():return json.loads((ROOT/'notes/navigation-state.json').read_text())
def write(v):(ROOT/'notes/navigation-state.json').write_text(json.dumps(v))

assert state()['variables']['339']==33,'Victoria victory phase required'
if not state().get('self_switches',{}).get('630,24,A'):
    run('linear_dialog.py',630,24,'--active','--burst')
    v=state();v['variables']['342']=v['variables']['342']%3+1
    v.setdefault('self_switches',{})['630,24,A']=True;write(v)
    # Capture the actual radio after the intro and any pending field trigger.
    run('checkpoint.py','Devon-first-puzzle-radio-ready')
assert locate(630)[0]==630

for eid,x,y,sw in [(28,24,23,746),(22,18,19,747),(28,24,23,746),(62,8,14,748),(63,27,14,749)]:
    run('devon_walk.py',630,x,y,'--go','--conveyors')
    model=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'630',str(x),str(y)],stderr=subprocess.DEVNULL))
    ev=model['events'][str(eid)]
    assert (ev['x'],ev['y'])==(x,y-1)
    cs=ev['list'];assert not any(c['code'] in [101,102,201,301] for c in cs)
    assert [c['parameters'] for c in cs if c['code']==121]==[[sw,sw,1],[sw,sw,0]]
    act('up:.12','c','wait:.5');print(read(),flush=True)
    assert locate(630)==(630,x,y)
    v=state();v.setdefault('switches',{})[str(sw)]=not v.get('switches',{}).get(str(sw),False);write(v)
    print('DEVON MONITOR VERIFIED',eid,sw,v['switches'][str(sw)],flush=True)

run('devon_walk.py',630,4,4,'--go','--conveyors')
print('DEVON FIRST MONITORS COMPLETE; SPINNER ENTRANCE VERIFIED',flush=True)
