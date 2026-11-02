"""Finish a publicly visible Mirage Rock Smash prompt and its damage dialogue."""
from play import *
from locate import locate
mid,eid=map(int,sys.argv[1:3]);assert mid in [674,677,707]
e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL))['events'][str(eid)]
assert 'Kernel.pbRockSmash' in str(e['list']) and 'pbFieldDamage' in str(e['list'])
t=read().lower();compact=re.sub('[^a-z]','',t)
if 'shatteredglasshurt' not in compact:
 assert 'rock smash' in t and 'yes' in t and 'no' in t,t
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
hurt=False; last='--last' in sys.argv; used=False; blank=0
assert not last or mid==707
for i in range(16):
 t=read();l=' '.join(t.lower().split());print(t,flush=True)
 if 'shatteredglasshurt' in re.sub('[^a-z]','',l):
  hurt=True;act('c','wait:.6');continue
 if 'used rock smash' in l or 'would you like' in l:used=True;act('c','wait:.7');continue
 if last and any(w in l for w in ['taka:', 'intervention', 'get you help', 'punching addiction', 'destructive impulses', 'hole leads downwards', 'have to go down']):act('c','wait:.7');continue
 if l.replace('pokemon reborn','').strip() in ['', '•']:
  blank+=1
  if hurt or (last and used and blank>=4):break
  act('wait:.5');continue
 raise AssertionError(('Unexpected glass dialogue',t))
else:raise AssertionError('Glass tail limit')
assert (hurt or (last and used)) and locate(mid)[0]==mid
subprocess.run([sys.executable,str(ROOT/'scripts/mark_event.py'),str(mid),str(eid),'B' if last else ('A' if mid in [677,707] else 'B')],check=True)
print('GLASS BREAK OBSERVED',mid,eid,flush=True)
