"""Reviewed Route 3 bridge scenes and Aya registration, using normal controls."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
def note(stage,**switches):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['184']=stage
 v.setdefault('switches',{}).update(switches);p.write_text(json.dumps(v))
rc=subprocess.call([sys.executable,str(ROOT/'scripts/q.py'),'361,22,22'])
if rc==0:act('up:.12','wait:1')
elif rc!=2:raise SystemExit(rc)
t=read().lower()
if not any(z in t for z in ['cain:','hardy:','saphira:']):raise SystemExit('First Route 3 scene review: '+t)
run('linear_dialog.py',361,53,'--burst')
note(7,**{'2045':True,'486':True})
run('q.py','361,53,17,right:.12,right:.12,wait:2')
run('q.py','404,1,11,right:.12,wait:1')
run('linear_dialog.py',404,71,'--burst')
note(8)
run('eventq.py',404,1,'talk')
run('linear_dialog.py',404,1,'--burst')
note(9,**{'2046':True,'488':True,'490':True})
run('checkpoint.py','Aya-route3-joined')
print('AYA REGISTERED — inspect saved partner and cave events',flush=True)
