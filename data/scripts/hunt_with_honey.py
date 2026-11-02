"""Use bounded owned Honey encounters, fleeing visibly identified non-targets."""
from play import *
import difflib
wanted=sys.argv[1].split(',');limit=int(sys.argv[2]) if len(sys.argv)>2 else 6
assert 1<=limit<=16
for used in range(limit+1):
 stop=ROOT/'work/stop-honey-hunt'
 if stop.exists():stop.unlink();raise SystemExit('Honey hunt paused for route review')
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
 r=snap();t=' '.join(v['text'] for v in r).lower()
 assert 'fight' in t and re.search(r'\b(?:bag|bae)\b',t),'Battle command required'
 enemy=' '.join(v['text'] for v in r if v['y']<.37).lower()
 if any(difflib.SequenceMatcher(None,n.lower(),w.strip('.,!?')).ratio()>=.83 for n in wanted for w in enemy.split()):
  print('TARGET FOUND',enemy,flush=True);break
 if used==limit:raise SystemExit('Honey search limit reached; stopped at command screen')
 hp=re.search(r'(\d+)\s*/\s*(\d+)',t)
 if not hp or not 0<int(hp[1])<=int(hp[2]):raise SystemExit('Public HP needs review before another escape')
 if int(hp[1])<min(120,int(hp[2])*.35):raise SystemExit('HP reserve reached; stopped at command screen')
 for escape in range(3):
  result=subprocess.run([sys.executable,str(ROOT/'scripts/flee.py')],capture_output=True,text=True)
  print(result.stdout,flush=True)
  if result.returncode==0:break
  message=result.stdout+result.stderr
  if 'prevents escaping' in message.lower() or 'arena trap' in message.lower():raise SystemExit('Trapping ability visibly blocks escape; battle action required')
  if 'failed run acknowledged; next command ready' not in message:raise SystemExit(result.stderr or 'Escape needs review')
 else:raise SystemExit('Three escape attempts failed; inspect HP before continuing')
 act('wait:.8')
 subprocess.run([sys.executable,str(ROOT/'scripts/use_field_item.py'),'Honey'],check=True)
 act('wait:2')
