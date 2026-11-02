"""Carry waiting Espeon through the inspected lift, avoiding companion-drop ladders."""
from play import *
from locate import locate
from glass_positions import refresh
def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],check=True)
assert locate(732)==(732,35,19)
act('right:.12','wait:.3','c','wait:1')
assert not read().strip().replace('Pokemon Reborn','').strip(),'Unexpected rejoin dialogue'
run('checkpoint.py','Glass-Espeon-rejoined-before-lift')
assert json.loads((ROOT/'notes/navigation-state.json').read_text())['switches']['947'],'Rejoin did not occur; no carry route sent'
# Walk the source-reviewed upper walkway; no ladder/companion-drop event.
f=ROOT/'notes/route-next.json';f.write_text(json.dumps([[732,35,19,6,19,[]]]))
run('queue_route.py',f)
run('eventq.py',732,70,'enter')
run('eventq.py',733,66)
run('choose_dialog.py','Ground Floor|B1F|B2F','B2F')
run('linear_dialog.py',733,66,'--past-choice')
run('eventq.py',733,67,'enter')
assert locate(732)==(732,6,24)
run('checkpoint.py','Glass-Espeon-carried-by-lift')
n=ROOT/'notes/navigation-state.json';v=json.loads(n.read_text())
assert v['switches']['947'] and v['switches']['410'] and not v['switches']['965'],'Native companion/floor evidence failed'
n.write_text(json.dumps(refresh(v,json.loads((ROOT/'work/story-map-732-events.json').read_text()))))
print('NATIVE ESPEON FOLLOWING ON B2F; LIFT CARRY VERIFIED',flush=True)
