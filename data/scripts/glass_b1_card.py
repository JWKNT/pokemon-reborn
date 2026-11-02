"""Normal B1F ice bridges, Meteor Card, and opening Noel/Anna pods.
No optional trainer or pallet detours; stops at any unreviewed state.
"""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
def mirror(ss):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches'].update(ss);p.write_text(json.dumps(v))
for eid,sw in [(9,941),(10,942),(16,943)]:
 if not json.loads((ROOT/'notes/navigation-state.json').read_text())['switches'].get(str(sw)):
  run('eventq.py',732,eid,'talk');run('linear_dialog.py',732,eid,'--active');mirror({str(sw):True})
run('eventq.py',732,61,'enter');run('eventq.py',736,32,'item');run('eventq.py',736,75,'item')
for eid in [67,68]:
 run('eventq.py',736,eid,'talk');run('choose_dialog.py','Yes|No','Yes');run('linear_dialog.py',736,eid,'--active','--past-choice','--burst')
run('checkpoint.py','Glass-Meteor-Card-pods');print('METEOR CARD AND BOTH PODS OBSERVED',flush=True)
