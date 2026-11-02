"""Prepared capped-team Victoria policy. Stop on any unexpected state."""
from play import *
import re

def run(*args):
 p=subprocess.Popen([sys.executable,str(ROOT/'scripts'/args[0]),*args[1:]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);out=[]
 for line in p.stdout:print(line,end='',flush=True);out.append(line)
 if p.wait():raise SystemExit('Helper failed')
 return ''.join(out)
out=run('battle_batch.py','Swampert','2','--foes','Pangoro','--turns','3','--min-hp','.4')
for stage in range(5):
 if 'defeated' in out.lower():print('VICTORIA WON');break
 t=read().lower()
 if not ('change pok' in t or 'switch your' in t):raise SystemExit('Expected free switch; inspect')
 matches=re.findall(r'send\s*in\s*(gallade|raichu|mienfoo|incineroar)',out.lower())
 if not matches:raise SystemExit('Upcoming foe unobserved')
 foe=matches[-1];actor='Swoobat' if foe in ['gallade','mienfoo'] else 'Swampert'
 act('c','wait:1.2');run('party_pick.py',actor)
 if foe=='gallade':
  run('battle_batch.py','Swoobat','2','--foes','Gallade','--turns','1','--min-hp','.5')
  out=run('battle_batch.py','Swoobat','3','--foes','Gallade','--turns','3','--min-hp','.12','--watch')
 else:
  slot=3 if foe=='mienfoo' else (1 if foe=='raichu' else 2)
  out=run('battle_batch.py',actor,str(slot),'--foes',foe,'--turns','4','--min-hp','.25')
