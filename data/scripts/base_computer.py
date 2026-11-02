"""Use a mapped base terminal, verify its message, then update navigation notes."""
from play import *
eid=int(sys.argv[1]);assert eid in [52,53,69]
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'254',str(eid),'talk'],check=True)
t=read();print(t,flush=True)
if 'engaged' not in t.lower() or not any(k in t.lower() for k in ['lock','gate']):raise SystemExit('Terminal message review')
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=8'],check=True)
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text())
if eid in [52,53]:s['variables']['149']+=1
else:s.setdefault('switches',{})['2031']=True
p.write_text(json.dumps(s))
subprocess.run([sys.executable,str(ROOT/'scripts/mark_event.py'),'254',str(eid)],check=True)
if eid==69:
 from nav import save
 save()
 with (ROOT/'notes/g7-before-abra.json').open('w') as f:
  subprocess.run(['ruby',str(ROOT/'scripts/status.rb')],stdout=f,stderr=subprocess.DEVNULL,check=True)
 print('LOWER SHORTCUT CHECKPOINT SAVED',flush=True)
