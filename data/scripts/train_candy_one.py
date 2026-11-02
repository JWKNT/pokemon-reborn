from play import *
import re
name,count,size=sys.argv[1:4]
act('x','wait:0.5','c','wait:1.6');t=read().lower()
if 'pokedex' in t and ('seen' in t or 'search' in t or 'exit' in t):act('x','wait:1','down','down','c','wait:1.6');t=read().lower()
if 'cancel' in t and t.count('hp')>=5:act('x','wait:1.6','down','c','wait:1.6');t=read().lower()
if 'field notes' in t or 'pulse dex' in t:act('x','wait:1.6','up','c','wait:1.6');t=read().lower()
if 'sort' not in t and sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())<3:raise SystemExit('Bag entry review')
for _ in range(8):
 if 'medicine' in t or 'medieine' in t:break
 act('right','wait:.5');t=read().lower()
else:raise SystemExit('Medicine pocket review')
subprocess.run([sys.executable,str(ROOT/'scripts/candy_batch.py'),name,count,size],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
