"""Execute a reviewed offline puzzle plan with bounded normal UI controls."""
import os
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
from play import *
from locate import locate
planpath=pathlib.Path(sys.argv[1]);plan=json.loads(planpath.read_text());actions=plan['actions'];i=int(sys.argv[2])if len(sys.argv)>2 else 0
receipt=planpath.with_suffix('.progress.json')
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
def phase(mid,ax,ay,x,y):run('distorted_phase_walk.py',mid,ax,ay,x,y)
def q(mid,x,y):run('q.py',f'{mid},{x},{y}')
while i<len(actions):
 a=actions[i];kind,mid=a[:2];print('ACTION',i,a,flush=True)
 if kind in ['walk','phase']:
  j=i
  while j+1<len(actions)and actions[j+1][:2]==a[:2]and(kind=='walk'or actions[j+1][5:]==a[5:]):j+=1
  x,y=actions[j][3:5]
  if kind=='walk':q(mid,x,y)
  else:
   try:phase(mid,*a[5:7],x,y)
   except subprocess.CalledProcessError:
    # A normal diagonal stair may finish a phase leg on an already reviewed
    # following walk tile. Accept only that exact public landing outside the
    # phase radius, before any further interaction; otherwise retain the stop.
    actual=locate(mid);matched=None
    if actual[0]==mid and abs(actual[1]-a[5])+abs(actual[2]-a[6])>8:
     for k in range(j+1,len(actions)):
      b=actions[k]
      if b[0]!='walk' or b[1]!=mid:break
      if tuple(b[3:5])==actual[1:]:matched=k;break
    if matched is None:raise
    print('VERIFIED FOLLOWING WALK LANDING',actual,'resume after',matched,flush=True);j=matched
  i=j+1
 else:
  _,_,eid,x,y,*origin=a
  assert locate()==(mid,x,y),'Interaction origin mismatch'
  e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(mid),str(eid)],stderr=subprocess.DEVNULL));ex,ey=e['x'],e['y'];assert abs(ex-x)+abs(ey-y)==1
  # The preceding phase path supplies the current statue origin.
  old=actions[i-1][5:7]if i and actions[i-1][0]=='phase'else None
  if old and abs(x-old[0])+abs(y-old[1])<=8:
   bx,by=2*x-ex,2*y-ey
   assert abs(bx-old[0])+abs(by-old[1])<=8, "Facing approach would exhaust phase"
   phase(mid,*old,bx,by);phase(mid,*old,x,y)
  else:
   facing='right'if ex>x else'left'if ex<x else'down'if ey>y else'up'
   act(facing)
  act('c','wait:.7');t=read();print(t,flush=True)
  if kind=='malamar':
   assert 'malamar' in t.lower(),'Expected Malamar'
   act('c','wait:1.5');t=read();print(t,flush=True)
   if 'room inverted' in t.lower():act('c','wait:.5')
   elif len(t.splitlines())>2:raise SystemExit('Unexpected inversion scene')
   assert locate()==(1781-mid,x,y),'Inversion coordinate mismatch'
  else:
   assert len(t.splitlines())<=2,'Unexpected statue dialogue'
   assert locate()==(mid,x,y),'Statue position changed'
  i+=1
 receipt.write_text(json.dumps(dict(plan=str(planpath),next_action=i,last_completed=actions[i-1],epoch=time.time()),indent=2))
print('PUZZLE PLAN COMPLETE',plan['end'],flush=True)
