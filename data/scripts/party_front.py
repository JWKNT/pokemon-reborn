"""Arrange named front party slots once, verifying the visible cards after each swap."""
from play import *
from party_cursor import selected_card, selection_path
import difflib

names = sys.argv[1:]
assert 1 <= len(names) <= 6 and len(set(names)) == len(names)
subprocess.run([sys.executable, str(ROOT/'scripts/party_open.py')], check=True)

def card_for(name, rows):
    matches = []
    for v in rows:
        word = re.sub('[^a-z]', '', v['text'].lower())
        if name.lower()=='mew' and word=='hew': word='mew'
        score = difflib.SequenceMatcher(None, name.lower(), word).ratio()
        if score >= .78 and .1 < v['y'] < .7:
            col = int(v['x'] > .5)
            row = round((v['y']-(.15 if not col else .195))/.21)
            if row in [0, 1, 2]: matches.append((score, row*2+col))
    assert matches, ('Named party card not found', name)
    return max(matches)[1]

for destination, name in enumerate(names):
    rows = snap()
    source = card_for(name, rows)
    if source == destination: continue
    keys = selection_path(selected_card(STATE), destination)
    if keys: act(*keys, 'wait:.3'); snap()
    assert selected_card(STATE) == destination
    act('a', 'wait:.4', *selection_path(destination, source), 'wait:.3')
    snap()
    assert selected_card(STATE) == source
    act('c', 'wait:2')
    assert card_for(name, snap()) == destination, 'Party swap result review'
for destination, name in enumerate(names):
    assert card_for(name, snap()) == destination
subprocess.run([sys.executable, str(ROOT/'scripts/overworld.py')], check=True)
print('NAMED PARTY FRONT VERIFIED', names, flush=True)
