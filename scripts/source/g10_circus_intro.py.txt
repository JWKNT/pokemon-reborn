"""Reviewed linear arrival scenes; stop on any unplanned battle or choice."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('linear_dialog',355,51,'--active','--burst')
# Scene progression is read back from a checkpoint, not guessed.
from nav import save
save()
raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL)
(ROOT/'notes/g10-circus-arrival.json').write_bytes(raw)
print('CIRCUS ARRIVAL SAVED',flush=True)
