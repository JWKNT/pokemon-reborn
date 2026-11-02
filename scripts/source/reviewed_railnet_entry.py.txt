"""Queue reviewed Devon approach, fleeing only known Railnet wild Noibat.
Uses normal controls; pauses at Arclight's readiness choice.
"""
from play import *
import re
steps=[('eventq.py','228','1','enter'),('eventq.py','229','150','talk'),('linear_dialog.py','229','150','--active','--until-choice','--burst')]
for command in steps:
 for attempt in range(8):
  t=read().lower()
  if 'noibat' in t and ('fight' in t or re.search(r'\bhp\b',t)):
   subprocess.run([sys.executable,str(ROOT/'scripts/flee.py')],check=True)
  started=time.time();r=subprocess.run([sys.executable,str(ROOT/'scripts'/command[0]),*command[1:]])
  if r.returncode==0:break
  now=read().lower()
  if 'noibat' in now and ('fight' in now or re.search(r'\bhp\b',now)):
   rows=[json.loads(l)for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]
   anchor=next((x['epoch']for x in rows if x['epoch']>=started and 'wild' in ' '.join(x['text']).lower()),time.time()-4)
   subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(anchor)],check=True);continue
  if command[0]=='eventq.py' and command[1:3]==('229','150') and 'arc:' in now and 'lowdo' in now:
   print('Inspected Arclight readiness scene reached',flush=True);break
  if command[0]=='eventq.py' and command[1]=='228':
   from locate import locate
   m,x,y=locate()
   if m==229:print('Reviewed entry reached despite interrupted transfer',flush=True);break
  raise SystemExit('Unexpected approach interruption')
 else:raise SystemExit('Railnet wild encounter budget exhausted')
