"""Use one visibly selected owned Repel through the ordinary field bag."""
from play import *

item = sys.argv[1] if len(sys.argv) > 1 else 'Super Repel'
assert item in ['Repel', 'Super Repel', 'Max Repel']
t = read().lower()
assert not re.search(r'\bfight\b|\bwild\b|\bhp\b', t), 'Field screen required'
if '--bag-open' not in sys.argv:
 act('x', 'wait:.5', 'c', 'wait:1')
 t = read().lower()
 if 'pokedex' in t and ('seen' in t or 'search' in t):
  act('x', 'wait:1', 'down', 'down', 'c', 'wait:1')
  t = read().lower()
 if 'cancel' in t and t.count('hp') >= 5:
  act('x', 'wait:1', 'down', 'c', 'wait:1'); t = read().lower()
 assert 'sort' in t or 'close bag' in t or sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3, 'Bag entry review'
for _ in range(9):
 if any(v['text'].strip().lower() == 'items' for v in snap()): break
 act('left', 'wait:.3')
else: raise SystemExit('Items pocket review')
subprocess.run([sys.executable, str(ROOT/'scripts/bag_select.py'), item, '--single-step'], check=True)
act('c', 'wait:.5')
assert any(v['text'].strip(' •›>').lower() in ['use', 'ulse', 'uee', 'uze', 'lise', 'lse', 'p use', 'p lise'] for v in snap()), 'Use menu review'
act('c', 'wait:1')
t = read().lower()
assert 'repel' in t and ('used' in t or 'lingered from' in t), 'Repel result review: '+t
act('c', 'wait:.5')
subprocess.run([sys.executable, str(ROOT/'scripts/overworld.py')], check=True)
