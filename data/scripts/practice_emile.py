"""Repeat the verified four-badge Emile matchup, with automatic postbattle healing supplied by the game."""
from play import *
def run(*args):
 p=subprocess.Popen([sys.executable,str(ROOT/'scripts'/args[0]),*args[1:]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);out=[]
 for line in p.stdout:print(line,end='',flush=True);out.append(line)
 if p.wait():raise SystemExit('Helper failed')
 return ''.join(out)
for cycle in range(int(sys.argv[1])):
 t=read().lower()
 if len(t.splitlines())>3:raise SystemExit('Expected overworld at Emile')
 act('up','c','wait:0.8','c','wait:0.8','c','wait:2')
 out=run('battle_batch.py','Arcanine','1','--foes','Servine','--turns','2','--min-hp','.4')
 for stage in range(3):
  t=read().lower()
  if not ('change pok' in t or 'switch your' in t):raise SystemExit('Expected free switch')
  import re
  upcoming=re.findall(r'send\s*in\s*(quilava|gardevoir|nidoking)',out.lower())
  if not upcoming:raise SystemExit('Upcoming opponent was not observed')
  foe=upcoming[-1];actor='Drapion' if foe=='gardevoir' else 'Swampert'
  act('c','wait:1.2');run('party_pick.py',actor)
  if foe=='gardevoir':
   run('battle_batch.py','Drapion','2','--foes','Gardevoir','--turns','1','--min-hp','.5')
   out=run('battle_batch.py','Drapion','0','--foes','Gardevoir','--turns','4','--min-hp','.18')
  else:out=run('battle_batch.py','Swampert','2','--foes',foe,'--turns','3','--min-hp','.35')
 if 'bonus' not in out.lower() or 'candy' not in out.lower():raise SystemExit('Reward not verified')
 print('EMILE COMPLETE',cycle+1,flush=True)
