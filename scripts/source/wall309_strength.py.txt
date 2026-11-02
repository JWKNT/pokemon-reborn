"""Activate a named owned Strength user through the visible party menu."""
from play import *
def run(n,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{n}.py'),*map(str,a)],check=True)
name=sys.argv[1] if len(sys.argv)>1 else 'Swampert'
run('party_open');run('party_pick',name,'--single')
t=read().lower();assert 'strength' in t and 'summary' in t,t
act('down:.12','c','wait:1')
if 'strength is already being used' in read().lower():act('c','wait:.4')
else:run('dialog','--limit=8')
run('overworld')
