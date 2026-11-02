"""Two explicit guarded actions; never replay a stopped action."""
import json,subprocess,sys
from play import ROOT
base=[sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','antoine','--foes','Mamoswine']
subprocess.run(base+['--item','Ultra Potion','--min-hp','1','--output','work/antoine-heal-before-burn131.json'],check=True)
r=json.loads((ROOT/'work/antoine-heal-before-burn131.json').read_text())
assert r['final_classification']=='fresh_expected_command' and r['final_hp_proof']['hp']>=144
subprocess.run(base+['--move-slot','2','--min-hp','144','--output','work/antoine-burn131.json'],check=True)
