"""Two reviewed moves, each guarded by the actual actor/foe, HP and field."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1')
for slot,extra in [(1,['--min-hp','1']),(3,['--require-field','misty','--min-hp','.42'])]:
 subprocess.run([sys.executable,str(R/'scripts/public_turn_capture.py'),'battle_batch.py','Sylveon',str(slot),'--foes','Noivern','--turns','1','--watch',*extra],check=True,env=env)
