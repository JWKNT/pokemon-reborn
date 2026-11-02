"""Queue the inspected badge-gate sequence; stop for any unexpected state."""
from play import *
from locate import locate
def run(s,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def observed_var(n,value):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v.setdefault('variables',{})[str(n)]=value;p.write_text(json.dumps(v))
def gate(mid,event,word):
 rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(event),'talk'])
 if rc and word.lower() not in read().lower():raise SystemExit('Unexpected gate interruption')
if '--resume-first' not in sys.argv:
 assert locate()[0]==446
 gate(446,3,'VOLTBADGE')
run('linear_dialog',446,3,'--active','--burst');observed_var(193,33)
run('eventq',446,6,'enter')
for event,stage in [(5,34),(9,35),(11,36)]:
 gate(443,event,{5:'CANOPY',9:'COCOON',11:'OMEN'}[event]);run('linear_dialog',443,event,'--active','--burst');observed_var(193,stage)
observed_var(215,6)
run('eventq',443,25,'enter')
assert locate()[0]==445
run('eventq',445,9,'item');run('mark_event',445,9)
run('field_medicine','Rare Candy','Kricketune');run('candy_progress');run('overworld')
print('RARE CANDY AND PERISH SONG PREPARATION COMPLETE',flush=True)
