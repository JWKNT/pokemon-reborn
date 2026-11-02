"""Decline a free switch only for the publicly announced expected opponent."""
from play import *
import difflib
foe=sys.argv[1]
t=read(); low=t.lower()
assert 'about to send in' in low, 'Fresh incoming-opponent announcement required: '+t
name=low.split('about to send in')[-1]
clean=lambda x:re.sub('[^a-z]','',x.lower())
assert clean(foe) in clean(name) or difflib.SequenceMatcher(None,clean(foe),clean(name)).ratio()>.82, 'Different incoming foe'
act('c','wait:.5');t=read().lower()
assert 'change pok' in t or 'switch your' in t, 'Free-switch prompt required'
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
