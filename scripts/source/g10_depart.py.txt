from play import *
from nav import save
save()
print(read(),flush=True)
raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL)
(ROOT/'notes/g10-depart-status.json').write_bytes(raw)
x=json.loads(raw)
assert x['party'][5]['level']==70 and x['party'][5]['item']=='ODDINCENSE',x['party'][5]
assert x['party'][1]['item']=='EXPSHARE',x['party'][1]
import shutil
shutil.copy2('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata',ROOT/'backups/Aster-Circus-depart.rxdata')
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'355,13,34,left,wait:2','365,8,33,up,wait:2','365,4,63,left,wait:2'],check=True)
