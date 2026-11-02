"""Use the installed 50% enhancement machine via its normal UI."""
from play import *
import re
for _ in range(20):
 t=read();print(t,flush=True);lo=t.lower().replace(' ','')
 if 'chooseapok' in lo or ('cancel' in lo and lo.count('hp')>=5):
  subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),'Zygarde','--single'],check=True)
 elif 'enhance?' in lo:
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
 elif any(q in lo for q in ['50%enhancement','cellsactive:40','40cellsrequired','enhancing','complete.']):act('c','wait:.8')
 elif not re.sub('[^a-z]','',lo.replace('pokemonreborn','')):break
 else:raise SystemExit('Enhancement review: '+t)
else:raise SystemExit('Enhancement bound')
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Zygarde383-50Percent'],check=True)
