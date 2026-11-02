from play import *
for item in ['X Defend','X Defend','X Speed','X Speed']:
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_item.py'),item,'Magearna'],check=True)
 act('wait:1');subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'Magearna','1','--foes','Cresselia','--turns','6','--status-move','--heal-below','.45','--heal-item','Ultra Potion','--stop-after-victory'],check=True)
