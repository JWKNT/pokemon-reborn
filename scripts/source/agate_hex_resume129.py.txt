"""Finish currently open normal reminder list after wrong-index guard; exact visible Hex."""
import os,subprocess,sys,json,re
os.environ['REBORN_COORD_CACHE']='1'
from play import ROOT,read,act
from agate_prep_phase import execute
assert 'night shade' in read().lower(),'Expected currently reviewed reminder list'
act('down:.12','wait:.4')
assert 'hex' in read().lower(),'Hex missing from visible list'
act('c','wait:.5')
assert 'teachhex' in re.sub('[^a-z]','',read().lower()),'Exact Hex confirmation required'
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
from learning import PLANS,resolve
PLANS['hex']=1
assert resolve(read()),'Hex learning needs review'
for name in ['relearn_finish','overworld']:
 subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py'))],check=True)
before=json.loads((ROOT/'notes/Circus-Cofa-after-shopping-129-status.json').read_text())
cmds=[{'script':'give_held','args':['Power Lens','Cofagrigus']},{'script':'eventq','args':[355,118,'talk']},{'script':'heal','args':[]},{'script':'checkpoint','args':['Agate-Cofa-training-ready']}]
execute('build',before,cmds)
print('HEX AND COFA BUILD COMPLETE',flush=True)
