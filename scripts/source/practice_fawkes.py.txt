"""Repeat verified Sunday Fawkes matchup; stop on any unrecognized transition."""
from play import *
def run(*args):
 p=subprocess.Popen([sys.executable,str(ROOT/'scripts'/args[0]),*args[1:]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);out=[]
 for line in p.stdout:print(line,end='',flush=True);out.append(line)
 if p.wait():raise SystemExit('Helper failed')
 return ''.join(out)
for cycle in range(int(sys.argv[1])):
 t=read().lower()
 if len(t.splitlines())>3 and not (cycle==0 and '--resume' in sys.argv):raise SystemExit('Expected overworld at Fawkes')
 if not (cycle==0 and '--resume' in sys.argv):act('right','c','wait:1','c','wait:1','c','wait:2')
 out=run('battle_batch.py','Arcanine','1','--foes','doublade','--turns','5','--min-hp','.2')
 for stage in range(2):
  t=read().lower()
  if not ('change pok' in t or 'switch your' in t):raise SystemExit('Expected free switch')
  import re
  normalized=re.sub(r'grenin[\W_]*ja','greninja',out.lower())
  upcoming=re.findall(r'send\s*in\s*(typhlosion|greninja)',normalized)
  if not upcoming:raise SystemExit('Upcoming opponent not observed')
  foe=upcoming[-1];actor='Swampert' if foe=='typhlosion' else 'Ampharos'
  act('c','wait:1.2');run('party_pick.py',actor)
  out=run('battle_batch.py',actor,'1' if actor=='Swampert' else '2','--foes',foe,'--turns','8','--min-hp','.15')
 if 'bonus' not in out.lower() or 'cand' not in out.lower():raise SystemExit('Reward not verified')
 print('FAWKES COMPLETE',cycle+1,flush=True)
