"""Bounded reviewed Roserade setup; all state comes from rendered battle UI."""
from play import *
from public_owned_hp import read as hp_read

def guard():
 rows=snap();text=' '.join(v['text'] for v in rows).lower()
 assert 'roserade' in text and 'volcanion' in text and 'fight' in text and 'run' in text,text
 return hp_read(rows,434)
def item(name):
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_item.py'),name,'Volcanion'],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
for name in ['X Sp. Atk','X Speed','X Sp. Atk','X Speed']:
 hp=guard();print('SETUP GUARD HP',hp,'NEXT',name,flush=True)
 if hp<240:
  item('Full Restore');hp=guard();assert hp>=240,'Healing did not establish safe HP'
 item(name)
print('SETUP COMPLETE HP',guard(),flush=True)
