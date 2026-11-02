from play import *
import nav
def run(*a):subprocess.run([sys.executable,str(ROOT/'scripts'/a[0]),*a[1:]],check=True)
def state(var=None,sw=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables'].update(var or {});v['switches'].update(sw or {});p.write_text(json.dumps(v))
run('q.py','325,13,19,down,wait:2')
run('eventq.py','324','53','enter')
run('eventq.py','328','22','enter')
run('q.py','329,25,19,down,wait:1')
state({'159':12});run('linear_dialog.py','329','15','--active','--burst')
run('eventq.py','331','9','talk');run('choose_dialog.py','Yes|No','Yes')
run('linear_dialog.py','331','9','--active','--past-choice','--burst')
state({'159':14},{'432':True});nav.save();print(read(),flush=True)
run('eventq.py','331','2','enter')
run('q.py','330,24,36','330,38,36','330,38,32','330,42,32','330,42,25','330,46,25','330,46,20','330,48,20,right,wait:2')
