"""Renew an already expired Repel, choosing Super Repel by visible label."""
from play import *
import re
from PIL import Image
t=read().lower()
if 'repel' not in t:raise SystemExit('No Repel message to handle')
if re.search(r'(?:w|u)ore\s*of\s*f',t):
 act('c','wait:.5');t=read().lower()
if 'cancel' in t and any(z in t for z in ['repel','super repel','max repel']):
 labels=[s for s in ['Repel','Super Repel','Max Repel','Cancel'] if any(z.strip(' •›>').lower()==s.lower() for z in t.splitlines())]
 if 'Cancel' not in labels or len(labels)<2:
  im=Image.open(NATIVE);w,h=im.size;cp=ROOT/'work/repel-choice.png'
  im.crop((int(w*.66),int(h*.48),int(w*.99),int(h*.76))).save(cp)
  rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)]))
  seen=[re.sub('[^a-z]','',z['text'].lower())for z in rows]
  labels=[s for s in ['Repel','Super Repel','Max Repel','Cancel']if re.sub('[^a-z]','',s.lower())in seen]
  if 'Cancel'not in labels or len(labels)<2:raise SystemExit('Repel choice review: '+str(seen))
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'|'.join(labels),'Cancel' if '--cancel' in sys.argv else next(z for z in ['Super Repel','Max Repel','Repel']if z in labels)],check=True)
elif 'yes' in t.splitlines() and 'no' in t.splitlines():
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No' if '--cancel' in sys.argv else 'Yes'],check=True)
elif not t.replace('pokemon reborn','').strip():
 print('REPEL EXPIRED; NO RENEWAL MENU',flush=True)
 raise SystemExit(0)
else:raise SystemExit('Repel renewal review: '+t)
t=read().lower()
renewal_confirmed = 'used' in t and 'repel' in t
if renewal_confirmed:act('c','wait:.5')
t=read().lower()
# New World floor textures produce many OCR words after confirmed use.
if len(t.splitlines())>3 and not renewal_confirmed:raise SystemExit('Repel result review: '+t)
print('REPEL CANCELED' if '--cancel' in sys.argv else 'REPEL RENEWED',flush=True)
