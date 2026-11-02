"""Advance Eve's inspected prebattle explanation and stop at a healed ordinary save."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',878,196,'talk')
run('linear_dialog',878,196,'--source-page',0)
run('party_front','Volcanion')
run('checkpoint','Idyll318-AnomalyPrepared')
