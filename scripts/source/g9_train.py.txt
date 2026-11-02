"""Apply the reviewed latest-save level65 candy plan through ordinary bag menus."""
from play import *
plan=json.loads((ROOT/'work/g9-candy-plan.json').read_text())
assert sum(p['candies'] for p in plan)<=37
act('x','wait:0.5','c','wait:1.6');t=read().lower()
if 'cancel' in t and t.count('hp')>=5:act('x','wait:1.6','down','c','wait:1.6');t=read().lower()
if 'field notes' in t or 'pulse dex' in t:act('x','wait:1.6','up','c','wait:1.6');t=read().lower()
if 'sort' not in t:raise SystemExit('Bag entry review')
if 'medicine' not in t:
 act('right','wait:1');t=read().lower()
 if 'medicine' not in t:raise SystemExit('Medicine pocket review')
for p in plan:
 if not p['candies']:continue
 print('TRAIN',p['name'],p['candies'],flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/candy_batch.py'),p['name'],str(p['candies']),'L'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
print('LEVEL65 CANDY PLAN COMPLETE',flush=True)
