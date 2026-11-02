"""Advance only the department elevator clerk's reviewed greeting to its floor menu."""
from play import *
for _ in range(6):
 t=read().lower();print(t,flush=True)
 if 'which floor' in t:
  assert re.search(r'[1i]f\s*[-–]',t),'Numbered floor options missing'
  print('NUMBERED FLOOR MENU READY',flush=True);break
 assert any(z in re.sub('[^a-z]','',t) for z in ['membershipcard','excellentthankyou']),('Unexpected clerk text',t)
 act('c','wait:.65')
else:raise SystemExit('Elevator greeting limit')
