"""Advance only the installed Common77 farewell text using normal confirm presses."""
from play import *
import difflib
src=json.loads((ROOT/'work/394-common77.json').read_text())['list'];blocks=[]
assert not any(c['code'] in [102,103,104,301] for c in src)
for c in src:
 if c['code']==101:blocks.append(str(c['parameters'][0]))
 elif c['code']==401 and blocks:blocks[-1]+=' '+str(c['parameters'][0])
def norm(s):return re.sub('[^a-z]','',s.lower().replace('pokemon reborn',''))
for _ in range(20):
 t=read();print(t,flush=True)
 score=max(difflib.SequenceMatcher(None,norm(t),norm(b)).ratio()for b in blocks)
 if score<.62:print('FAREWELL BOUNDARY',score,flush=True);break
 act('c','wait:.5')
