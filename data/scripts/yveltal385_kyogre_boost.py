from play import *
for item in ['X Sp. Def','X Sp. Atk','X Sp. Atk']:
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_item.py'),item,'Kyogre'],check=True)
 act('wait:1');subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
