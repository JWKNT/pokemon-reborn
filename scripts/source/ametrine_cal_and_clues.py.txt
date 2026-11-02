"""Refusal route: meet Cal, gather the installed apartment clues, stop at password."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
def observed(variables=None,switches=None):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables'].update({str(k):z for k,z in(variables or{}).items()});v.setdefault('switches',{}).update({str(k):z for k,z in(switches or{}).items()});p.write_text(json.dumps(v))
def elevator(label):
 run('eventq.py',457,7,'talk');run('choose_dialog.py','Ground Floor|Top Floor',label);observed({74:1 if label=='Top Floor' else 0})
 run('eventq.py',457,6,'enter')
if '--cal-started' not in sys.argv:
 run('eventq.py',457,5,'enter');observed({74:1});elevator('Ground Floor');run('eventq.py',457,1,'enter')
observed(switches={506:True})
run('linear_dialog.py',439,142,'--active','--burst');observed({193:17},{507:True})
run('surface_event.py',439,62,'enter');run('eventq.py',457,4,'enter');observed({74:0});elevator('Top Floor')
# Read the available hint, then obtain key head, handle, completed key, cable and disc.
for eid in [12,17,35,40,39,38,37,24,24]:
 run('eventq.py',457,eid,'talk');run('linear_dialog.py',457,eid,'--active','--burst')
 if eid==40:observed(switches={514:True})
 if eid==39:observed(switches={515:True,513:True})
 if eid==38:observed(switches={511:True})
 if eid==37:observed(switches={512:True})
# Monitor has a numeric input: no generic dialogue driver crosses it.
run('eventq.py',457,25,'talk')
print('PASSWORD MONITOR REACHED — verify digits before confirmation',flush=True)
