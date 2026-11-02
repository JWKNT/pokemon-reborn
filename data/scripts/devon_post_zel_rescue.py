"""Reviewed post-ZEL rescue via ordinary controls; no game data writes."""
from play import ROOT,act
from locate import locate
import json,subprocess,sys

def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/name),*map(str,args)],check=True)

def phase(value):
 # Observed linear source completion updates the planner only.
 p=ROOT/'notes/navigation-state.json';d=json.loads(p.read_text())
 d['variables']['339']=value;p.write_text(json.dumps(d))

assert json.loads((ROOT/'notes/navigation-state.json').read_text())['variables']['339']==39
assert locate()[0]==632
run('eventq.py',632,8,'talk')
run('linear_dialog.py',632,8,'--active','--burst')
phase(40)
run('eventq.py',632,1,'enter')
run('devon_spinners.py','--map',631,'--monitor',124,'--activate','--go')
run('devon_spinners.py','--map',631,'--goal',2,5,'--go')
run('eventq.py',631,10,'enter')
run('eventq.py',628,66,'talk')
run('linear_dialog.py',628,66,'--active','--burst','--log-scripted-bgm')
phase(44)
run('eventq.py',628,7,'enter')
run('checkpoint.py','Devon-allies-rescued')
s=json.loads((ROOT/'notes/Devon-allies-rescued-status.json').read_text())
assert s['map']==527
print('DEVON RESCUE AND RETURN TO CITY VERIFIED',flush=True)
