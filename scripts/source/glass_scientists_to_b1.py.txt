"""After an observed scientist victory, unlock the lift and take Glaceon to B1F."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
def mirror(ss=None,vv=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches'].update(ss or{});v['variables'].update(vv or{});p.write_text(json.dumps(v))
run('victory_outro.py');run('trainer_music.py','finish');run('linear_dialog.py',737,70,'--past-battle','--after-last-battle','--source-page',0)
run('eventq.py',737,69,'talk');run('linear_dialog.py',737,69,'--active');run('checkpoint.py','Glass-Scientists');run('glass_positions.py')
run('eventq.py',737,9,'enter');run('eventq.py',732,63,'talk');run('linear_dialog.py',732,63,'--active')
mirror({'946':True,'947':False},{'404':0,'405':0});run('eventq.py',732,73,'enter')
run('eventq.py',733,66,'talk');run('choose_dialog.py','Ground Floor|B1F|B2F','B1F');run('linear_dialog.py',733,66,'--past-choice','--active')
mirror(vv={'432':2});run('eventq.py',733,67,'enter');mirror({'410':False,'964':True,'965':True});print('NORMAL LIFT B1F EXIT OBSERVED',flush=True)
