"""Finish the observed David victory and reach Devon's PC using native inputs."""
from play import ROOT,read,act
from locate import locate
import subprocess,sys,json

def run(s,*args):
    subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)

run('victory_outro.py')
run('linear_dialog.py',626,7,'--active','--past-battle','--burst')
run('trainer_music.py','finish','--world-verified')
run('mark_event.py',626,7)
run('devon_walk.py',626,2,4,'--go')
run('eventq.py',626,3,'enter')
run('linear_dialog.py',627,3,'--active','--burst')
v=json.loads((ROOT/'notes/navigation-state.json').read_text());v['variables']['339']=26;(ROOT/'notes/navigation-state.json').write_text(json.dumps(v))
run('q.py','627,5,8')
act('right:.12','wait:3');print(read(),flush=True)
v=json.loads((ROOT/'notes/navigation-state.json').read_text());v['variables']['339']=27;(ROOT/'notes/navigation-state.json').write_text(json.dumps(v))
run('linear_dialog.py',627,4,'--active','--burst')
assert locate(628)==(628,30,8),'Devon trap transfer requires review'
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text())
v['variables']['339']=28;v.setdefault('switches',{})['777']=False
p.write_text(json.dumps(v))
run('devon_pc_prepare.py')
print('DAVID CLEARED; VICTORIA ROSTER SAVED AT PC',flush=True)
