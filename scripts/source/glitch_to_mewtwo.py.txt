"""Continue the inspected Glitch route, stopping before the Mewtwo interaction.

Resume at an explicitly named stage after reviewing any interruption. All progress
is through keyboard input; stage flags below update navigation notes only.
"""
from play import *
from locate import locate
def run(s,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def observed(values=None,switches=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text())
 v.setdefault('variables',{}).update({str(k):z for k,z in (values or {}).items()})
 v.setdefault('switches',{}).update({str(k):z for k,z in (switches or {}).items()});p.write_text(json.dumps(v))
def gate(mid,event,badge,value,transfer=None):
 rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(event),'enter' if transfer else 'talk'])
 t=read()
 gate_text=''.join(t.lower().split())
 if rc and badge.lower() not in t.lower() and 'youcanpasshere' not in gate_text:raise SystemExit('Unexpected badge-gate interruption')
 if transfer or badge.lower() in t.lower() or 'youcanpasshere' in gate_text:run('linear_dialog',mid,event,'--active','--burst')
 actual=locate()
 if transfer:assert actual[0]==transfer
 else:assert actual[0]==mid
 observed({193:value})
start=sys.argv[1] if len(sys.argv)>1 else 'moon'
stages=['moon','opal','rocket','lavender','standard','wasteland','mansion-switch','mansion-exit','citae','victory-road','mewtwo-prep']
assert start in stages
for stage in stages[stages.index(start):]:
 print('GLITCH ROUTE STAGE',stage,flush=True)
 if stage=='moon':run('party_lead','Hexan');run('eventq',445,13,'enter')
 elif stage=='opal':gate(447,19,'BLIGHT',37);run('eventq',447,20,'enter')
 elif stage=='rocket':run('glitch_spinner_walk',26,14);run('eventq',448,53,'enter')
 elif stage=='lavender':gate(449,2,'RIME',38)
 elif stage=='standard':gate(449,13,'STANDARD',39,450)
 elif stage=='wasteland':run('surface_event',450,4,'enter')
 elif stage=='mansion-switch':
  run('eventq',451,13,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',451,13,'--active','--past-choice','--burst');observed({193:40},{519:True})
 elif stage=='mansion-exit':run('eventq',451,11,'enter')
 elif stage=='citae':gate(452,3,'STRIKE',41,453)
 elif stage=='victory-road':run('eventq',453,3,'enter')
 elif stage=='mewtwo-prep':
  run('eventq',455,2,'talk');run('linear_dialog',455,2,'--active','--burst');run('mark_event',455,2)
  run('party_lead','Cofagrigus')
  run('surface_walk',455,36,21)
  run('checkpoint','Mewtwo-ready')
  print('MEWTWO PREBATTLE STOP',locate(),flush=True)
