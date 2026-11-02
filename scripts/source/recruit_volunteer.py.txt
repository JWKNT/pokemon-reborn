"""Recruit one inspected Adrienn volunteer through dialogue; planner changes only."""
from play import *
import difflib
m,e=map(int,sys.argv[1:3]);sf=ROOT/'notes/navigation-state.json';state=json.loads(sf.read_text());key=f'{m},{e},A'
if state.get('self_switches',{}).get(key):print('ALREADY RECRUITED',m,e,flush=True);raise SystemExit(0)
assert 50<=state['variables']['339']<65,'Recruitment phase is not active'
review=json.loads((ROOT/'work/adrienn-volunteers-reviewed.json').read_text());pages=[r for r in review if(r['map'],r['event'])==(m,e)];assert pages
cs=pages[0]['commands'];assert not any(c['code']in[102,103,104,301]or'pbTrainerBattle'in str(c['parameters'])for c in cs)
assert any(c['code']==122 and c['parameters']==[339,339,1,0,1]for c in cs)
texts=[]
for c in cs:
 if c['code']==101:texts.append(str(c['parameters'][0]))
 elif c['code']==401 and texts:texts[-1]+=' '+str(c['parameters'][0])
started=time.time()
if '--active-dialogue' not in sys.argv:
 for attempt in range(30):
  began=time.time();rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),str(m),str(e),'talk'])
  if rc==0:break
  text=read().lower()
  # These installed maps were checked to contain no trainer battles.
  if m in [570,531,533] and 'fight' in text and 'hp' in text and 'cofagrig' in text:
   subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(began)],check=True);continue
  raise SystemExit('Volunteer route interruption requires review: '+text)
 else:raise SystemExit('Volunteer wild-escape retry bound')
subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),str(m),str(e),'--active','--burst'],check=True)
norm=lambda z:re.sub('[^a-z]','',z.lower().replace('Pokemon Reborn',''))
rows=[json.loads(l)for l in(ROOT/'recordings/screens.jsonl').read_text().splitlines()];rows=[r for r in rows if r['epoch']>=started]
matches=[r for r in rows if any(difflib.SequenceMatcher(None,norm(' '.join(r['text'])),norm(t)).ratio()>=.65 for t in texts[-4:])]
if not matches and '--active-dialogue' not in sys.argv:
 subprocess.run([sys.executable,str(ROOT/'scripts/chase_volunteer.py'),str(m),str(e)],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),str(m),str(e),'--active','--burst'],check=True)
 rows=[json.loads(l)for l in(ROOT/'recordings/screens.jsonl').read_text().splitlines()];rows=[r for r in rows if r['epoch']>=started]
 matches=[r for r in rows if any(difflib.SequenceMatcher(None,norm(' '.join(r['text'])),norm(t)).ratio()>=.65 for t in texts[-4:])]
assert matches,'No observed consenting volunteer dialogue; do not credit or alter planner'
state=json.loads(sf.read_text());state.setdefault('self_switches',{})[key]=True;state['variables']['339']+=1;sf.write_text(json.dumps(state))
p=ROOT/'notes/adrienn-volunteer-progress.json';ledger=json.loads(p.read_text())if p.exists()else[];ledger.append({'map':m,'event':e,'completed_epoch':time.time(),'counter':state['variables']['339'],'consent_evidence':matches[-1]});p.write_text(json.dumps(ledger,indent=2))
print('VOLUNTEER OBSERVED COMPLETE',m,e,'COUNT',state['variables']['339']-50,flush=True)
