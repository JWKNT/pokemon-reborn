"""Normal-key wall walking after a visibly activated Subseven statue.
No game memory/save writes. Explicit statue origin and target are required.
Coordinates come from the game's public coordinate popup; radius is installed rule.
"""
from play import *
from locate import locate
ax,ay,tx,ty=map(int,sys.argv[1:5])
assert 0<=tx<160 and 0<=ty<120 and abs(tx-ax)+abs(ty-ay)<=9
m,x,y=locate(871);assert m==871 and abs(x-ax)+abs(y-ay)<=8
from collections import deque
last=None
for i in range(18):
 if (x,y)==(tx,ty):print('PHASE LEG VERIFIED',m,x,y,flush=True);break
 assert abs(x-ax)+abs(y-ay)<=8, 'Phase radius exhausted before target'
 # Reconcile a possible one-tile approach difference without leaving the
 # installed radius before the terminal landing. No ordinary-wall assumptions.
 start=(x,y);queue=deque([start]);prev={start:None}
 while queue and (tx,ty) not in prev:
  u=queue.popleft()
  for key,dx,dy in [('up',0,-1),('down',0,1),('left',-1,0),('right',1,0)]:
   n=(u[0]+dx,u[1]+dy)
   if not(0<=n[0]<160 and 0<=n[1]<120) or n in prev:continue
   if abs(n[0]-ax)+abs(n[1]-ay)>8 and n!=(tx,ty):continue
   prev[n]=(u,key);queue.append(n)
 assert (tx,ty) in prev, 'No legal radius path'
 keys=[];u=(tx,ty)
 while prev[u]:u,key=prev[u];keys.append(key)
 keys=keys[::-1][:6]
 act(*[z for key in keys for z in (key+':.08','wait:.16')])
 text=read().lower()
 assert not any(z in text for z in ['fight','would you','lukah:','taka:']), 'Public scene interruption'
 last=(x,y);m,x,y=locate(871)
 assert (x,y)!=last, 'No public movement; review statue activation'
 assert abs(x-ax)+abs(y-ay)<=9, 'Unexpected movement'
else:raise SystemExit('Phase leg bound')
