"""Apply a reviewed, finite recovery plan through normal field bag menus.
Input JSON is a list of {item, target}; stops on unexpected receipts or menus.
"""
from play import *
plan=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert isinstance(plan,list) and 1<=len(plan)<=12
for step in plan:
 assert set(step)=={'item','target'} and step['item'] in ['Revive','Ultra Potion','Hyper Potion','Full Restore']
for i,step in enumerate(plan):
 if i:
  t=read().lower();assert re.search(r'hp [wmu]as res\s*tored',t),('Recovery receipt review',t)
  act('c','wait:.5','x','wait:.5');t=read().lower()
  assert 'sort' in t or 'close bag' in t,('Return to bag review',t)
 args=[sys.executable,str(ROOT/'scripts/field_medicine.py'),step['item'],step['target']]
 if i:args.append('--bag-open')
 subprocess.run(args,check=True)
t=read().lower();assert re.search(r'hp [wmu]as res\s*tored',t),('Final recovery receipt review',t)
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
print('REVIEWED FIELD RECOVERY COMPLETE',flush=True)
