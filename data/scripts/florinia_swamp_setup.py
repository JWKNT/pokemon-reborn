"""Three X Attacks only against publicly verified, PP-exhausted Cradily."""
from play import *
import difflib
for _ in range(3):
 r=snap();t=' '.join(x['text'] for x in r).lower();enemy=' '.join(x['text'].lower() for x in r if x['y']<.35)
 assert 'fight' in t and 'swampert' in t and any(difflib.SequenceMatcher(None,'cradily',w).ratio()>.8 for w in enemy.split()),'Setup actor/foe changed; stop'
 subprocess.run([sys.executable,str(ROOT/'scripts/public_turn_capture.py'),'battle_item.py','X Attack','Swampert'],check=True)
