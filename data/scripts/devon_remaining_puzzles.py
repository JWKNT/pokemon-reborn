"""Reviewed Devon monitor sequences; normal inputs, bounded coordinate checks."""
from play import ROOT,act,read
from locate import locate
import sys,json,subprocess
mode=int(sys.argv[1]);assert mode in (629,631)
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
def state_switch(k,v):
 p=ROOT/'notes/navigation-state.json';d=json.loads(p.read_text());d['switches'][str(k)]=v;p.write_text(json.dumps(d))
def full_checkpoint(name):
 run('checkpoint.py',name);s=json.loads((ROOT/'notes'/f'{name}-status.json').read_text());assert all(m['hp']==m['totalhp'] for m in s['party']),'Electrical damage detected; stop before battles'
def power(eid,sw):
 run('devon_spinners.py','--map',mode,'--monitor',eid,'--go')
 d=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(mode),str(eid)],stderr=subprocess.DEVNULL));_,x,y=locate(mode);ex,ey=d['x'],d['y'];f={(ex,ey+1):'up',(ex,ey-1):'down',(ex+1,ey):'left',(ex-1,ey):'right'}
 assert (x,y)in f;act(f[(x,y)]+':.12','c','wait:.6');print(read(),flush=True)
 run('choose_dialog.py','Yes|No','Yes');run('linear_dialog.py',mode,eid,'--active','--past-choice');state_switch(sw,True)
assert locate(mode)[0]==mode
if mode==629:
 # Run only after an independently observed native radio calibration in this room.
 assert (ROOT/'notes/Devon-second-radio-calibrated-navigation.json').exists()
 for eid in ([198,197,196]if '--resume-after195' in sys.argv else [195,198,197,196]):run('devon_spinners.py','--map',629,'--monitor',eid,'--activate','--go')
 power(15,1563);run('devon_spinners.py','--map',629,'--goal',12,3,'--go');run('eventq.py',629,11,'enter')
 run('linear_dialog.py',628,45,'--burst','--log-scripted-bgm','--world-settle',18);full_checkpoint('Devon-second-puzzle-complete')
 assert json.loads((ROOT/'notes/navigation-state.json').read_text())['variables']['339']==38,'Cutscene still active; do not enter final room'
 run('eventq.py',628,11,'enter');act('wait:1')
 full_checkpoint('Devon-final-puzzle-radio-ready')
else:
 assert json.loads((ROOT/'notes/navigation-state.json').read_text())['variables']['339']==38
 for eid in [120,117,118,117,119,121,122,123]:run('devon_spinners.py','--map',631,'--monitor',eid,'--activate','--go')
 power(41,1564);full_checkpoint('Devon-ZEL-entry-ready')
 print('STOPPED AT FULL-HP PRE-ZEL CHECKPOINT; entry/major capture handled separately',flush=True)
