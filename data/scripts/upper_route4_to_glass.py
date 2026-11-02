"""Four reviewed normal rock climbs, then Hardy's entrance survey.
Stops at the bet so the choice is selected from visible labels.
"""
from play import *
from locate import locate

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
if '--hardy-pending' not in sys.argv:
 for mid,eid,nextmap in [(710,2,711),(711,3,713),(713,5,714),(714,3,715)]:
  run('eventq',mid,eid,'talk');run('dialog','--limit=10')
  actual=locate(nextmap);assert actual[0]==nextmap,(mid,eid,actual)
run('eventq',715,69,'talk')
run('choose_dialog','Yes|No','Yes','--source',715,69)
run('linear_dialog',715,69,'--active','--past-choice')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['391']=4;v['switches']['938']=True;p.write_text(json.dumps(v))
run('eventq',715,60,'enter')
run('linear_dialog',731,6,'--active','--burst','--world-settle',30)
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['391']=6;p.write_text(json.dumps(v))
print('GLASS ENTRANCE SURVEY READY FOR REVIEW',flush=True)
