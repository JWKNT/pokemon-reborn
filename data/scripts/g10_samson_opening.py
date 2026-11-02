"""Reviewed opening: rocks, free Cofagrigus, then one burn attempt. UI guards stop deviations."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
t=read().lower()
if not all(w in t for w in ['fight','boldore','hariyama']):raise SystemExit('Opening menu expected')
run('battle_batch','Boldore',2,'--foes','Hariyama','--turns',1)
run('battle_batch','Boldore',3,'--foes','Hariyama','--turns',1)
t=read().lower()
if not ('cancel' in t and t.count('hp')>=5):raise SystemExit('Expected free replacement')
run('party_pick','Cofagrigus')
run('battle_batch','Cofagrigus',2,'--foes','Hariyama','--turns',1,'--status-move')
print('OPENING COMPLETE; verify Mummy, burn, HP before next turn',flush=True)
