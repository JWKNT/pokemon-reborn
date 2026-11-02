"""Finish the reviewed first power panel and stop before Arclight's trigger."""
from play import ROOT
from locate import locate
import subprocess, sys, json

def run(name, *args):
    subprocess.run([sys.executable, str(ROOT/'scripts'/name), *map(str,args)], check=True)

assert locate(630) == (630,15,3)
run('eventq.py',630,44,'talk')
run('choose_dialog.py','Yes|No','Yes')
run('linear_dialog.py',630,44,'--active','--past-choice')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches']['1562']=True;p.write_text(json.dumps(v))
run('devon_walk.py',630,25,3,'--go','--conveyors')
run('eventq.py',630,3,'enter')
assert locate(628)==(628,30,24)
run('eventq.py',628,4,'enter')
assert locate(628)==(628,2,25)
run('checkpoint.py','Devon-first-puzzle-complete')
