"""Reviewed return cart, lever, then basement transfer; normal save guards."""
import os,sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(e,label):subprocess.run([sys.executable,str(R/'scripts/victory_hazard_interact.py'),str(e),label],env=dict(os.environ,REBORN_FAST_KEYS='1'),check=True)
s=json.loads((R/'notes/navigation-state.json').read_text());assert s['switches']['1121'] and s['variables']['492']==1
run(132,'South191-return');s=json.loads((R/'notes/navigation-state.json').read_text());assert s['variables']['492']==0
run(130,'South191-lever');s=json.loads((R/'notes/navigation-state.json').read_text());assert s['switches']['1122']
run(132,'SE191-entry');s=json.loads((R/'notes/SE191-entry-status.json').read_text());assert s['map']==786;print('SOUTHEAST BASEMENT ENTERED',s['position'],flush=True)
