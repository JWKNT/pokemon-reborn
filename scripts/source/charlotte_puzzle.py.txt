"""Execute the published Charlotte puzzle solution with coordinate checks."""
from play import *
from locate import locate,capture_ready
import re
puzzles={
1:((9,55),'U2 L2 U3 R D R D R D R U2 L U L U',188),
2:((9,44),'U2 R U R2 D R U4 L2 D R D L2 U L D2 L U L D2 L2 U R U2 L U R4 U',189),
3:((9,32),'U2 L U L2 D L2 U R U L U R U2 L U2 R3 D2 L D R D2 R U R D R D2 R U R U R D2 R U3 L3 U L2 U L U R2 D R2 D R2 U3 L D L U L3 U',190)}
n=int(sys.argv[1]);start,solution,counter=puzzles[n]
keys={'U':('up',(0,-1)),'D':('down',(0,1)),'L':('left',(-1,0)),'R':('right',(1,0))}
steps=[];x,y=start
for token in solution.split():
 k,num=re.fullmatch(r'([UDLR])(\d*)',token).groups();key,(dx,dy)=keys[k]
 for _ in range(int(num or 1)):x+=dx;y+=dy;steps.append((key,(x,y)))
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'419',*map(str,start)],stderr=subprocess.DEVNULL))
gray={(e['x'],e['y'])for e in v['events'].values()if any(c['code']==122 and c['parameters'][:2]==[counter,counter] and c['parameters'][2]==1 for c in(e['list']or[]))}
visited=[p for k,p in steps if p in gray]
assert len(visited)==len(set(visited)),'Solution repeats a puzzle tile'
assert set(visited)==gray,('Uncovered puzzle tiles',gray-set(visited))
print('VALIDATED PUZZLE',n,'start',start,'end',(x,y),'steps',len(steps),'counter tiles',len(gray),flush=True)
if '--plan-only' in sys.argv:raise SystemExit(0)
def puzzle_locate():
 try:return locate(419)
 except SystemExit as error:
  if error.code==2 and 'repel' in read().lower():
   subprocess.run([sys.executable,str(ROOT/'scripts/renew_repel.py'),'--cancel'],check=True)
   return locate(419)
  raise
actual=puzzle_locate()
if '--resume' in sys.argv:
 candidates=([0] if actual==(419,*start) else [])+[j+1 for j,(_,point) in enumerate(steps) if actual==(419,*point)]
 assert len(candidates)==1,('Resume coordinate is not unique in the solution',actual,candidates)
 i=candidates[0];print('RESUMING PUZZLE at step',i,flush=True)
else:
 assert actual==(419,*start),'Puzzle start coordinate mismatch'
 i=0
while i<len(steps):
 chunk=steps[i:i+8]
 try:act(*[key+':.12'for key,p in chunk])
 except subprocess.CalledProcessError as error:
  if error.returncode!=2:raise
  capture_ready();actual=puzzle_locate()
  candidates=[j+1 for j,(_,point) in enumerate(steps) if (419,*point)==actual and i<=j+1<=i+len(chunk)]
  if actual==(419,*(start if i==0 else steps[i-1][1])):candidates.append(i)
  assert len(candidates)==1,('Interrupted puzzle coordinate review',actual,candidates)
  i=candidates[0];print('PUZZLE CAPTURE RECOVERED at step',i,flush=True);continue
 t=read().lower()
 if any(s in t for s in ['fight',' hp','yes','no']):raise SystemExit('Puzzle dialogue/battle review')
 actual=puzzle_locate();assert actual==(419,*chunk[-1][1]),(actual,chunk[-1][1])
 i+=len(chunk)
print('PUZZLE COMPLETE',n,(x,y),flush=True)
