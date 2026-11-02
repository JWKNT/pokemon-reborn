"""Use an explicit medicine on one party member. Requires Pokemon menu remembered."""
from play import *
item,name=sys.argv[1:3]
act('x','wait:0.5','c','wait:1.6');t=read().lower()
if 'pokedex' in t and ('seen' in t or 'search' in t):
 act('x','wait:1','down','down','c','wait:1');t=read().lower()
if ('cancel' in t and t.count('hp')>=5):
 act('x','wait:1.6','down','c','wait:1.6');t=read().lower()
if 'field notes' in t or 'pulse dex' in t:
 act('x','wait:1.6','up','c','wait:1.6');t=read().lower()
if not ('sort' in t or 'close bag' in t):raise SystemExit('Bag entry review')
for _ in range(9):
 t=read().lower()
 if any(s in t for s in ['medicine','medieine','nedicine']):break
 act('right','wait:0.4')
else:raise SystemExit('Medicine pocket review')
scan=[sys.executable,str(ROOT/'scripts/bag_select.py'),item]
result=subprocess.run(scan)
if result.returncode==4:raise SystemExit('Item absent after a complete visible bag cycle; no item used')
if result.returncode:
 subprocess.run([*scan,'--single-step'],check=True)
act('c','wait:0.4','c','wait:0.8')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name,'--single'],check=True)
t=read();print(t,flush=True)
if not any(s in ''.join(t.lower().split()) for s in ['restored','reetored','revived','wokeup','cured','healthy',"won'thaveanyeffect"]):raise SystemExit('Medicine result review')
act('c','wait:0.6')
if 'used your last' in read().lower():act('c','wait:0.6')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
print(read())
