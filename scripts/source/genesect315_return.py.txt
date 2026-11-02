"""Return through inspected ordinary factory doors to the saved Cain approach."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('fly_to',530,'--carrier','Zapdos')
for mid,eid in [(530,11),(522,15),(594,10),(595,1),(596,13)]:run('eventq',mid,eid,'enter')
run('queue_route','work/315-cain-approach.json')
run('checkpoint','Genesect315-CainEntry')
