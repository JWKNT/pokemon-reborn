"""Collect the source-reviewed southeast Shaymin using normal controls."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',878,173,'talk')
act('wait:4')
print(read(),flush=True)
run('checkpoint','Idyll318-SEOrb')
run('eventq',878,189,'talk')
run('linear_dialog',878,189,'--source-page',0)
run('checkpoint','Idyll318-Shaymin4')
