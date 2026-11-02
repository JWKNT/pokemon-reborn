"""Bounded normal UI epilogue queue; match only inspected choice-free ending pages."""
from play import *
import difflib
pages=json.loads((ROOT/'work/394-ending-dialogue-pages.json').read_text())
blocks=[]
for key,p in pages.items():
 assert not any(c['code'] in [102,103,104,301] or any(z in str(c['parameters'])for z in ['pbTrainerBattle','pbWildBattle']) for c in p['list'])
 bs=[]
 for c in p['list']:
  if c['code']==101:bs.append(str(c['parameters'][0]))
  elif c['code']==401 and bs:bs[-1]+=' '+str(c['parameters'][0])
 for b in bs:blocks.append((key,b))
def norm(s):return re.sub('[^a-z]','',s.lower().replace('pokemon reborn','').replace('\\pn','aster'))
for iteration in range(40):
 r=snap();text=' '.join(x['text']for x in r);print('ENDING PUBLIC',text,flush=True)
 # No movement or inputs to automatic credits, choices, or unfamiliar screens.
 matches=sorted((difflib.SequenceMatcher(None,norm(text),norm(b)).ratio(),k,b) for k,b in blocks)
 score,k,b=matches[-1]
 if score<.68 or len(norm(text))<8:print('ENDING REVIEW STOP',score,flush=True);break
 mid,eid,page=k.split('/');print('MATCHED ENDING SOURCE',k,b,flush=True)
 result=subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),mid,eid,'--source-page',page,'--burst','--log-scripted-bgm'])
 act('wait:1')
 if result.returncode not in [0,1]:raise SystemExit(result.returncode)
else:raise SystemExit('Ending scene budget reached')
