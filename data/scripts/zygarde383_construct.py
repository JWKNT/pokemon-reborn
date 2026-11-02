"""Normal assembly dialogue; keep Zygarde in party by boxing Cresselia."""
from play import *
import re
for _ in range(24):
 t=read();print(t,flush=True);lo=t.lower().replace("zugarde","zygarde")
 if 'construct?' in lo:
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
 elif 'nickname' in lo:
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
 elif 'party is full' in lo or 'party member to the pc' in lo:
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
 elif 'choose a pok' in lo:
  subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),'Cresselia','--single'],check=True)
 elif any(q.replace(' ','') in lo.replace(' ','') for q in ['cells active','cells required','constructing','obtained zygarde','cresselia was sent','complete.']):act('c','wait:.7')
 elif not re.sub('[^a-z]','',lo.replace('pokemon reborn','')):
  print('ASSEMBLY OVERWORLD',flush=True);break
 else:raise SystemExit('Assembly review: '+t)
else:raise SystemExit('Assembly bound')
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Zygarde383-Constructed'],check=True)
