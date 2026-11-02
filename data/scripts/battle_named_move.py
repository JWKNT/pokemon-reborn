"""Resolve an actor's named move from the unchanged saved build, then use normal UI.

For unsaved move learning/replacement, take a new normal checkpoint before using
this helper. It never reads live AI, RNG or game memory, and never edits game data.
"""
from play import *
import difflib
actor,move=sys.argv[1:3];target=sys.argv[3:4]
rows=snap();prompt=' '.join(v['text'] for v in rows if v['y']>.72 and v['x']<.5)
assert any(difflib.SequenceMatcher(None,actor.lower(),w.lower().strip('.,?')).ratio()>.72 for w in prompt.split()),'Named actor must match fresh battle prompt'
s=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/status_full.rb')],stderr=subprocess.DEVNULL))
mon=next(m for m in s['party'] if m['name']==actor)
slots=[i for i,m in enumerate(mon['moves']) if m['move']==move.upper()]
assert len(slots)==1,'Named move not in verified saved build'
print('NAMED MOVE',actor,move.upper(),'slot',slots[0],flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),str(slots[0]),*target,'--watch'],check=True)
