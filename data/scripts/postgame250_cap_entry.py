"""Record a normal Nightclub entry that activates the reviewed 110→115 tier."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from locate import *
assert locate(826)==(826,10,5)
pre=json.loads((ROOT/'notes/Postgame250-NightclubLobby-navigation.json').read_text())
assert pre['variables']['569']==13 and pre['variables']['741']==1
boundary={'session':250,'before_video':22,'after_video':23,'before_cap':110,'after_cap':115,'before_save':'backups/Aster-Postgame250-NightclubLobby.rxdata','entry_event':'826E6→827; installed CommonEvent76 tier handler','entry_request_epoch':time.time()}
p=ROOT/'work/250-cap-entry.json';p.write_text(json.dumps(boundary,indent=2))
act('up:.12','wait:3');print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Postgame250-Tier3'],check=True)
post=json.loads((ROOT/'notes/Postgame250-Tier3-navigation.json').read_text())
assert post['variables']['741']==2 and post['variables']['595']==15,post['variables']
boundary['after_save']='backups/Aster-Postgame250-Tier3.rxdata';boundary['verified_epoch']=time.time();p.write_text(json.dumps(boundary,indent=2));print('CAP115 VERIFIED; REVIEW RAW FADE FOR VIDEO SPLIT',flush=True)
