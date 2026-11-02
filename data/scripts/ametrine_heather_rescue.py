"""Run the inspected refusal-route passage and linear Heather scenes via UI."""
from play import *
from locate import locate
def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],check=True)
def state(**values):
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text())
 s.setdefault('variables',{}).update({str(k):v for k,v in values.items()})
 p.write_text(json.dumps(s))
run('linear_dialog.py',457,30,'--active','--burst')
state(**{'193':18})
run('eventq.py',457,26,'enter')
assert locate()[0]==374
state(**{'185':0})
run('surface_event.py',374,31,'enter')
assert locate()[0]==440
run('eventq.py',440,2,'enter')
assert locate()[0]==439
run('eventq.py',439,66,'talk')
run('linear_dialog.py',439,66,'--active','--burst')
# The door scene automatically continues into Heather's shack and the rescue
# outside. All three linked events were inspected as linear, with no choices.
assert locate()[0]==439
state(**{'193':20})
print('HEATHER SHACK SCENE COMPLETE',locate(),flush=True)
