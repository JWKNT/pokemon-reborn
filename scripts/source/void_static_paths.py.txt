"""Read-only offline routes from already extracted Void map JSON.

No imports of the UI/game driver, no native/save/navigation reads or writes.
Prints proposed paths and story touch events; observed coordinates remain
authoritative because cutscenes can move actors and update event pages.
"""
import json
from collections import deque
from itertools import groupby
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def path(v, start, goal):
    w, h = v['width'], v['height']
    data, pas, pri = v['data']['data'], v['passages']['data'], v['priorities']['data']
    blocked = {(e['x'], e['y']) for e in v['events'].values()
               if not e['through'] and e['character']}
    tile_events = {(e['x'], e['y']): e['tile_id'] for e in v['events'].values()
                   if not e['through'] and e['tile_id'] >= 0}

    def terrain(p):
        x, y = p
        if not (0 <= x < w and 0 <= y < h):
            return 0
        for z in [2, 1, 0]:
            t = data[x + w*y + w*h*z]
            tag = v['terrain']['data'][t]
            if tag and tag != 13:
                return tag
        return 0

    def landing(p):
        x, y = p
        if not (0 <= x < w and 0 <= y < h) or p in blocked:
            return False
        if p in tile_events:
            t = tile_events[p]
            if pas[t] & 15 == 15:
                return False
            if pri[t] == 0:
                return True
        for z in [2, 1, 0]:
            t = data[x + w*y + w*h*z]
            if pas[t] & 15 == 15:
                return False
            if pri[t] == 0:
                return True
        return True

    def okay(p, d):
        x, y = p
        if not (0 <= x < w and 0 <= y < h):
            return False
        bit = 1 << (d // 2 - 1)
        if p in tile_events:
            t = tile_events[p]
            if pas[t] & bit or pas[t] & 15 == 15:
                return False
            if pri[t] == 0:
                return True
        for z in [2, 1, 0]:
            t = data[x + w*y + w*h*z]
            if pas[t] & bit or pas[t] & 15 == 15:
                return False
            if pri[t] == 0:
                return True
        return True

    q, prev = deque([start]), {start: None}
    while q:
        p = q.popleft()
        if p == goal:
            break
        for dx, dy, d, name in [(0, 1, 2, 'down'), (-1, 0, 4, 'left'),
                                (1, 0, 6, 'right'), (0, -1, 8, 'up')]:
            n = p[0]+dx, p[1]+dy
            if n in blocked or not okay(p, d) or not okay(n, 10-d):
                continue
            if terrain(n) == 1:
                n = p[0]+2*dx, p[1]+2*dy
                name = 'jump:'+name
                if not landing(n):
                    continue
            if n in prev:
                continue
            prev[n] = p, name
            q.append(n)
    if goal is None:
        return prev
    if goal not in prev:
        raise ValueError(f'No offline path to {goal}')
    nodes, keys, p = [goal], [], goal
    while prev[p]:
        p, key = prev[p]
        nodes.append(p)
        keys.append(key)
    return list(reversed(keys)), list(reversed(nodes))


def event_leg(mid, start, eid, v=None):
    if v is None:
        v = json.loads((ROOT/'work'/f'void-map-{mid}.json').read_text())
    e = v['events'][str(eid)]
    if e['trigger'] == 1 and not e['character']:
        candidates = [(e['x'], e['y'])]
    else:
        candidates = [(e['x']+dx, e['y']+dy)
                      for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    options = []
    for goal in candidates:
        try:
            keys, nodes = path(v, start, goal)
            options.append((len(keys), goal, keys, nodes))
        except ValueError:
            pass
    if not options:
        raise ValueError(f'No accessible offline face for {mid}E{eid}')
    count, goal, keys, nodes = min(options)
    encountered = []
    for p in nodes[1:]:
        for key, ev in v['events'].items():
            if (ev['x'], ev['y']) == p and ev['trigger'] == 1 and any(
                    c['code'] not in [0, 108, 408] for c in ev['list']):
                encountered.append({'event': int(key), 'name': ev['name'], 'xy': p})
    return {'map': mid, 'start': start, 'target_event': eid, 'approach': goal,
            'steps': count, 'runs': [[k, len(list(g))] for k, g in groupby(keys)],
            'touch_stops': encountered}


if __name__ == '__main__':
    legs = []
    # Only RAM copies change here. These are source-conditioned route proposals,
    # never observed state or instructions to execute blindly across cutscenes.
    def cleared(v, ids):
        for eid in ids:
            v['events'][str(eid)].update(character='', through=True, list=[])

    for mid, start, events in [
            (754, (31, 12), [5, 2, 3]),
            (755, (60, 81), [24]),
            (756, (62, 64), [3, 2, 4]),
            (757, (102, 20), [2, 14, 16, 17, 24, 26, 27])]:
        v = json.loads((ROOT/'work'/f'void-map-{mid}.json').read_text())
        for eid in events:
            leg = event_leg(mid, start, eid, v)
            leg['state'] = 'hypothetical; refresh observed state after story stops'
            legs.append(leg)
            start = tuple(leg['approach'])
            cleared(v, [eid])
            # Lin is removed by a runtime move route. Radomus removes Luna too,
            # then sets switch973; unlike other gates it does not use self-A.
            if mid == 757 and eid == 26:
                cleared(v, [147])
    v = json.loads((ROOT/'work'/'void-map-758.json').read_text())
    # Stop one tile before the boss touch trigger, never on 758E122[28,105].
    keys, nodes = path(v, (120, 158), (28, 106))
    legs.append({'map': 758, 'start': [120, 158], 'target_event': 122,
                 'approach': [28, 106], 'steps': len(keys),
                 'runs': [[k, len(list(g))] for k, g in groupby(keys)],
                 'touch_stops': [{'event': int(eid), 'name': e['name'],
                                  'xy': [e['x'], e['y']]}
                                 for eid, e in v['events'].items()
                                 if (e['x'], e['y']) in nodes[1:]
                                 and e['trigger'] == 1
                                 and any(c['code'] not in [0,108,408]
                                         for c in e['list'])],
                 'state': 'hypothetical; boss is one UP beyond endpoint'})
    print(json.dumps(legs, indent=2))
