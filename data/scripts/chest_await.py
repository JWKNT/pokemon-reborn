"""Await a chest defender from a prepared interception tile using public UI.

Only advance the known Blaziken speed warning. Stop on battle or any other
dialogue; on timeout immediately try to freeze the actual Bag screen.
"""
from play import *
from chest_safe_pause import classify,finish_bag_entry
if '--world-open' not in sys.argv:
    assert classify(snap())=='bag','Begin in actual Bag'
    act('x:.12','wait:1','x:.12')
deadline=time.time()+45
while time.time()<deadline:
    r=snap();t=' '.join(v['text']for v in r).lower()
    print(t,flush=True)
    if ('wild' in t and ('appeared' in t or ('hp' in t and ' a wild ' in t))) or any(k in t for k in ['what will','like to battle']):
        print('BATTLE OBSERVED; no action selected',flush=True);break
    if 'garchomp is preparing' in t and 'rush' in t and os.environ.get('REBORN_POST_BATTLE_GOAL'):
        from fast_chest_transition import finish
        finish()
        break
    if 'repel' in t and 'wore off' in t:
        act('c:.12','wait:.25');continue
    if 'use another repel' in t:
        act('x:.12','wait:.25');continue
    if 'blaziken is' in t and 'up speed' in t:
        act('c:.12','wait:.5');continue
    if any(v['y']>.72 and len(v['text'])>12 for v in r):
        raise SystemExit('Unexpected dialogue; immediate review needed')
    act('wait:.25')
else:
    act('x:.12','wait:.3','c:.12','wait:1.2')
    finish_bag_entry()
    raise SystemExit('No battle; safely paused in Bag')
