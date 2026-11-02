"""Execute reviewed straight pushes using ordinary controls and fresh save guards."""
import json,subprocess,sys,os,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
groups=json.loads((R/'work/197-arrow-final-groups.json').read_text())
start=int(sys.argv[1]);end=int(sys.argv[2])
for index in range(start,end+1):
 g=groups[index-1];e=str(g['event']);dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[g['direction']];target=g['box_to']
 for attempt in range(4):
  n=json.loads((R/'notes/navigation-state.json').read_text());cur=n['positions']['787'][e]
  if cur==target:break
  delta=[target[0]-cur[0],target[1]-cur[1]];count=delta[0]*dx+delta[1]*dy
  assert 1<=count<=10 and delta==[dx*count,dy*count],(cur,target)
  before=n['positions']['787'];label=f'Arrow197-final-{index}-try{attempt+1}';began=time.time()
  rc=subprocess.call([sys.executable,str(R/'scripts/victory_arrow_push_steps.py'),e,g['direction'],label,str(count)],env=dict(os.environ,REBORN_FAST_KEYS='1'))
  p=R/'notes'/f'{label}-navigation.json';assert p.exists() and p.stat().st_mtime>began,'No fresh normal save; inspect UI'
  after=json.loads(p.read_text())['positions']['787'];assert all(after[i]==before[i]for i in ['58','59','60','61','65','69','73','74']if i!=e),'Other boulder moved'
  if rc:
   text=subprocess.check_output([sys.executable,str(R/'scripts/play.py')],text=True).lower()
   assert 'cancel' in text and text.count('hp')>=5,'Not safely in Party'
  if after[e]==target:break
 else:raise SystemExit('Four tries exhausted')
 assert json.loads((R/'notes/navigation-state.json').read_text())['positions']['787'][e]==target
 print('STRAIGHT GROUP VERIFIED',index,target,flush=True)
