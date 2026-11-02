"""Finish reviewed Swoobat candy training, checkpoint, approach supplies."""
from play import *
from nav import save

def run(script,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
run('train_candy_one.py','Swoobat',8,'L')
save()
t=read();print(t,flush=True)
raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL)
(ROOT/'notes/g10-trained-status.json').write_bytes(raw)
x=json.loads(raw)
assert x['map']==355 and x['party'][5]['level']==70,x['party'][5]
import shutil
shutil.copy2('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata',ROOT/'backups/Aster-Circus-trained.rxdata')
run('q.py','355,44,24,down,c,wait:1')
