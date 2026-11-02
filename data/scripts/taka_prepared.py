"""Guarded, reviewed Taka1 matchup. All game actions go through UI helpers."""
from play import *
import re,difflib

def run(*args):
 p=subprocess.Popen([sys.executable,str(ROOT/'scripts'/args[0]),*args[1:]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);out=[]
 for line in p.stdout:print(line,end='',flush=True);out.append(line)
 if p.wait():raise SystemExit('Helper failed')
 return ''.join(out)
current='Arcanine';out=run('battle_batch.py',current,'1','--foes','Klefki','--turns','2','--min-hp','.35')
for stage in range(4):
 if 'defeated' in out.lower() or 'for winning' in out.lower():print('TAKA WON');break
 t=read().lower()
 if not ('change pok' in t or 'switch your' in t):raise SystemExit('Expected free switch; inspect')
 lines=[x.lower() for x in out.splitlines() if 'send in' in x.lower() or 'sendin' in x.lower()]
 if not lines:raise SystemExit('Upcoming foe unobserved')
 ranking=sorted([(difflib.SequenceMatcher(None,n,w.strip('.,')).ratio(),n) for n in ['gligar','exeggutor','chatot'] for w in lines[-1].split()],reverse=True)
 if ranking[0][0]<.75:raise SystemExit('Unknown next foe')
 foe=ranking[0][1];actor='Swampert' if foe=='gligar' else 'Hexan';slot=2 if foe=='gligar' else 1
 if current==actor:act('x','wait:1')
 else:act('c','wait:1');run('party_pick.py',actor)
 current=actor
 out=run('battle_batch.py',actor,str(slot),'--foes',foe,'--turns','3','--min-hp','.25')
