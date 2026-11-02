"""Repeat the reviewed Monday Water-team matchup using normal UI."""
from play import *
def run(*args):
 p=subprocess.Popen([sys.executable,str(ROOT/'scripts'/args[0]),*args[1:]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);out=[]
 for line in p.stdout:print(line,end='',flush=True);out.append(line)
 if p.wait():raise SystemExit('Helper failed')
 return ''.join(out)
for cycle in range(int(sys.argv[1])):
 t=read().lower()
 if len(t.replace('pokemon reborn','').strip())>10:raise SystemExit('Expected overworld at Jonah')
 act('right','c','wait:1')
 run('choose_dialog.py','Yes|No','Yes')
 out=run('battle_batch.py','Ampharos','2','--foes','Squirtle,Wartortle,Blastoise','--turns','12','--stay-team-reviewed','--min-hp','.25')
 if not ('defeated' in out.lower() or 'for winning' in out.lower()):raise SystemExit('Win not verified')
 act('wait:2')
 out+=run('dialog.py','--limit=15')
 if 'bonus' not in out.lower() and 'cand' not in out.lower():raise SystemExit('Reward not verified')
 print('JONAH COMPLETE',cycle+1,flush=True)
