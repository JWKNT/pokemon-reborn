"""Record a normal Nightclub entry that activates the reviewed 120→125 tier."""
import os
os.environ['REBORN_FAST_KEYS']='1'
from locate import *
assert locate(826)==(826,10,5)
pre=json.loads((ROOT/'notes/Postgame287-NightclubLobby-navigation.json').read_text())
assert pre['variables']['569']==28 and pre['variables']['741']==4 and pre['switches']['1868']
boundary={'session':288,'before_video':24,'after_video':25,'before_cap':120,'after_cap':125,'before_save':'backups/Aster-Postgame287-NightclubLobby.rxdata','entry_event':'826E6→827; installed CommonEvent76 tier handler','entry_request_epoch':time.time()}
p=ROOT/'work/288-cap-entry.json';p.write_text(json.dumps(boundary,indent=2))
act('up:.12','wait:3');print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Postgame288-Tier5'],check=True)
post=json.loads((ROOT/'notes/Postgame288-Tier5-navigation.json').read_text())
assert post['variables']['741']==5 and post['variables']['595']==25,post['variables']
boundary['after_save']='backups/Aster-Postgame288-Tier5.rxdata';boundary['verified_epoch']=time.time();p.write_text(json.dumps(boundary,indent=2));print('CAP125 VERIFIED; REVIEW RAW FADE FOR VIDEO SPLIT',flush=True)
