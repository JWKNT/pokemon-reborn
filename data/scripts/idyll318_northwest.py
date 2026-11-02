"""Collect the source-reviewed northwest Shaymin using normal controls."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',878,187,'talk')
act('wait:4')
print(read(),flush=True)
run('checkpoint','Idyll318-NWOrb')
run('eventq',878,191,'talk')
run('linear_dialog',878,191,'--source-page',0)
run('checkpoint','Idyll318-Shaymin3')
