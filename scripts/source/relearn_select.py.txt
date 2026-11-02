"""Choose an inspected relearner index, verifying the move before accepting."""
from play import *
import re,difflib
name=sys.argv[1];index=int(sys.argv[2]);assert 0<=index<=40
norm=lambda s:re.sub('[^a-z]','',s.lower())
t=read();assert 'teachwhich' in norm(t),'Relearner list expected'
act(*[k for _ in range(index) for k in ('down:.12','wait:.18')],'wait:.5');t=read();print(t,flush=True)
# Session370 direct visual review: V-create's V can disappear in full-screen OCR.
visible = norm(name) in norm(t) or (norm(name)=='vcreate' and any(line.strip().lower()=='-create' for line in t.splitlines()) and '180' in t and '95' in t)
assert visible,'Expected move absent from visible list'
act('c','wait:.5');t=read();print(t,flush=True)
assert any(difflib.SequenceMatcher(None,'teach'+norm(name),norm(line)).ratio()>=.82 for line in t.splitlines()),'Selected move confirmation mismatch'
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
learning_args=[]
if len(sys.argv)>3:
 slot=int(sys.argv[3]);assert 0<=slot<=3
 learning_args=['--expected-move',name,'--replace-slot',str(slot)]
subprocess.run([sys.executable,str(ROOT/'scripts/learning.py'),*learning_args],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/relearn_finish.py')],check=True)
