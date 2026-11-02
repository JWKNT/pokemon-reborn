"""Normal reviewed Ricardo touch trigger, stop at first command."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from locate import locate
from play import read,act
assert locate()[0:3]==(763,32,63),"Actual safe32,63 required"
assert len(read().splitlines())<4
subprocess.run([sys.executable,str(ROOT/'scripts/trainer_music.py'),'start','MeteorAceM','Ricardo'],check=True)
act('up:.12','wait:.6')
print(read(),flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/trainer_enter.py'),'763','48','MeteorAceM','Ricardo','--active-dialogue'],check=True)
