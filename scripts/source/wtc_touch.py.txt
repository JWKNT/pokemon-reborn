"""Bump an inspected automatic Titania water control and verify its real transfer."""
from play import *
from locate import locate
from wtc_model import predict

old, eid, new, x, y, target_ground = map(int, sys.argv[1:7])
key = sys.argv[7]
delta = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
assert key in delta
actual = locate(old)
assert actual[0] == old
s = json.loads((ROOT/'notes/navigation-state.json').read_text())
v = json.loads(subprocess.check_output(
    ['ruby', str(ROOT/'scripts/route_map.rb'), str(old), *map(str, actual[1:])],
    stderr=subprocess.DEVNULL))
e = v['events'][str(eid)]
cs = e['list'] or []
assert e['trigger'] in [1, 2]
assert any(c['code'] == 122 and c['parameters'][0] in range(256, 265) for c in cs)
assert not any(c['code'] in [101, 102, 103, 104, 301, 355, 655] for c in cs)
dx, dy = delta[key]
assert (e['x'], e['y']) == (x+dx, y+dy)
_, predicted, _ = predict(s, old, eid)
assert predicted == new
subprocess.run([sys.executable, str(ROOT/'scripts/layer_walk.py'), str(old),
                str(x), str(y), str(int(s['switches'].get('410', False))),
                str(target_ground)], check=True)
act(key+':.12', 'wait:2')
subprocess.run([sys.executable, str(ROOT/'scripts/wtc_control_notes.py'),
                str(old), str(eid), str(new)], check=True)
