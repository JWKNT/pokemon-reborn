"""Bounded ordinary training for the reviewed EV Tuner purchase; public UI only."""
import json,subprocess,sys,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
previous=R/'notes/Postgame343-Jace3-status.json'
assert previous.exists()
for n in range(4,24):
 s=json.loads(previous.read_text())
 if s['trainer']['money']>=45000:break
 assert shutil.disk_usage(R).free>5*1024**3, 'Reserve capture space'
 label=f'Postgame343-Jace{n}'
 subprocess.run([sys.executable,str(R/'scripts/jace330_round.py'),label],check=True)
 previous=R/'notes'/f'{label}-status.json'
 print('FUNDS',json.loads(previous.read_text())['trainer']['money'],flush=True)
else:raise SystemExit('Funding bound reached; review')
print('FUNDING COMPLETE',previous,flush=True)
