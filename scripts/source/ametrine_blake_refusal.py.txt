"""Use the inspected apartment elevator and refuse Blake's ring deal three times."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
def stage(k,value):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables'][str(k)]=value;p.write_text(json.dumps(v))
run('surface_event.py',439,62,'enter');run('eventq.py',457,4,'enter');stage(74,0)
run('eventq.py',457,7,'talk');run('choose_dialog.py','Ground Floor|Top Floor','Top Floor');stage(74,1)
run('eventq.py',457,6,'enter');run('eventq.py',457,9,'talk')
for number in range(1,4):
 run('choose_dialog.py','Yes|No','No')
 print('BLAKE RING REFUSAL VERIFIED',number,flush=True)
run('dialog.py','--limit=100','--story-burst');stage(193,16)
print('REFUSED ALL THREE — next is Cal outside',flush=True)
