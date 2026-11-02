"""Heal at inspected Ametrine nurse and enter storage; stop for slot verification."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
run('eventq.py',458,4,'talk');run('heal.py')
run('eventq.py',458,7,'talk')
print('PC opened',flush=True)
