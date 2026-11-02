"""Select a named replacement from a fresh battle menu or offered free switch."""
from play import *
import re
from PIL import Image
name=sys.argv[1];t=read().lower()
if re.search(r'about\s*to\s*send\s*in',t):
 act('c','wait:.5');t=read().lower()
 assert 'change pok' in t or 'switch your' in t,'Expected free-switch choice after public send-in notice'
if 'fight' in t:
 act('left:0.22','down:0.22','c','wait:1.5')
elif 'change pok' in t or 'switch your' in t:act('c','wait:1.5')
elif 'choose a pok' in t or ('cancel' in t and t.count('hp')>=5):pass
else:raise SystemExit('Expected switch offer, forced replacement or battle menu')
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name],check=True)
seen={}
for _ in range(30):
 t=read();print(t,flush=True)
 seen[t]=seen.get(t,0)+1
 if re.search(r'\ble[vw]el\s*\d+\s*[!i]',' '.join(t.lower().split())) or 'max. hp' in t.lower() or 'max.hp' in t.lower():
  act('c','wait:.2');continue
 if 'already in battle' in t.lower():
  act('x','wait:0.3','x','wait:0.3');raise SystemExit('Already active; returned from party selector')
 if re.search(r'de.?feated|for winning',t,re.I) or 'change pok' in t.lower():
  print('PUBLIC BATTLE BOUNDARY; no further switch input',flush=True);break
 if 'FIGHT' in t or 'Choose a Pok' in t or ('CANCEL' in t and t.count('HP')>=3):break
 if seen[t]>=3 and len(' '.join(t.splitlines()[-2:]))>15 and not any(x in t.lower() for x in ['yes','choose a pok','change pok']):act('c','wait:0.4')
 else:act('wait:0.4')
