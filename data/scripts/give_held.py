from play import *
import re
item,name=sys.argv[1:3]
pocket=sys.argv[sys.argv.index('--pocket')+1] if '--pocket' in sys.argv else 'Items'
assert pocket in ['Items','Berries','Crystals']
initial=read().lower()
if 'fight' in initial or initial.count('hp')>=5:raise SystemExit('Held item helper requires overworld')
if '--bag-open' not in sys.argv:
 act('x','wait:0.5','c','wait:1.5');t=read().lower()
 if 'would you like to save' in t:
  act('x','wait:2','x','wait:2','x','wait:2',*(['up:0.22']*3),'c','wait:2');t=read().lower()
 if 'pokedex' in t and ('seen' in t or 'search' in t or 'exit' in t):act('x','wait:1.5','down','down','c','wait:1.5');t=read().lower()
 if 'cancel' in t and t.count('hp')>=5:act('x','wait:1.3','down','c','wait:1.5');t=read().lower()
 if 'field notes' in t or 'pulse dex' in t:act('x','wait:1.3','up','c','wait:1.5');t=read().lower()
 if not ('sort' in t or 'close bag' in t or 'close aoc' in t or sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3):raise SystemExit('Bag entry review')
for _ in range(9):
 r=snap()
 if any(v['text'].strip().lower() in ({'crystals','crustals'} if pocket=='Crystals' else {pocket.lower()}) for v in r):break
 act('left','wait:0.4')
else:raise SystemExit(pocket+' pocket review')
# New pickups are appended to this unsorted pocket. Approach its end, then use OCR.
act('up','wait:0.5')
subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),item,*(['--single-step'] if '--single-step' in sys.argv else [])],check=True)
act('c','wait:0.5');r=snap();t=' '.join(v['text'] for v in r);print(t,flush=True)
if not any(v['text'].strip(' •›>').lower()=='give' for v in r):raise SystemExit('Give menu review')
labels=(['Give','Toss','Favorite','Cancel'] if item=='Persim Berry' else ['Use','Give','Toss','Favorite','Cancel']) if pocket=='Berries' else ['Give','Toss','Cancel']
if pocket=='Berries':
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'|'.join(labels),'Give'],check=True)
else:act('c','wait:1.2')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name,'--single'],check=True)
t=read();print(t,flush=True)
if not any(s in t.lower() for s in ['hold','gave','given']):raise SystemExit('Held item result review')
act('c','wait:0.5');t=read();print(t,flush=True)
if 'switch the two items' in t.lower():
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
 act('c','wait:0.7');result=read();print(result,flush=True)
 if 'taken and replaced' in result.lower():act('c','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
