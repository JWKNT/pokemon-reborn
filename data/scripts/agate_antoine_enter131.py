"""Reviewed normal Antoine touch trigger from protected staging, no raid."""
import json,subprocess,sys,time
from play import ROOT,read,act
from locate import locate
assert locate(763)==(763,36,61)
assert len(read().splitlines())<4
subprocess.run([sys.executable,str(ROOT/'scripts/trainer_music.py'),'start','MeteorAceF','Antoine','--battle-track','Atmosphere- Majesty'],check=True)
p=ROOT/'work/active-trainer-music.json';v=json.loads(p.read_text())
v['victory']='Atmosphere- Majesty'
v['victory_override_evidence']='763E49 command133 empty AudioFile; Field3045 Utilities1925 Audio221-251 skip empty without stopping current BGM'
p.write_text(json.dumps(v,indent=2)+'\n')
act('right:.12','wait:.7')
subprocess.run([sys.executable,str(ROOT/'scripts/trainer_enter.py'),'763','49','MeteorAceF','Antoine','--active-dialogue','--resume-intro'],check=True)
