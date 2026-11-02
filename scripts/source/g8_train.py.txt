"""Prepare the current six for the badge-seven cap through normal bag controls."""
from play import *
act('x','wait:0.5','c','wait:1.6');t=read().lower()
if 'cancel' in t and t.count('hp')>=5:act('x','wait:1.6','down','c','wait:1.6');t=read().lower()
if 'field notes' in t or 'pulse dex' in t:act('x','wait:1.6','up','c','wait:1.6');t=read().lower()
if 'sort' not in t:raise SystemExit('Bag review')
for name,n in [('Cofagrigus',5),('Drapion',7),('Klinklang',6),('Arcanine',7),('Swampert',6),('Ampharos',6)]:
 print('TRAIN',name,n,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/candy_batch.py'),name,str(n),'L'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
act('up','c','wait:1')
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=8'],check=True)
print('TEAM TRAINED AND HEALED',flush=True)
