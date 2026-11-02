"""Normal reward equipment and return, stopping before final-tier trigger."""
import subprocess,sys,json,time
from pathlib import Path
p=Path('work/calcenon388-reward-queue.json')
for _ in range(60):
 j=json.loads(p.read_text())
 if j['done']==9 and not j.get('pending'):break
 time.sleep(1)
else:raise SystemExit('Reward checkpoint unfinished')
for cmd in [('give_held','Mewtwonite Y','Mewtwo','--pocket','Crystals'),('fly_to',527,'--carrier','Rayquaza'),('checkpoint','Nightclub388-TierBoundary')]:
 print(cmd,flush=True);subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
