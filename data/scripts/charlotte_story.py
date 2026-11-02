"""Reviewed Calcenon story progression, with the planned Charlotte answer."""
from play import *
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
def note(variable=None,value=None,switch=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text())
 if variable is not None:v['variables'][str(variable)]=value
 if switch is not None:v['switches'][str(switch)]=True
 p.write_text(json.dumps(v))
run('eventq.py',413,80,'enter');run('linear_dialog.py',419,8,'--burst')
note(184,17,492);run('q.py','419,9,61,down,wait:2')
run('eventq.py',413,51,'talk');run('choose_dialog.py','Yes|No','Yes')
run('linear_dialog.py',413,51,'--past-choice','--burst')
note(184,21,491)
run('eventq.py',413,21,'enter');run('eventq.py',418,4,'talk')
run('linear_dialog.py',418,4,'--active','--burst');note(184,22)
run('eventq.py',418,1,'enter');run('eventq.py',413,80,'enter')
print('CHARLOTTE STORY COMPLETE; GYM READY',flush=True)
