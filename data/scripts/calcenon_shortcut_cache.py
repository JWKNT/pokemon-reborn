"""Confirm the reviewed $40000 prompt; open shortcut, fetch its item cache."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
start=time.time()-120 if '--resume' in sys.argv else time.time()
if '--resume' not in sys.argv:act('c','wait:.6')
run('dialog.py','--story-burst','--limit=15')
evidence=' '.join(' '.join(json.loads(x)['text'])for x in(ROOT/'recordings/screens.jsonl').read_text().splitlines() if json.loads(x)['epoch']>=start).lower()
if 'road is now open' not in evidence:raise SystemExit('Road completion evidence needed')
p=ROOT/'notes/navigation-state.json';state=json.loads(p.read_text());state['switches']['486']=False;state['variables']['333']=0;p.write_text(json.dumps(state))
run('eventq.py',418,5,'enter');run('eventq.py',361,63,'enter')
for e in [2,1,4]:run('eventq.py',438,e,'item')
run('eventq.py',438,3,'enter');run('eventq.py',361,51,'enter');run('eventq.py',418,6,'enter')
run('eventq.py',413,68,'enter');run('eventq.py',415,7,'talk')
print('CALCENON PC READY',flush=True)
