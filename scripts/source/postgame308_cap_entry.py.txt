"""Record a normal Nightclub entry that activates the reviewed 125→130 tier."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from locate import *
assert locate(826)==(826,10,5)
pre=json.loads((ROOT/'notes/Postgame307-NightclubLobby-navigation.json').read_text())
assert pre['variables']['569']==38 and pre['variables']['741']==5
boundary={'session':308,'before_video':25,'after_video':26,'before_cap':125,'after_cap':130,'before_save':'backups/Aster-Postgame307-NightclubLobby.rxdata','entry_event':'826E6→827; installed CommonEvent76 tier handler','entry_request_epoch':time.time()}
p=ROOT/'work/308-cap-entry.json';p.write_text(json.dumps(boundary,indent=2))
act('up:.12','wait:3');print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Postgame308-Tier6'],check=True)
post=json.loads((ROOT/'notes/Postgame308-Tier6-navigation.json').read_text())
assert post['variables']['741']==6 and post['variables']['595']==30,post['variables']
boundary['after_save']='backups/Aster-Postgame308-Tier6.rxdata';boundary['verified_epoch']=time.time();p.write_text(json.dumps(boundary,indent=2));print('CAP130 VERIFIED; REVIEW RAW FADE FOR VIDEO SPLIT',flush=True)
