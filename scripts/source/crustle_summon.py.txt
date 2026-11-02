"""Summon and sleep an installed Route2 Crustle; update planning notes only after UI proof."""
from play import *
m,eid=map(int,sys.argv[1:3]);assert m==360 and eid in [198,123,137]
p=ROOT/'notes/navigation-state.json';state=json.loads(p.read_text());ground=state['switches']['410']
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];x,y=e['x'],e['y'];assert state['switches'].get('464')
def run(s,*args):
 r=subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],capture_output=True,text=True);print(r.stdout,flush=True)
 if r.returncode:raise SystemExit(r.stderr or 'Helper review')
 return r.stdout
run('layer_walk',m,x,y+2,int(ground));act('up','c','wait:.7')
t=read().lower()
if 'emerged' not in t:raise SystemExit('Crustle summon review: '+t)
run('dialog','--limit=8');act('c','wait:.5');t=run('choose_dialog','Yes|No','Yes')
if 'fell asleep' not in t.lower():raise SystemExit('Sleep result review')
act('c','wait:.8');print(read(),flush=True)
state=json.loads(p.read_text());state.setdefault('positions',{}).setdefault(str(m),{})[str(eid)]=[x,y+2];state.setdefault('self_switches',{})[f'{m},{eid},B']=True;state['switches']['464']=False;p.write_text(json.dumps(state));print('CRUSTLE ASLEEP',eid,x,y+2,flush=True)
