"""Reviewed Magma raid setup, ending at the Aqua entrance battle introduction."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('party_swap',1,2) # Current order: Ampharos/Cofa/Swampert; pair Discharge with Ground immunity.
run('eventq',79,150,'enter')
run('eventq',165,14,'talk')
run('linear_dialog',165,14,'--active')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['95']=7;p.write_text(json.dumps(v))
run('q','165,31,12,right,wait:2','79,8,19,left,wait:2','424,3,5,left,wait:2')
run('eventq',80,33,'enter')
run('eventq',170,3,'talk')
print('READY: AQUA ENTRANCE DOUBLE; AMPHAROS DISCHARGE + SWAMPERT MUDDY WATER',flush=True)
