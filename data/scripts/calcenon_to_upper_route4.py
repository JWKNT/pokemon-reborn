"""Reviewed Calcenon briefing, Hardy's HM gift, and first normal Rock Climb."""
from play import *
from locate import locate

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
if '--hardy-pending' not in sys.argv:
 if not any(z in sys.argv for z in ['--briefing-active','--after-choice']):run('eventq',413,67,'enter')
 # Entrance413E67 sets the transient house switch503; mirror observed transfer in route notes.
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches']['503']=True;p.write_text(json.dumps(v))
 if '--after-choice' not in sys.argv:run('choose_dialog','Yes|No','No','--source',417,23)
 run('linear_dialog',417,23,'--active','--past-choice','--log-scripted-bgm')
 run('checkpoint','Calcenon-Glass-briefing')
 run('eventq',417,6,'enter');run('eventq',413,21,'enter');run('eventq',418,2,'enter')
 run('use_field_item','Super Repel')
run('eventq',412,46,'talk');run('linear_dialog',412,46,'--active','--burst')
# This observed completed source event assigns391=3; only update route notes.
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['391']=3;p.write_text(json.dumps(v))
run('teach_machine','TMX9 Rock Climb','Swampert','Rock Climb',3)
run('eventq',412,1,'talk');run('dialog','--limit=10')
actual=locate(710);assert actual[0]==710,actual
print('UPPER ROUTE4 FIRST CLIMB VERIFIED',actual,flush=True)
