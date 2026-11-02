"""Up to six reviewed Flamethrowers; stops if a foe survives or actor changes."""
from play import *
from public_owned_hp import read as hp_read
foes=['roserade','breloom','klinklang','ferrothorn','cinccino','magearna']
def state():
 rows=snap();t=' '.join(v['text'] for v in rows).lower()
 if re.search(r'de.?feated|for winning',t):return None
 assert 'volcanion' in t and 'fight' in t and 'run' in t,t
 enemy=' '.join(v['text'].lower() for v in rows if v['y']<.37).replace('cinceino','cinccino')
 match=[f for f in foes if f in enemy];assert len(match)==1,enemy
 hp=hp_read(rows,434);assert hp>60,'HP safety review'
 return match[0],hp
for i in range(6):
 before=state()
 if before is None:break
 print('SWEEP TURN',i+1,'FOE/HP',before,flush=True)
 result=subprocess.run([sys.executable,str(ROOT/'scripts/battle_turn.py'),'1'])
 if result.returncode:
  text=read().lower()
  assert 'change pok' in text and 'yes' in text and 'no' in text,text
  subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
 after=state()
 if after is None:print('PUBLIC VICTORY',flush=True);break
 assert after[0]!=before[0],'Opponent survived; review before further input'
else:print('Six-attack bound reached',flush=True)
