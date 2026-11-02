"""Talk to the wandering Eustace from the visually verified room tile."""
from play import *
for i in range(30):
 t=read();print(t,flush=True)
 if 'eustace' in t.lower() or 'scheme' in t.lower():break
 assert len(t.strip().splitlines())<=1,t
 act('c','wait:.2')
else:raise SystemExit('Wandering NPC not adjacent; inspect screen')
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=35'],check=True)
t=read().lower();assert 'choose a pok' in t or ('cancel' in t and 'able' in t),t
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),'Vanillite','--single'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=35'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'League220-VanilliteReturned'],check=True)
