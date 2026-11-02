"""Record a normal Nightclub entry that activates the reviewed 115→120 tier."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from locate import *
assert locate(826)==(826,10,5)
pre=json.loads((ROOT/'notes/Postgame258-NightclubLobby-navigation.json').read_text())
assert pre['variables']['569']==21 and pre['variables']['741']==2
boundary={'session':259,'before_video':23,'after_video':24,'before_cap':115,'after_cap':120,'before_save':'backups/Aster-Postgame258-NightclubLobby.rxdata','entry_event':'826E6→827; installed CommonEvent76 tier handler','entry_request_epoch':time.time()}
p=ROOT/'work/259-cap-entry.json';p.write_text(json.dumps(boundary,indent=2))
act('up:.12','wait:3');print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Postgame259-Tier4'],check=True)
post=json.loads((ROOT/'notes/Postgame259-Tier4-navigation.json').read_text())
assert post['variables']['741']==3 and post['variables']['595']==20,post['variables']
boundary['after_save']='backups/Aster-Postgame259-Tier4.rxdata';boundary['verified_epoch']=time.time();p.write_text(json.dumps(boundary,indent=2));print('CAP120 VERIFIED; REVIEW RAW FADE FOR VIDEO SPLIT',flush=True)
