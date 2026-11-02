"""Resume after the publicly verified normal Timid Mint; never replay consumed steps."""
import os,json,subprocess,sys
from pathlib import Path
os.environ['REBORN_COORD_CACHE']='1'
from play import read,act,ROOT
from agate_prep_phase import plan,execute
assert 'cofagrigus becomes timid' in read().lower(),'Expected live mint-effect receipt'
act('c','wait:.6')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
before=json.loads((ROOT/'notes/Circus-Cofa-after-shopping-129-status.json').read_text())
commands=plan('build',before)
assert commands[2]=={'internal':'timid-mint'}
assert commands[3]['script']=='berry_batch'
execute('build',before,commands[3:])
print('COFA BUILD RESUME COMPLETE',flush=True)
