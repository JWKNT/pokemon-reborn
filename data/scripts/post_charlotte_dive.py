"""Reviewed healing, Dive acquisition, and Hardy conversation after badge11."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
act('x','wait:.6')
run('q.py','419,9,61,down,wait:2')
run('eventq.py',413,68,'enter')
run('eventq.py',415,4,'talk');run('heal.py')
# Stop with the party healed; next transfer is reviewed from installed assets.
print('CALCENON PARTY HEALED',flush=True)
