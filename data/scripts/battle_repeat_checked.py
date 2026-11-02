"""Bounded single-battle repetition, checked only against the public command UI."""
import argparse, difflib, re, subprocess, sys
from play import snap, ROOT

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--actor', required=True)
p.add_argument('--foe', required=True)
p.add_argument('--slot', type=int, choices=range(4), required=True)
p.add_argument('--count', type=int, required=True)
p.add_argument('--min-hp', type=int, required=True)
a = p.parse_args()
assert 1 <= a.count <= 4 and a.min_hp > 0

def matches(name, words):
    return any(difflib.SequenceMatcher(None, name.lower(), re.sub('[^a-z]', '', word.lower())).ratio() > .84 for word in words.split())

for turn in range(a.count):
    rows = snap()
    text = ' '.join(r['text'] for r in rows)
    assert 'fight' in text.lower() and re.search(r'\b(?:bag|bae)\b', text, re.I), 'Command menu changed'
    actor = ' '.join(r['text'] for r in rows if r['x'] < .55 and r['y'] > .72)
    foe = ' '.join(r['text'] for r in rows if r['y'] < .37)
    assert matches(a.actor, actor), 'Actor changed: ' + actor
    assert matches(a.foe, foe), 'Foe changed: ' + foe
    # The directly reviewed Glitch HUD slash sometimes OCRs as uppercase F.
    hp = re.findall(r'(?<!\d)(\d+)\s*[/F]\s*(\d+)(?!\d)', text)
    assert len(hp) == 1, 'Single HP reading required: ' + text
    current, maximum = map(int, hp[0])
    assert a.min_hp <= current <= maximum, 'HP guard: ' + str(hp)
    print('PUBLIC CHECK', turn + 1, a.actor, a.foe, current, maximum, flush=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/battle_move.py'), str(a.slot), '--watch'], check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/battle_ready.py')], check=True)
print('BOUNDED REPETITION COMPLETE', flush=True)
