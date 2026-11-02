"""Collect three source-reviewed unused purple shards via normal travel."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',38,6,'enter')
run('fly_to',292,'--carrier','Zapdos')
for eid in [21,17]:
 run('eventq',292,eid,'talk')
 out=subprocess.check_output([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=12'],text=True);print(out,flush=True)
 assert 'shard' in out.lower(),'Pickup requires review'
run('fly_to',524,'--carrier','Zapdos')
run('eventq',524,84,'talk')
out=subprocess.check_output([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=12'],text=True);print(out,flush=True)
assert 'shard' in out.lower(),'Pickup requires review'
run('checkpoint','Genesect315-Shards')
run('fly_to',355,'--carrier','Zapdos')
run('eventq',355,129,'talk')
